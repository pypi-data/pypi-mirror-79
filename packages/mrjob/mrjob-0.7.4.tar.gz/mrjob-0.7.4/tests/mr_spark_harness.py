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
"""A wrapper for mrjob/spark/harness.py, so we can test the harness with
the inline runner."""
from mrjob.job import MRJob
from mrjob.options import _parse_raw_args
from mrjob.spark.harness import _PASSTHRU_OPTIONS
from mrjob.spark.harness import main as harness_main


_PASSTHRU_OPTION_STRINGS = {
    arg for args, kwargs in _PASSTHRU_OPTIONS for arg in args}
# handled separately because these are also runner options
_PASSTHRU_OPTION_STRINGS.update({
    '--emulate-map-input-file',
    '--max-output-files',
    '--skip-internal-protocol',
})


class MRSparkHarness(MRJob):

    def configure_args(self):
        super(MRSparkHarness, self).configure_args()

        # this is a positional argument in the spark harness
        self.add_passthru_arg(
            '--job-class', dest='job_class', type=str,
            help='dot-separated module and class name of MRJob',
            default='mrjob.job.MRJob')

        for args, kwargs in _PASSTHRU_OPTIONS:
            self.add_passthru_arg(*args, **kwargs)

        # these are both runner and harness switches
        self.pass_arg_through('--emulate-map-input-file')
        self.pass_arg_through('--max-output-files')
        self.pass_arg_through('--skip-internal-protocol')

    def spark(self, input_path, output_path):
        harness_args = [
            self.options.job_class, input_path, output_path]

        # find arguments to pass through to the Spark harness
        raw_args = _parse_raw_args(self.arg_parser, self._cl_args)

        for dest, option_string, args in raw_args:
            if option_string in _PASSTHRU_OPTION_STRINGS:
                harness_args.append(option_string)
                harness_args.extend(args)

        harness_main(harness_args)


if __name__ == '__main__':
    MRSparkHarness.run()
