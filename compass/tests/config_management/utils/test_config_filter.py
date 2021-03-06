#!/usr/bin/python
#
# Copyright 2014 Huawei Technologies Co. Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""test config_filter module.

   .. moduleauthor:: Xiaodong Wang <xiaodongwang@huawei.com>
"""
import os
import unittest2


os.environ['COMPASS_IGNORE_SETTING'] = 'true'


from compass.utils import setting_wrapper as setting
reload(setting)


from compass.config_management.utils import config_filter
from compass.utils import flags
from compass.utils import logsetting


class TestConfigFilter(unittest2.TestCase):
    """test config filter class."""

    def setUp(self):
        super(TestConfigFilter, self).setUp()
        logsetting.init()

    def tearDown(self):
        super(TestConfigFilter, self).tearDown()

    def test_allows(self):
        """test allows rules."""
        config = {'1': '1',
                  '2': {'22': '22',
                        '33': {'333': '333',
                               '44': '444'}},
                  '3': {'33': '44'}}
        allows = ['*', '3', '5']
        configfilter = config_filter.ConfigFilter(allows)
        filtered_config = configfilter.filter(config)
        self.assertEqual(filtered_config, config)
        allows = ['/1', '2/22', '5']
        expected_config = {'1': '1', '2': {'22': '22'}}
        configfilter = config_filter.ConfigFilter(allows)
        filtered_config = configfilter.filter(config)
        self.assertEqual(filtered_config, expected_config)
        allows = ['*/33']
        expected_config = {'2': {'33': {'333': '333',
                                        '44': '444'}},
                           '3': {'33': '44'}}
        configfilter = config_filter.ConfigFilter(allows)
        filtered_config = configfilter.filter(config)
        self.assertEqual(filtered_config, expected_config)

    def test_denies(self):
        """test denies rules."""
        config = {'1': '1', '2': {'22': '22',
                                  '33': {'333': '333',
                                         '44': '444'}},
                            '3': {'33': '44'}}
        denies = ['/1', '2/22', '2/33/333', '5']
        expected_config = {'2': {'33': {'44': '444'}}, '3': {'33': '44'}}
        configfilter = config_filter.ConfigFilter(denies=denies)
        filtered_config = configfilter.filter(config)
        self.assertEqual(filtered_config, expected_config)
        denies = ['*']
        configfilter = config_filter.ConfigFilter(denies=denies)
        filtered_config = configfilter.filter(config)
        self.assertIsNone(filtered_config)
        denies = ['*/33']
        expected_config = {'1': '1', '2': {'22': '22'}}
        configfilter = config_filter.ConfigFilter(denies=denies)
        filtered_config = configfilter.filter(config)
        self.assertEqual(filtered_config, expected_config)


if __name__ == '__main__':
    flags.init()
    logsetting.init()
    unittest2.main()
