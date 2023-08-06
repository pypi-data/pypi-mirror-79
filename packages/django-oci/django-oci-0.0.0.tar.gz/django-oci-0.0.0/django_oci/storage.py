"""

Copyright (c) 2020, Vanessa Sochat

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http.response import Http404, HttpResponse
from django_oci import settings
from django.urls import reverse
from django_oci.models import Blob, Image, Repository
from django_oci.utils import parse_image_name
from rest_framework.response import Response

import hashlib
import logging

logger = logging.getLogger(__name__)

def get_storage():
    """Return the correct storage handler based on the key obtained from
       settings
    """
    storage = settings.STORAGE_BACKEND
    lookup = {"filesystem": FileSystemStorage}
    if storage not in lookup:
        logger.warning(f"{storage} not supported as a storage backend, defaulting to filesystem.")         
        storage = "filesystem"
    return lookup[storage]()

# Storage backends for django_oci
# each should have default set of functions for:
# monolithic upload
# chunked upload
# etc.

class StorageBase:
    """A storage base provides shared functions for a storage type
    """  
  
    def calculate_digest(self, body):
        """Calculate the sha256 sum for some body (bytes)
        """
        hasher = hashlib.sha256()
        hasher.update(body)
        return hasher.hexdigest()


class FileSystemStorage(StorageBase):

    def create_blob_request(self, name, content_type):
        """A create blob request is intended to be done first with a name,
           digest, and content type, and we do all steps of the creation
           except for the actual upload of the file, which is handled
           by a second PUT request.
        """
        # TODO: need to make UploadSession with identifier, that expires after some time
        ids = parse_image_name(name)
        tag = ids.get('tag', 'latest')
        collection = ids.get('url')

        # Here we get the repository based on the name (get or create)
        # TODO: will need to add owner
        repository, _ = Repository.objects.get_or_create(name=collection)

        # Get the image associated with the tag
        image, _ = Image.objects.get_or_create(repository=repository, tag=tag)

        # Upon success, the response MUST have a code of 202 Accepted with a location header
        return Response(status=202, headers={"Location": image.create_upload_session()})


    def create_chunked_request(self, name, content_type):
        pass

    def create_blob(self, name, digest, body, content_type):
        """Create an image blob from a monolithic post. We get the repository
           name along with the body for the blob and the digest.

           Parameters
           ==========
           name (str): the name of the repository
           body (bytes): the request body to write the container
           uri (str): the unique resource identifier to create
        """
        # the <digest> MUST match the blob's digest (how to calculate)
        calculated_digest = self.calculate_digest(body)
        if calculated_digest != digest:
            return Response(status=400)
        
        # Parse image name to get tag, etc.
        ids = parse_image_name(name)
        tag = ids.get('tag', 'latest')
        collection = ids.get('url')

        # Here we get the repository based on the name (get or create)
        # TODO: will need to add owner
        repository, _ = Repository.objects.get_or_create(name=collection)

        # Get the image associated with the tag
        image, _ = Image.objects.get_or_create(repository=repository, tag=tag)

        # Create the blob, and associate with image
        blob, created = Blob.objects.get_or_create(digest=calculated_digest, content_type=content_type, image=image)

        # Update blob body
        datafile = SimpleUploadedFile(calculated_digest, body, content_type=content_type)
        blob.datafile = datafile
        blob.save()

        # If it's already existing, return Accepted header, otherwise alert created        
        status_code = 202
        if created:
            status_code = 201        

        # Location header must have <blob-location> being a pullable blob URL.
        return Response(status=status_code, headers={"Location": blob.get_download_url()})


    def download_blob(self, name, digest):
        """Given a blob repository name and digest, return response to stream download.
           The repository name is associated to the blob via the image.
        """
        ids = parse_image_name(name)
        try:
            blob = Blob.objects.get(digest=digest, image__repository__name=ids['url'])
        except Blob.DoesNotExist:
            raise Http404

        blob_path = os.path.join(settings.MEDIA_ROOT, blob.datafile.name)
        if os.path.exists(blob_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type=blob.content_type)
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
