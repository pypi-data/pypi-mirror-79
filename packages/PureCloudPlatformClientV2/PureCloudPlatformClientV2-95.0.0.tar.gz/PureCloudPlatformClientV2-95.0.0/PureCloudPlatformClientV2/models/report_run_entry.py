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

class ReportRunEntry(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ReportRunEntry - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'report_id': 'str',
            'run_time': 'datetime',
            'run_status': 'str',
            'error_message': 'str',
            'run_duration_msec': 'int',
            'report_url': 'str',
            'report_format': 'str',
            'schedule_uri': 'str',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'report_id': 'reportId',
            'run_time': 'runTime',
            'run_status': 'runStatus',
            'error_message': 'errorMessage',
            'run_duration_msec': 'runDurationMsec',
            'report_url': 'reportUrl',
            'report_format': 'reportFormat',
            'schedule_uri': 'scheduleUri',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._report_id = None
        self._run_time = None
        self._run_status = None
        self._error_message = None
        self._run_duration_msec = None
        self._report_url = None
        self._report_format = None
        self._schedule_uri = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this ReportRunEntry.
        The globally unique identifier for the object.

        :return: The id of this ReportRunEntry.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ReportRunEntry.
        The globally unique identifier for the object.

        :param id: The id of this ReportRunEntry.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this ReportRunEntry.


        :return: The name of this ReportRunEntry.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ReportRunEntry.


        :param name: The name of this ReportRunEntry.
        :type: str
        """
        
        self._name = name

    @property
    def report_id(self):
        """
        Gets the report_id of this ReportRunEntry.


        :return: The report_id of this ReportRunEntry.
        :rtype: str
        """
        return self._report_id

    @report_id.setter
    def report_id(self, report_id):
        """
        Sets the report_id of this ReportRunEntry.


        :param report_id: The report_id of this ReportRunEntry.
        :type: str
        """
        
        self._report_id = report_id

    @property
    def run_time(self):
        """
        Gets the run_time of this ReportRunEntry.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The run_time of this ReportRunEntry.
        :rtype: datetime
        """
        return self._run_time

    @run_time.setter
    def run_time(self, run_time):
        """
        Sets the run_time of this ReportRunEntry.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param run_time: The run_time of this ReportRunEntry.
        :type: datetime
        """
        
        self._run_time = run_time

    @property
    def run_status(self):
        """
        Gets the run_status of this ReportRunEntry.


        :return: The run_status of this ReportRunEntry.
        :rtype: str
        """
        return self._run_status

    @run_status.setter
    def run_status(self, run_status):
        """
        Sets the run_status of this ReportRunEntry.


        :param run_status: The run_status of this ReportRunEntry.
        :type: str
        """
        allowed_values = ["RUNNING", "COMPLETED", "COMPLETED_WITH_ERRORS", "FAILED", "FAILED_TIMEOUT", "FAILED_DATALIMIT", "UNABLE_TO_COMPLETE"]
        if run_status.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for run_status -> " + run_status
            self._run_status = "outdated_sdk_version"
        else:
            self._run_status = run_status

    @property
    def error_message(self):
        """
        Gets the error_message of this ReportRunEntry.


        :return: The error_message of this ReportRunEntry.
        :rtype: str
        """
        return self._error_message

    @error_message.setter
    def error_message(self, error_message):
        """
        Sets the error_message of this ReportRunEntry.


        :param error_message: The error_message of this ReportRunEntry.
        :type: str
        """
        
        self._error_message = error_message

    @property
    def run_duration_msec(self):
        """
        Gets the run_duration_msec of this ReportRunEntry.


        :return: The run_duration_msec of this ReportRunEntry.
        :rtype: int
        """
        return self._run_duration_msec

    @run_duration_msec.setter
    def run_duration_msec(self, run_duration_msec):
        """
        Sets the run_duration_msec of this ReportRunEntry.


        :param run_duration_msec: The run_duration_msec of this ReportRunEntry.
        :type: int
        """
        
        self._run_duration_msec = run_duration_msec

    @property
    def report_url(self):
        """
        Gets the report_url of this ReportRunEntry.


        :return: The report_url of this ReportRunEntry.
        :rtype: str
        """
        return self._report_url

    @report_url.setter
    def report_url(self, report_url):
        """
        Sets the report_url of this ReportRunEntry.


        :param report_url: The report_url of this ReportRunEntry.
        :type: str
        """
        
        self._report_url = report_url

    @property
    def report_format(self):
        """
        Gets the report_format of this ReportRunEntry.


        :return: The report_format of this ReportRunEntry.
        :rtype: str
        """
        return self._report_format

    @report_format.setter
    def report_format(self, report_format):
        """
        Sets the report_format of this ReportRunEntry.


        :param report_format: The report_format of this ReportRunEntry.
        :type: str
        """
        
        self._report_format = report_format

    @property
    def schedule_uri(self):
        """
        Gets the schedule_uri of this ReportRunEntry.


        :return: The schedule_uri of this ReportRunEntry.
        :rtype: str
        """
        return self._schedule_uri

    @schedule_uri.setter
    def schedule_uri(self, schedule_uri):
        """
        Sets the schedule_uri of this ReportRunEntry.


        :param schedule_uri: The schedule_uri of this ReportRunEntry.
        :type: str
        """
        
        self._schedule_uri = schedule_uri

    @property
    def self_uri(self):
        """
        Gets the self_uri of this ReportRunEntry.
        The URI for this object

        :return: The self_uri of this ReportRunEntry.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this ReportRunEntry.
        The URI for this object

        :param self_uri: The self_uri of this ReportRunEntry.
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

