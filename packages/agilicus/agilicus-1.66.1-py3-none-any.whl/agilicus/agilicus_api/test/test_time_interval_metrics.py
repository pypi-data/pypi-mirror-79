# coding: utf-8

"""
    Agilicus API

    Agilicus API endpoints  # noqa: E501

    The version of the OpenAPI document: 2020.09.08
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import agilicus_api
from agilicus_api.models.time_interval_metrics import TimeIntervalMetrics  # noqa: E501
from agilicus_api.rest import ApiException

class TestTimeIntervalMetrics(unittest.TestCase):
    """TimeIntervalMetrics unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TimeIntervalMetrics
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.time_interval_metrics.TimeIntervalMetrics()  # noqa: E501
        if include_optional :
            return TimeIntervalMetrics(
                time = '2019-05-16T19:11:18Z', 
                metric = 1
            )
        else :
            return TimeIntervalMetrics(
        )

    def testTimeIntervalMetrics(self):
        """Test TimeIntervalMetrics"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
