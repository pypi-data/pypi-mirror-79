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
from agilicus_api.models.list_issuer_roots_response import ListIssuerRootsResponse  # noqa: E501
from agilicus_api.rest import ApiException

class TestListIssuerRootsResponse(unittest.TestCase):
    """ListIssuerRootsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ListIssuerRootsResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.list_issuer_roots_response.ListIssuerRootsResponse()  # noqa: E501
        if include_optional :
            return ListIssuerRootsResponse(
                issuer_roots = [
                    agilicus_api.models.issuer.Issuer(
                        id = '123', 
                        issuer = '0', 
                        enabled = True, 
                        org_id = '0', 
                        theme_file_id = 'ASsdq23lsaSSf', 
                        upstream_redirect_uri = '0', 
                        managed_upstreams = [
                            agilicus_api.models.managed_upstream_identity_provider.ManagedUpstreamIdentityProvider(
                                name = '0', 
                                enabled = True, )
                            ], 
                        oidc_upstreams = [
                            agilicus_api.models.oidc_upstream_identity_provider.OIDCUpstreamIdentityProvider(
                                name = '0', 
                                icon = 'city-login', 
                                issuer = '0', 
                                client_id = '0', 
                                client_secret = '0', 
                                issuer_external_host = '0', 
                                username_key = '0', 
                                email_key = '0', 
                                email_verification_required = True, 
                                request_user_info = True, 
                                user_id_key = '0', 
                                auto_create_status = 'active', )
                            ], 
                        clients = [
                            agilicus_api.models.issuer_client.IssuerClient(
                                id = '123', 
                                issuer_id = '123', 
                                name = '0', 
                                secret = '0', 
                                application = '0', 
                                org_id = '0', 
                                restricted_organisations = ["org-1","org-2"], 
                                organisation_scope = 'here_only', 
                                redirects = [
                                    '0'
                                    ], 
                                mfa_challenge = 'user_preference', )
                            ], )
                    ], 
                limit = 56
            )
        else :
            return ListIssuerRootsResponse(
                limit = 56,
        )

    def testListIssuerRootsResponse(self):
        """Test ListIssuerRootsResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
