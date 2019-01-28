# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

import yaml
import logging
from st2tests.base import BaseActionTestCase


class PackerBaseActionTestCase(BaseActionTestCase):
    __test__ = False

    def setUp(self):
        super(PackerBaseActionTestCase, self).setUp()
        logging.disable(logging.CRITICAL)  # disable logging
        self._blank_config = self.load_yaml('configs/blank.yaml')
        self._full_config = self.load_yaml('configs/full.yaml')

    def tearDown(self):
        super(EncoreBaseActionTestCase, self).tearDown()
        logging.disable(logging.NOTSET)  # enable logging

    def load_yaml(self, filename):
        return yaml.safe_load(self.get_fixture_content(filename))

    @property
    def blank_config(self):
        return self._blank_config

    @property
    def full_config(self):
        return self._full_config
