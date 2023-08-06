# Copyright 2018 Google Inc.
# Copyright 2019 Yelp
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Limited mock of google-cloud-sdk for tests
"""
import sys
from io import BytesIO
from unittest import SkipTest

try:
    from google.cloud.logging.entries import StructEntry
    from google.cloud.logging.resource import Resource
    from google.oauth2.credentials import Credentials
except ImportError:
    if sys.version_info[:2] == (3, 4):
        raise SkipTest('Google libraries are not supported on Python 3.4')
    else:
        raise

from mrjob.fs.gcs import parse_gcs_uri

from .dataproc import MockGoogleDataprocClusterClient
from .dataproc import MockGoogleDataprocJobClient
from .logging import MockGoogleLoggingClient
from .storage import MockGoogleStorageClient
from tests.mr_two_step_job import MRTwoStepJob
from tests.py2 import Mock
from tests.py2 import patch
from tests.sandbox import SandboxedTestCase

_TEST_PROJECT = 'test-mrjob:test-project'


class MockGoogleTestCase(SandboxedTestCase):

    def setUp(self):
        super(MockGoogleTestCase, self).setUp()

        # maps (project_id, region, cluster_name) to a
        # google.cloud.dataproc_v1beta2.types.Cluster
        self.mock_clusters = {}

        # maps (project_id, region, job_name) to a
        # google.cloud.dataproc_v1beta2.types.Job
        self.mock_jobs = {}

        # set this to False to make jobs ERROR
        self.mock_jobs_succeed = True

        # a list of StructEntry objects for mock logging client to return
        self.mock_log_entries = []

        # mock OAuth token, returned by mock google.auth.default()
        self.mock_token = 'mock_token'

        # mock project ID, returned by mock google.auth.default()
        self.mock_project_id = 'mock-project-12345'

        # Maps bucket name to a dictionary with the keys
        # *blobs* and *location*. *blobs* maps object name to
        # a dictionary with the key *data*, which is
        # a bytestring.
        self.mock_gcs_fs = {}

        self.start(patch('google.api_core.grpc_helpers.create_channel',
                         self.create_channel))

        self.start(patch('google.auth.default', self.auth_default))

        self.start(patch(
            'google.cloud.dataproc_v1beta2.ClusterControllerClient',
            self.cluster_client))

        self.start(patch('google.cloud.dataproc_v1beta2.JobControllerClient',
                         self.job_client))

        self.start(patch('google.cloud.logging.Client',
                         self.logging_client))

        self.start(patch('google.cloud.storage.client.Client',
                         self.storage_client))

        self.start(patch('time.sleep'))

    def auth_default(self, scopes=None):
        credentials = Credentials(self.mock_token, scopes=scopes)
        return (credentials, self.mock_project_id)

    def create_channel(self, target, credentials=None):
        channel = Mock()
        channel._channel = Mock()
        channel._channel.target = Mock(return_value=target)

        return channel

    def cluster_client(self, channel=None, credentials=None):
        return MockGoogleDataprocClusterClient(
            channel=channel,
            credentials=credentials,
            mock_clusters=self.mock_clusters,
            mock_gcs_fs=self.mock_gcs_fs,
            mock_jobs=self.mock_jobs,
            mock_jobs_succeed=self.mock_jobs_succeed,
        )

    def job_client(self, channel=None, credentials=None):
        return MockGoogleDataprocJobClient(
            channel=channel,
            credentials=credentials,
            mock_clusters=self.mock_clusters,
            mock_gcs_fs=self.mock_gcs_fs,
            mock_jobs=self.mock_jobs,
            mock_jobs_succeed=self.mock_jobs_succeed,
        )

    def logging_client(self, project=None, credentials=None):
        return MockGoogleLoggingClient(
            credentials=credentials,
            mock_log_entries=self.mock_log_entries,
            project=project,
        )

    def storage_client(self, project=None, credentials=None):
        return MockGoogleStorageClient(mock_gcs_fs=self.mock_gcs_fs)

    def add_mock_log_entry(
            self, payload, logger, insert_id=None, timestamp=None,
            labels=None, severity=None, http_request=None, resource=None):

        if isinstance(resource, dict):
            resource = Resource(**resource)

        entry = StructEntry(
            http_request=http_request,
            insert_id=insert_id,
            labels=labels,
            logger=logger,
            payload=payload,
            resource=resource,
            severity=severity,
            timestamp=timestamp,
        )

        self.mock_log_entries.append(entry)

    def make_runner(self, *args):
        """create a dummy job, and call make_runner() on it.
        Use this in a with block:

        with self.make_runner() as runner:
            ...
        """
        stdin = BytesIO(b'foo\nbar\n')
        mr_job = MRTwoStepJob(['-r', 'dataproc'] + list(args))
        mr_job.sandbox(stdin=stdin)

        return mr_job.make_runner()

    def put_gcs_multi(self, gcs_uri_to_data_map):
        client = self.storage_client()

        for uri, data in gcs_uri_to_data_map.items():
            bucket_name, blob_name = parse_gcs_uri(uri)

            bucket = client.bucket(bucket_name)
            if not bucket.exists():
                bucket.create()

            blob = bucket.blob(blob_name)
            blob.upload_from_string(data)

    def put_job_output_parts(self, dataproc_runner, raw_parts):
        """Generate fake output on GCS for the given Dataproc runner."""
        assert type(raw_parts) is list

        base_uri = dataproc_runner.get_output_dir()
        gcs_multi_dict = dict()
        for part_num, part_data in enumerate(raw_parts):
            gcs_uri = base_uri + 'part-%05d' % part_num
            gcs_multi_dict[gcs_uri] = part_data

        self.put_gcs_multi(gcs_multi_dict)
