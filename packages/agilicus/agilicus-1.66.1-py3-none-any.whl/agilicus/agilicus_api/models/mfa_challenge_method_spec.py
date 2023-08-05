# coding: utf-8

"""
    Agilicus API

    Agilicus API endpoints  # noqa: E501

    The version of the OpenAPI document: 2020.09.08
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from agilicus_api.configuration import Configuration


class MFAChallengeMethodSpec(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'priority': 'int',
        'challenge_type': 'str',
        'endpoint': 'str',
        'nickname': 'str',
        'enabled': 'bool'
    }

    attribute_map = {
        'priority': 'priority',
        'challenge_type': 'challenge_type',
        'endpoint': 'endpoint',
        'nickname': 'nickname',
        'enabled': 'enabled'
    }

    def __init__(self, priority=None, challenge_type=None, endpoint=None, nickname=None, enabled=None, local_vars_configuration=None):  # noqa: E501
        """MFAChallengeMethodSpec - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._priority = None
        self._challenge_type = None
        self._endpoint = None
        self._nickname = None
        self._enabled = None
        self.discriminator = None

        self.priority = priority
        self.challenge_type = challenge_type
        self.endpoint = endpoint
        if nickname is not None:
            self.nickname = nickname
        if enabled is not None:
            self.enabled = enabled

    @property
    def priority(self):
        """Gets the priority of this MFAChallengeMethodSpec.  # noqa: E501

        The priority of this challenge method. Priority is how the user specifies which challenge method to be notified with if that method is supported.  A priority of 1 is the highest priority and indicates that the user prefers this challenge method.  # noqa: E501

        :return: The priority of this MFAChallengeMethodSpec.  # noqa: E501
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this MFAChallengeMethodSpec.

        The priority of this challenge method. Priority is how the user specifies which challenge method to be notified with if that method is supported.  A priority of 1 is the highest priority and indicates that the user prefers this challenge method.  # noqa: E501

        :param priority: The priority of this MFAChallengeMethodSpec.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and priority is None:  # noqa: E501
            raise ValueError("Invalid value for `priority`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                priority is not None and priority < 1):  # noqa: E501
            raise ValueError("Invalid value for `priority`, must be a value greater than or equal to `1`")  # noqa: E501

        self._priority = priority

    @property
    def challenge_type(self):
        """Gets the challenge_type of this MFAChallengeMethodSpec.  # noqa: E501

        The type of challenge to issue. This controls how the user is informed of the challenge, as well as how the challenge can be satisfied. The follow types are supported:   - sms:  a `sms` challenge informs the user via text message of the challenge. The challenge can     be answered via the link provided in the text message. The user can deny the challenge via this     mechanism as well.   - web_push: a `web_push` challenge informs the user of the challenge on every device they have   registered via the web push (rfc8030) mechanism. If the user accepts via the link provided in   the web push, the challenge will be satisfied. The user can deny the challenge via this   mechanism as well.   - totp: a time-based one-time password challenge allows the user to enter the code from their registered   - webauthn: a challenge issued for a specific device the user has possession of. Either a yubikey, or a phone that has a Trusted Platform Module.   device and application. enum: [sms, web_push, totp, webauthn] example: web_push   # noqa: E501

        :return: The challenge_type of this MFAChallengeMethodSpec.  # noqa: E501
        :rtype: str
        """
        return self._challenge_type

    @challenge_type.setter
    def challenge_type(self, challenge_type):
        """Sets the challenge_type of this MFAChallengeMethodSpec.

        The type of challenge to issue. This controls how the user is informed of the challenge, as well as how the challenge can be satisfied. The follow types are supported:   - sms:  a `sms` challenge informs the user via text message of the challenge. The challenge can     be answered via the link provided in the text message. The user can deny the challenge via this     mechanism as well.   - web_push: a `web_push` challenge informs the user of the challenge on every device they have   registered via the web push (rfc8030) mechanism. If the user accepts via the link provided in   the web push, the challenge will be satisfied. The user can deny the challenge via this   mechanism as well.   - totp: a time-based one-time password challenge allows the user to enter the code from their registered   - webauthn: a challenge issued for a specific device the user has possession of. Either a yubikey, or a phone that has a Trusted Platform Module.   device and application. enum: [sms, web_push, totp, webauthn] example: web_push   # noqa: E501

        :param challenge_type: The challenge_type of this MFAChallengeMethodSpec.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and challenge_type is None:  # noqa: E501
            raise ValueError("Invalid value for `challenge_type`, must not be `None`")  # noqa: E501

        self._challenge_type = challenge_type

    @property
    def endpoint(self):
        """Gets the endpoint of this MFAChallengeMethodSpec.  # noqa: E501

        The specific device to issue the challenge to. The meaning of this field may change depending on the challenge type specified.  # noqa: E501

        :return: The endpoint of this MFAChallengeMethodSpec.  # noqa: E501
        :rtype: str
        """
        return self._endpoint

    @endpoint.setter
    def endpoint(self, endpoint):
        """Sets the endpoint of this MFAChallengeMethodSpec.

        The specific device to issue the challenge to. The meaning of this field may change depending on the challenge type specified.  # noqa: E501

        :param endpoint: The endpoint of this MFAChallengeMethodSpec.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and endpoint is None:  # noqa: E501
            raise ValueError("Invalid value for `endpoint`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                endpoint is not None and len(endpoint) > 511):
            raise ValueError("Invalid value for `endpoint`, length must be less than or equal to `511`")  # noqa: E501

        self._endpoint = endpoint

    @property
    def nickname(self):
        """Gets the nickname of this MFAChallengeMethodSpec.  # noqa: E501

        A descriptive name the user can set to differentiate their challenge methods.  # noqa: E501

        :return: The nickname of this MFAChallengeMethodSpec.  # noqa: E501
        :rtype: str
        """
        return self._nickname

    @nickname.setter
    def nickname(self, nickname):
        """Sets the nickname of this MFAChallengeMethodSpec.

        A descriptive name the user can set to differentiate their challenge methods.  # noqa: E501

        :param nickname: The nickname of this MFAChallengeMethodSpec.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                nickname is not None and len(nickname) > 100):
            raise ValueError("Invalid value for `nickname`, length must be less than or equal to `100`")  # noqa: E501

        self._nickname = nickname

    @property
    def enabled(self):
        """Gets the enabled of this MFAChallengeMethodSpec.  # noqa: E501

        The state of the challenge method. A value of true indicates that the method is active. A value of false indicates that the method is disabled. When a method is disabled it will not be used as an authentication factor when the user logs in.   # noqa: E501

        :return: The enabled of this MFAChallengeMethodSpec.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this MFAChallengeMethodSpec.

        The state of the challenge method. A value of true indicates that the method is active. A value of false indicates that the method is disabled. When a method is disabled it will not be used as an authentication factor when the user logs in.   # noqa: E501

        :param enabled: The enabled of this MFAChallengeMethodSpec.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MFAChallengeMethodSpec):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MFAChallengeMethodSpec):
            return True

        return self.to_dict() != other.to_dict()
