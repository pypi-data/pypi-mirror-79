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

class ContactList(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ContactList - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'date_created': 'datetime',
            'date_modified': 'datetime',
            'version': 'int',
            'division': 'DomainEntityRef',
            'column_names': 'list[str]',
            'phone_columns': 'list[ContactPhoneNumberColumn]',
            'import_status': 'ImportStatus',
            'preview_mode_column_name': 'str',
            'preview_mode_accepted_values': 'list[str]',
            'size': 'int',
            'attempt_limits': 'DomainEntityRef',
            'automatic_time_zone_mapping': 'bool',
            'zip_code_column_name': 'str',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'date_created': 'dateCreated',
            'date_modified': 'dateModified',
            'version': 'version',
            'division': 'division',
            'column_names': 'columnNames',
            'phone_columns': 'phoneColumns',
            'import_status': 'importStatus',
            'preview_mode_column_name': 'previewModeColumnName',
            'preview_mode_accepted_values': 'previewModeAcceptedValues',
            'size': 'size',
            'attempt_limits': 'attemptLimits',
            'automatic_time_zone_mapping': 'automaticTimeZoneMapping',
            'zip_code_column_name': 'zipCodeColumnName',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._date_created = None
        self._date_modified = None
        self._version = None
        self._division = None
        self._column_names = None
        self._phone_columns = None
        self._import_status = None
        self._preview_mode_column_name = None
        self._preview_mode_accepted_values = None
        self._size = None
        self._attempt_limits = None
        self._automatic_time_zone_mapping = None
        self._zip_code_column_name = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this ContactList.
        The globally unique identifier for the object.

        :return: The id of this ContactList.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ContactList.
        The globally unique identifier for the object.

        :param id: The id of this ContactList.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this ContactList.


        :return: The name of this ContactList.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ContactList.


        :param name: The name of this ContactList.
        :type: str
        """
        
        self._name = name

    @property
    def date_created(self):
        """
        Gets the date_created of this ContactList.
        Creation time of the entity. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_created of this ContactList.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this ContactList.
        Creation time of the entity. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_created: The date_created of this ContactList.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def date_modified(self):
        """
        Gets the date_modified of this ContactList.
        Last modified time of the entity. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_modified of this ContactList.
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """
        Sets the date_modified of this ContactList.
        Last modified time of the entity. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_modified: The date_modified of this ContactList.
        :type: datetime
        """
        
        self._date_modified = date_modified

    @property
    def version(self):
        """
        Gets the version of this ContactList.
        Required for updates, must match the version number of the most recent update

        :return: The version of this ContactList.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this ContactList.
        Required for updates, must match the version number of the most recent update

        :param version: The version of this ContactList.
        :type: int
        """
        
        self._version = version

    @property
    def division(self):
        """
        Gets the division of this ContactList.
        The division this entity belongs to.

        :return: The division of this ContactList.
        :rtype: DomainEntityRef
        """
        return self._division

    @division.setter
    def division(self, division):
        """
        Sets the division of this ContactList.
        The division this entity belongs to.

        :param division: The division of this ContactList.
        :type: DomainEntityRef
        """
        
        self._division = division

    @property
    def column_names(self):
        """
        Gets the column_names of this ContactList.
        The names of the contact data columns.

        :return: The column_names of this ContactList.
        :rtype: list[str]
        """
        return self._column_names

    @column_names.setter
    def column_names(self, column_names):
        """
        Sets the column_names of this ContactList.
        The names of the contact data columns.

        :param column_names: The column_names of this ContactList.
        :type: list[str]
        """
        
        self._column_names = column_names

    @property
    def phone_columns(self):
        """
        Gets the phone_columns of this ContactList.
        Indicates which columns are phone numbers.

        :return: The phone_columns of this ContactList.
        :rtype: list[ContactPhoneNumberColumn]
        """
        return self._phone_columns

    @phone_columns.setter
    def phone_columns(self, phone_columns):
        """
        Sets the phone_columns of this ContactList.
        Indicates which columns are phone numbers.

        :param phone_columns: The phone_columns of this ContactList.
        :type: list[ContactPhoneNumberColumn]
        """
        
        self._phone_columns = phone_columns

    @property
    def import_status(self):
        """
        Gets the import_status of this ContactList.
        The status of the import process.

        :return: The import_status of this ContactList.
        :rtype: ImportStatus
        """
        return self._import_status

    @import_status.setter
    def import_status(self, import_status):
        """
        Sets the import_status of this ContactList.
        The status of the import process.

        :param import_status: The import_status of this ContactList.
        :type: ImportStatus
        """
        
        self._import_status = import_status

    @property
    def preview_mode_column_name(self):
        """
        Gets the preview_mode_column_name of this ContactList.
        A column to check if a contact should always be dialed in preview mode.

        :return: The preview_mode_column_name of this ContactList.
        :rtype: str
        """
        return self._preview_mode_column_name

    @preview_mode_column_name.setter
    def preview_mode_column_name(self, preview_mode_column_name):
        """
        Sets the preview_mode_column_name of this ContactList.
        A column to check if a contact should always be dialed in preview mode.

        :param preview_mode_column_name: The preview_mode_column_name of this ContactList.
        :type: str
        """
        
        self._preview_mode_column_name = preview_mode_column_name

    @property
    def preview_mode_accepted_values(self):
        """
        Gets the preview_mode_accepted_values of this ContactList.
        The values in the previewModeColumnName column that indicate a contact should always be dialed in preview mode.

        :return: The preview_mode_accepted_values of this ContactList.
        :rtype: list[str]
        """
        return self._preview_mode_accepted_values

    @preview_mode_accepted_values.setter
    def preview_mode_accepted_values(self, preview_mode_accepted_values):
        """
        Sets the preview_mode_accepted_values of this ContactList.
        The values in the previewModeColumnName column that indicate a contact should always be dialed in preview mode.

        :param preview_mode_accepted_values: The preview_mode_accepted_values of this ContactList.
        :type: list[str]
        """
        
        self._preview_mode_accepted_values = preview_mode_accepted_values

    @property
    def size(self):
        """
        Gets the size of this ContactList.
        The number of contacts in the ContactList.

        :return: The size of this ContactList.
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """
        Sets the size of this ContactList.
        The number of contacts in the ContactList.

        :param size: The size of this ContactList.
        :type: int
        """
        
        self._size = size

    @property
    def attempt_limits(self):
        """
        Gets the attempt_limits of this ContactList.
        AttemptLimits for this ContactList.

        :return: The attempt_limits of this ContactList.
        :rtype: DomainEntityRef
        """
        return self._attempt_limits

    @attempt_limits.setter
    def attempt_limits(self, attempt_limits):
        """
        Sets the attempt_limits of this ContactList.
        AttemptLimits for this ContactList.

        :param attempt_limits: The attempt_limits of this ContactList.
        :type: DomainEntityRef
        """
        
        self._attempt_limits = attempt_limits

    @property
    def automatic_time_zone_mapping(self):
        """
        Gets the automatic_time_zone_mapping of this ContactList.
        Indicates if automatic time zone mapping is to be used for this ContactList.

        :return: The automatic_time_zone_mapping of this ContactList.
        :rtype: bool
        """
        return self._automatic_time_zone_mapping

    @automatic_time_zone_mapping.setter
    def automatic_time_zone_mapping(self, automatic_time_zone_mapping):
        """
        Sets the automatic_time_zone_mapping of this ContactList.
        Indicates if automatic time zone mapping is to be used for this ContactList.

        :param automatic_time_zone_mapping: The automatic_time_zone_mapping of this ContactList.
        :type: bool
        """
        
        self._automatic_time_zone_mapping = automatic_time_zone_mapping

    @property
    def zip_code_column_name(self):
        """
        Gets the zip_code_column_name of this ContactList.
        The name of contact list column containing the zip code for use with automatic time zone mapping. Only allowed if 'automaticTimeZoneMapping' is set to true.

        :return: The zip_code_column_name of this ContactList.
        :rtype: str
        """
        return self._zip_code_column_name

    @zip_code_column_name.setter
    def zip_code_column_name(self, zip_code_column_name):
        """
        Sets the zip_code_column_name of this ContactList.
        The name of contact list column containing the zip code for use with automatic time zone mapping. Only allowed if 'automaticTimeZoneMapping' is set to true.

        :param zip_code_column_name: The zip_code_column_name of this ContactList.
        :type: str
        """
        
        self._zip_code_column_name = zip_code_column_name

    @property
    def self_uri(self):
        """
        Gets the self_uri of this ContactList.
        The URI for this object

        :return: The self_uri of this ContactList.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this ContactList.
        The URI for this object

        :param self_uri: The self_uri of this ContactList.
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

