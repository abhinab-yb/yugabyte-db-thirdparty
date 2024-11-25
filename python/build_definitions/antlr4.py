#
# Copyright (c) YugabyteDB, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations
# under the License.
#

import os
import subprocess

from yugabyte_db_thirdparty.build_definition_helpers import *
from yugabyte_db_thirdparty.util import which_must_exist
from yugabyte_db_thirdparty.string_util import shlex_join

class Antlr4Dependency(Dependency):
    def __init__(self) -> None:
        super(Antlr4Dependency, self).__init__(
            name='antlr4',
            version='4.13.2',
            url_pattern='https://github.com/abhinab-yb/antlr4/archive/refs/tags/{0}.tar.gz',
            build_group=BuildGroup.POTENTIALLY_INSTRUMENTED)
        self.copy_sources = True

    def build(self, builder: BuilderInterface) -> None:
        antlr_jar_url = 'https://www.antlr.org/download/antlr-4.13.2-complete.jar'
        curl_path = which_must_exist('curl')
        antlr_jar_location = os.path.join(builder.fs_layout.get_source_path(self), 'antlr-4.13.2-complete.jar')
        curl_cmd_line = [
            curl_path,
            '-o',
            antlr_jar_location,
            '-L',
            '--silent',
            '--show-error',
            '--location',
            antlr_jar_url]
        log("Running command: %s", shlex_join(curl_cmd_line))
        subprocess.check_call(curl_cmd_line)
        builder.build_with_cmake(self,
                            ["-DANTLR_JAR_LOCATION={path}".format(path=antlr_jar_location)])
