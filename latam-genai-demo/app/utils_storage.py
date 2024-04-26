# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import datetime

from configs import BUCKET_NAME
from google import auth
from google.cloud import storage


def upload_image_to_gcs(image_bytes: bytes, file_name: str) -> str:
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(file_name)
    blob.upload_from_string(image_bytes, content_type="image/jpeg")

    credentials, project_id = auth.default()
    if credentials.token is None:
        credentials.refresh(auth.transport.requests.Request())

    url = blob.generate_signed_url(
        version="v4",
        service_account_email=credentials.service_account_email,
        access_token=credentials.token,
        expiration=datetime.timedelta(minutes=15),
        method="GET",
    )
    return url
