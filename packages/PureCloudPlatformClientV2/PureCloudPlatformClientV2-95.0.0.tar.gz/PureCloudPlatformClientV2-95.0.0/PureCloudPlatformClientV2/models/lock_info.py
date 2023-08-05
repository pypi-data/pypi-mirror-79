# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems
import re
import json

from ..utils import sanitize_for_serialization

class LockInfo(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        LockInfo - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'locked_by': 'DomainEntityRef',
            'date_created': 'datetime',
            'date_expires': 'datetime',
            'action': 'str'
        }

        self.attribute_map = {
            'locked_by': 'lockedBy',
            'date_created': 'dateCreated',
            'date_expires': 'dateExpires',
            'action': 'action'
        }

        self._locked_by = None
        self._date_created = None
        self._date_expires = None
        self._action = None

    @property
    def locked_by(self):
        """
        Gets the locked_by of this LockInfo.


        :return: The locked_by of this LockInfo.
        :rtype: DomainEntityRef
        """
        return self._locked_by

    @locked_by.setter
    def locked_by(self, locked_by):
        """
        Sets the locked_by of this LockInfo.


        :param locked_by: The locked_by of this LockInfo.
        :type: DomainEntityRef
        """
        
        self._locked_by = locked_by

    @property
    def date_created(self):
        """
        Gets the date_created of this LockInfo.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_created of this LockInfo.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this LockInfo.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_created: The date_created of this LockInfo.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def date_expires(self):
        """
        Gets the date_expires of this LockInfo.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_expires of this LockInfo.
        :rtype: datetime
        """
        return self._date_expires

    @date_expires.setter
    def date_expires(self, date_expires):
        """
        Sets the date_expires of this LockInfo.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_expires: The date_expires of this LockInfo.
        :type: datetime
        """
        
        self._date_expires = date_expires

    @property
    def action(self):
        """
        Gets the action of this LockInfo.


        :return: The action of this LockInfo.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """
        Sets the action of this LockInfo.


        :param action: The action of this LockInfo.
        :type: str
        """
        allowed_values = ["UPDATE", "DELETE", "COPY", "MOVE", "REPLACE", "THUMBNAIL", "TEXT_EXTRACTION"]
        if action.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for action -> " + action
            self._action = "outdated_sdk_version"
        else:
            self._action = action

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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

    def to_json(self):
        """
        Returns the model as raw JSON
        """
        return json.dumps(sanitize_for_serialization(self.to_dict()))

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

