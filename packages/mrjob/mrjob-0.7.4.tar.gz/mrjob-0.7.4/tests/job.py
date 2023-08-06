# Copyright 2015 Yelp
# Copyright 2017 Yelp
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
"""Utilities for testing jobs."""
from io import BytesIO


def run_job(job, raw_input=b''):
    """Run a MRJob and return its output as a dictionary."""
    job.sandbox(stdin=BytesIO(raw_input))

    with job.make_runner() as runner:
        runner.run()
        return {
            to_dict_key(k): v
            for k, v in
            job.parse_output(runner.cat_output())
        }


def to_dict_key(k):
    """Recursively convert lists to tuples.

    This only looks into lists, which seems to be good enough for testing
    """
    if isinstance(k, list):
        return tuple(to_dict_key(item) for item in k)
    else:
        return k
