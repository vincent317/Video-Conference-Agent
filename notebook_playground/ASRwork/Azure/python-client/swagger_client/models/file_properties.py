# coding: utf-8

"""
    Speech Services API v3.1

    Speech Services API v3.1.  # noqa: E501

    OpenAPI spec version: v3.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from swagger_client.configuration import Configuration


class FileProperties(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'size': 'int',
        'duration': 'str'
    }

    attribute_map = {
        'size': 'size',
        'duration': 'duration'
    }

    def __init__(self, size=None, duration=None, _configuration=None):  # noqa: E501
        """FileProperties - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._size = None
        self._duration = None
        self.discriminator = None

        if size is not None:
            self.size = size
        if duration is not None:
            self.duration = duration

    @property
    def size(self):
        """Gets the size of this FileProperties.  # noqa: E501

        The size of the data in bytes.  # noqa: E501

        :return: The size of this FileProperties.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this FileProperties.

        The size of the data in bytes.  # noqa: E501

        :param size: The size of this FileProperties.  # noqa: E501
        :type: int
        """

        self._size = size

    @property
    def duration(self):
        """Gets the duration of this FileProperties.  # noqa: E501

        The duration in case this file is an audio file. The duration is encoded as ISO 8601  duration (\"PnYnMnDTnHnMnS\", see https://en.wikipedia.org/wiki/ISO_8601#Durations).  # noqa: E501

        :return: The duration of this FileProperties.  # noqa: E501
        :rtype: str
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """Sets the duration of this FileProperties.

        The duration in case this file is an audio file. The duration is encoded as ISO 8601  duration (\"PnYnMnDTnHnMnS\", see https://en.wikipedia.org/wiki/ISO_8601#Durations).  # noqa: E501

        :param duration: The duration of this FileProperties.  # noqa: E501
        :type: str
        """

        self._duration = duration

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(FileProperties, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, FileProperties):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, FileProperties):
            return True

        return self.to_dict() != other.to_dict()
