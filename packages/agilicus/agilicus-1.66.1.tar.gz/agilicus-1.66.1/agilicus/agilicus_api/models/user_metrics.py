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


class UserMetrics(object):
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
        'email': 'str',
        'count': 'int',
        'user_id': 'str'
    }

    attribute_map = {
        'email': 'email',
        'count': 'count',
        'user_id': 'user_id'
    }

    def __init__(self, email=None, count=None, user_id=None, local_vars_configuration=None):  # noqa: E501
        """UserMetrics - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._email = None
        self._count = None
        self._user_id = None
        self.discriminator = None

        if email is not None:
            self.email = email
        if count is not None:
            self.count = count
        if user_id is not None:
            self.user_id = user_id

    @property
    def email(self):
        """Gets the email of this UserMetrics.  # noqa: E501

        User's email-address; Is an empty string if no email is found in the user id lookup  # noqa: E501

        :return: The email of this UserMetrics.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this UserMetrics.

        User's email-address; Is an empty string if no email is found in the user id lookup  # noqa: E501

        :param email: The email of this UserMetrics.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                email is not None and len(email) > 100):
            raise ValueError("Invalid value for `email`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                email is not None and len(email) < 0):
            raise ValueError("Invalid value for `email`, length must be greater than or equal to `0`")  # noqa: E501

        self._email = email

    @property
    def count(self):
        """Gets the count of this UserMetrics.  # noqa: E501

        Number of intervals for which the user was active  # noqa: E501

        :return: The count of this UserMetrics.  # noqa: E501
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this UserMetrics.

        Number of intervals for which the user was active  # noqa: E501

        :param count: The count of this UserMetrics.  # noqa: E501
        :type: int
        """

        self._count = count

    @property
    def user_id(self):
        """Gets the user_id of this UserMetrics.  # noqa: E501

        Identifier for the active user  # noqa: E501

        :return: The user_id of this UserMetrics.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this UserMetrics.

        Identifier for the active user  # noqa: E501

        :param user_id: The user_id of this UserMetrics.  # noqa: E501
        :type: str
        """

        self._user_id = user_id

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
        if not isinstance(other, UserMetrics):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UserMetrics):
            return True

        return self.to_dict() != other.to_dict()
