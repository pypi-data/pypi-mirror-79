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

class Flow(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Flow - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'division': 'WritableDivision',
            'description': 'str',
            'type': 'str',
            'locked_user': 'User',
            'locked_client': 'DomainEntityRef',
            'active': 'bool',
            'system': 'bool',
            'deleted': 'bool',
            'published_version': 'FlowVersion',
            'saved_version': 'FlowVersion',
            'input_schema': 'object',
            'output_schema': 'object',
            'checked_in_version': 'FlowVersion',
            'debug_version': 'FlowVersion',
            'published_by': 'User',
            'current_operation': 'Operation',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'division': 'division',
            'description': 'description',
            'type': 'type',
            'locked_user': 'lockedUser',
            'locked_client': 'lockedClient',
            'active': 'active',
            'system': 'system',
            'deleted': 'deleted',
            'published_version': 'publishedVersion',
            'saved_version': 'savedVersion',
            'input_schema': 'inputSchema',
            'output_schema': 'outputSchema',
            'checked_in_version': 'checkedInVersion',
            'debug_version': 'debugVersion',
            'published_by': 'publishedBy',
            'current_operation': 'currentOperation',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._division = None
        self._description = None
        self._type = None
        self._locked_user = None
        self._locked_client = None
        self._active = None
        self._system = None
        self._deleted = None
        self._published_version = None
        self._saved_version = None
        self._input_schema = None
        self._output_schema = None
        self._checked_in_version = None
        self._debug_version = None
        self._published_by = None
        self._current_operation = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this Flow.
        The flow identifier

        :return: The id of this Flow.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Flow.
        The flow identifier

        :param id: The id of this Flow.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this Flow.
        The flow name

        :return: The name of this Flow.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Flow.
        The flow name

        :param name: The name of this Flow.
        :type: str
        """
        
        self._name = name

    @property
    def division(self):
        """
        Gets the division of this Flow.
        The division to which this entity belongs.

        :return: The division of this Flow.
        :rtype: WritableDivision
        """
        return self._division

    @division.setter
    def division(self, division):
        """
        Sets the division of this Flow.
        The division to which this entity belongs.

        :param division: The division of this Flow.
        :type: WritableDivision
        """
        
        self._division = division

    @property
    def description(self):
        """
        Gets the description of this Flow.


        :return: The description of this Flow.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this Flow.


        :param description: The description of this Flow.
        :type: str
        """
        
        self._description = description

    @property
    def type(self):
        """
        Gets the type of this Flow.


        :return: The type of this Flow.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this Flow.


        :param type: The type of this Flow.
        :type: str
        """
        allowed_values = ["BOT", "COMMONMODULE", "INBOUNDCALL", "INBOUNDCHAT", "INBOUNDEMAIL", "INBOUNDSHORTMESSAGE", "INQUEUECALL", "OUTBOUNDCALL", "SECURECALL", "SPEECH", "SURVEYINVITE", "WORKFLOW"]
        if type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for type -> " + type
            self._type = "outdated_sdk_version"
        else:
            self._type = type

    @property
    def locked_user(self):
        """
        Gets the locked_user of this Flow.
        User that has the flow locked.

        :return: The locked_user of this Flow.
        :rtype: User
        """
        return self._locked_user

    @locked_user.setter
    def locked_user(self, locked_user):
        """
        Sets the locked_user of this Flow.
        User that has the flow locked.

        :param locked_user: The locked_user of this Flow.
        :type: User
        """
        
        self._locked_user = locked_user

    @property
    def locked_client(self):
        """
        Gets the locked_client of this Flow.
        OAuth client that has the flow locked.

        :return: The locked_client of this Flow.
        :rtype: DomainEntityRef
        """
        return self._locked_client

    @locked_client.setter
    def locked_client(self, locked_client):
        """
        Sets the locked_client of this Flow.
        OAuth client that has the flow locked.

        :param locked_client: The locked_client of this Flow.
        :type: DomainEntityRef
        """
        
        self._locked_client = locked_client

    @property
    def active(self):
        """
        Gets the active of this Flow.


        :return: The active of this Flow.
        :rtype: bool
        """
        return self._active

    @active.setter
    def active(self, active):
        """
        Sets the active of this Flow.


        :param active: The active of this Flow.
        :type: bool
        """
        
        self._active = active

    @property
    def system(self):
        """
        Gets the system of this Flow.


        :return: The system of this Flow.
        :rtype: bool
        """
        return self._system

    @system.setter
    def system(self, system):
        """
        Sets the system of this Flow.


        :param system: The system of this Flow.
        :type: bool
        """
        
        self._system = system

    @property
    def deleted(self):
        """
        Gets the deleted of this Flow.


        :return: The deleted of this Flow.
        :rtype: bool
        """
        return self._deleted

    @deleted.setter
    def deleted(self, deleted):
        """
        Sets the deleted of this Flow.


        :param deleted: The deleted of this Flow.
        :type: bool
        """
        
        self._deleted = deleted

    @property
    def published_version(self):
        """
        Gets the published_version of this Flow.


        :return: The published_version of this Flow.
        :rtype: FlowVersion
        """
        return self._published_version

    @published_version.setter
    def published_version(self, published_version):
        """
        Sets the published_version of this Flow.


        :param published_version: The published_version of this Flow.
        :type: FlowVersion
        """
        
        self._published_version = published_version

    @property
    def saved_version(self):
        """
        Gets the saved_version of this Flow.


        :return: The saved_version of this Flow.
        :rtype: FlowVersion
        """
        return self._saved_version

    @saved_version.setter
    def saved_version(self, saved_version):
        """
        Sets the saved_version of this Flow.


        :param saved_version: The saved_version of this Flow.
        :type: FlowVersion
        """
        
        self._saved_version = saved_version

    @property
    def input_schema(self):
        """
        Gets the input_schema of this Flow.
        json schema describing the inputs for the flow

        :return: The input_schema of this Flow.
        :rtype: object
        """
        return self._input_schema

    @input_schema.setter
    def input_schema(self, input_schema):
        """
        Sets the input_schema of this Flow.
        json schema describing the inputs for the flow

        :param input_schema: The input_schema of this Flow.
        :type: object
        """
        
        self._input_schema = input_schema

    @property
    def output_schema(self):
        """
        Gets the output_schema of this Flow.
        json schema describing the outputs for the flow

        :return: The output_schema of this Flow.
        :rtype: object
        """
        return self._output_schema

    @output_schema.setter
    def output_schema(self, output_schema):
        """
        Sets the output_schema of this Flow.
        json schema describing the outputs for the flow

        :param output_schema: The output_schema of this Flow.
        :type: object
        """
        
        self._output_schema = output_schema

    @property
    def checked_in_version(self):
        """
        Gets the checked_in_version of this Flow.


        :return: The checked_in_version of this Flow.
        :rtype: FlowVersion
        """
        return self._checked_in_version

    @checked_in_version.setter
    def checked_in_version(self, checked_in_version):
        """
        Sets the checked_in_version of this Flow.


        :param checked_in_version: The checked_in_version of this Flow.
        :type: FlowVersion
        """
        
        self._checked_in_version = checked_in_version

    @property
    def debug_version(self):
        """
        Gets the debug_version of this Flow.


        :return: The debug_version of this Flow.
        :rtype: FlowVersion
        """
        return self._debug_version

    @debug_version.setter
    def debug_version(self, debug_version):
        """
        Sets the debug_version of this Flow.


        :param debug_version: The debug_version of this Flow.
        :type: FlowVersion
        """
        
        self._debug_version = debug_version

    @property
    def published_by(self):
        """
        Gets the published_by of this Flow.


        :return: The published_by of this Flow.
        :rtype: User
        """
        return self._published_by

    @published_by.setter
    def published_by(self, published_by):
        """
        Sets the published_by of this Flow.


        :param published_by: The published_by of this Flow.
        :type: User
        """
        
        self._published_by = published_by

    @property
    def current_operation(self):
        """
        Gets the current_operation of this Flow.


        :return: The current_operation of this Flow.
        :rtype: Operation
        """
        return self._current_operation

    @current_operation.setter
    def current_operation(self, current_operation):
        """
        Sets the current_operation of this Flow.


        :param current_operation: The current_operation of this Flow.
        :type: Operation
        """
        
        self._current_operation = current_operation

    @property
    def self_uri(self):
        """
        Gets the self_uri of this Flow.
        The URI for this object

        :return: The self_uri of this Flow.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this Flow.
        The URI for this object

        :param self_uri: The self_uri of this Flow.
        :type: str
        """
        
        self._self_uri = self_uri

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

