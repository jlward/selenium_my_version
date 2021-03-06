# Copyright 2008-2009 WebDriver committers
# Copyright 2008-2009 Google Inc.
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

import logging
import socket
import sys
import unittest


def run_tests(test_case, driver, webserver):
    logging.basicConfig(level=logging.WARN)

    webserver.start()
    try:
        testLoader = unittest.TestLoader()
        testRunner = unittest.TextTestRunner()
        test_case_name = "selenium.common_tests.%s" % test_case
        if len(sys.argv) > 1:
            testMethod = sys.argv[1]
            testRunner.run(
                testLoader.loadTestsFromName(
                    "%s.%s" % (test_case_name, testMethod)))
        else:
            testRunner.run(testLoader.loadTestsFromName(test_case_name))
        driver.quit()
    finally:
        webserver.stop()


def require_online(func):
    """Only exucte the test method if the internet is accessible."""
    def testMethod(self):
        socket_ = socket.socket()
        try:
            socket_.settimeout(1)
            socket_.connect(("www.google.com", 80))
            return func(self)
        except socket.error:
            return lambda x: None
    testMethod.func_name = func.func_name
    return testMethod


def convert_cookie_to_json(cookie):
    cookie_dict = {}
    for key, value in cookie.items():
        if key == "expires":
            cookie_dict["expiry"] = int(value) * 1000
        else:
            cookie_dict[key] = value
    return cookie_dict
