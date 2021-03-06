# --------------------------------------------------------------------------
# Copyright 2014-2016 Digital Sapphire Development Team
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
# --------------------------------------------------------------------------
from __future__ import unicode_literals

import pytest

from pyupdater.client.downloader import FileDownloader


FILENAME = 'dont+delete+pyu+test.txt'
FILENAME_WITH_SPACES = 'dont delete pyu test.txt'
FILE_HASH = '82719546b992ef81f4544fb2690c6a05b300a0216eeaa8f3616b3b107a311629'
URL = 'https://pyu-tester.s3.amazonaws.com/'


@pytest.mark.usefixtue("cleandir")
class TestData(object):

    def test_return(self):
        fd = FileDownloader(FILENAME, URL, FILE_HASH, verify=True)
        binary_data = fd.download_verify_return()
        assert binary_data is not None

    def test_cb(self):
        def cb(status):
            pass
        fd = FileDownloader(FILENAME, URL, FILE_HASH,
                            progress_hooks=[cb], verify=True)
        binary_data = fd.download_verify_return()
        assert binary_data is not None

    def test_return_fail(self):
        fd = FileDownloader(FILENAME, URL,
                            'JKFEIFJILEFJ983NKFNKL', verify=True)
        binary_data = fd.download_verify_return()
        assert binary_data is None


@pytest.mark.usefixtue("cleandir")
class TestUrl(object):
    def test_url_with_spaces(self):
        fd = FileDownloader(FILENAME_WITH_SPACES, URL,
                            FILE_HASH, verify=True)
        binary_data = fd.download_verify_return()
        assert binary_data is not None

    def test_bad_url(self):
        fd = FileDownloader(FILENAME, 'bad url', 'bad hash', verify=True)
        binary_data = fd.download_verify_return()
        assert binary_data is None


@pytest.mark.usefixtue("cleandir")
class TestContentLength(object):
    def test_bad_content_length(self):
        class FakeHeaders(object):
            headers = {}
        fd = FileDownloader(FILENAME, URL, FILE_HASH, verify=True)
        data = FakeHeaders()
        assert fd._get_content_length(data) == 100001

    def test_good_conent_length(self):
        fd = FileDownloader(FILENAME, URL, FILE_HASH, verify=True)
        fd.download_verify_return()
        assert fd.content_length == 2387
