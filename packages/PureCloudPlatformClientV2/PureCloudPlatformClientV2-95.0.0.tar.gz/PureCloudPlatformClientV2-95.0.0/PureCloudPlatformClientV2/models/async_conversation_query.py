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

class AsyncConversationQuery(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        AsyncConversationQuery - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'interval': 'str',
            'conversation_filters': 'list[ConversationDetailQueryFilter]',
            'segment_filters': 'list[SegmentDetailQueryFilter]',
            'evaluation_filters': 'list[EvaluationDetailQueryFilter]',
            'media_endpoint_stat_filters': 'list[MediaEndpointStatDetailQueryFilter]',
            'survey_filters': 'list[SurveyDetailQueryFilter]',
            'order': 'str',
            'order_by': 'str',
            'limit': 'int',
            'start_of_day_interval_matching': 'bool'
        }

        self.attribute_map = {
            'interval': 'interval',
            'conversation_filters': 'conversationFilters',
            'segment_filters': 'segmentFilters',
            'evaluation_filters': 'evaluationFilters',
            'media_endpoint_stat_filters': 'mediaEndpointStatFilters',
            'survey_filters': 'surveyFilters',
            'order': 'order',
            'order_by': 'orderBy',
            'limit': 'limit',
            'start_of_day_interval_matching': 'startOfDayIntervalMatching'
        }

        self._interval = None
        self._conversation_filters = None
        self._segment_filters = None
        self._evaluation_filters = None
        self._media_endpoint_stat_filters = None
        self._survey_filters = None
        self._order = None
        self._order_by = None
        self._limit = None
        self._start_of_day_interval_matching = None

    @property
    def interval(self):
        """
        Gets the interval of this AsyncConversationQuery.
        Specifies the date and time range of data being queried. Results will include conversations that both started on a day touched by the interval AND either started, ended, or any activity during the interval. Intervals are represented as an ISO-8601 string. For example: YYYY-MM-DDThh:mm:ss/YYYY-MM-DDThh:mm:ss

        :return: The interval of this AsyncConversationQuery.
        :rtype: str
        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        """
        Sets the interval of this AsyncConversationQuery.
        Specifies the date and time range of data being queried. Results will include conversations that both started on a day touched by the interval AND either started, ended, or any activity during the interval. Intervals are represented as an ISO-8601 string. For example: YYYY-MM-DDThh:mm:ss/YYYY-MM-DDThh:mm:ss

        :param interval: The interval of this AsyncConversationQuery.
        :type: str
        """
        
        self._interval = interval

    @property
    def conversation_filters(self):
        """
        Gets the conversation_filters of this AsyncConversationQuery.
        Filters that target conversation-level data

        :return: The conversation_filters of this AsyncConversationQuery.
        :rtype: list[ConversationDetailQueryFilter]
        """
        return self._conversation_filters

    @conversation_filters.setter
    def conversation_filters(self, conversation_filters):
        """
        Sets the conversation_filters of this AsyncConversationQuery.
        Filters that target conversation-level data

        :param conversation_filters: The conversation_filters of this AsyncConversationQuery.
        :type: list[ConversationDetailQueryFilter]
        """
        
        self._conversation_filters = conversation_filters

    @property
    def segment_filters(self):
        """
        Gets the segment_filters of this AsyncConversationQuery.
        Filters that target individual segments within a conversation

        :return: The segment_filters of this AsyncConversationQuery.
        :rtype: list[SegmentDetailQueryFilter]
        """
        return self._segment_filters

    @segment_filters.setter
    def segment_filters(self, segment_filters):
        """
        Sets the segment_filters of this AsyncConversationQuery.
        Filters that target individual segments within a conversation

        :param segment_filters: The segment_filters of this AsyncConversationQuery.
        :type: list[SegmentDetailQueryFilter]
        """
        
        self._segment_filters = segment_filters

    @property
    def evaluation_filters(self):
        """
        Gets the evaluation_filters of this AsyncConversationQuery.
        Filters that target evaluations

        :return: The evaluation_filters of this AsyncConversationQuery.
        :rtype: list[EvaluationDetailQueryFilter]
        """
        return self._evaluation_filters

    @evaluation_filters.setter
    def evaluation_filters(self, evaluation_filters):
        """
        Sets the evaluation_filters of this AsyncConversationQuery.
        Filters that target evaluations

        :param evaluation_filters: The evaluation_filters of this AsyncConversationQuery.
        :type: list[EvaluationDetailQueryFilter]
        """
        
        self._evaluation_filters = evaluation_filters

    @property
    def media_endpoint_stat_filters(self):
        """
        Gets the media_endpoint_stat_filters of this AsyncConversationQuery.
        Filters that target mediaEndpointStats

        :return: The media_endpoint_stat_filters of this AsyncConversationQuery.
        :rtype: list[MediaEndpointStatDetailQueryFilter]
        """
        return self._media_endpoint_stat_filters

    @media_endpoint_stat_filters.setter
    def media_endpoint_stat_filters(self, media_endpoint_stat_filters):
        """
        Sets the media_endpoint_stat_filters of this AsyncConversationQuery.
        Filters that target mediaEndpointStats

        :param media_endpoint_stat_filters: The media_endpoint_stat_filters of this AsyncConversationQuery.
        :type: list[MediaEndpointStatDetailQueryFilter]
        """
        
        self._media_endpoint_stat_filters = media_endpoint_stat_filters

    @property
    def survey_filters(self):
        """
        Gets the survey_filters of this AsyncConversationQuery.
        Filters that target surveys

        :return: The survey_filters of this AsyncConversationQuery.
        :rtype: list[SurveyDetailQueryFilter]
        """
        return self._survey_filters

    @survey_filters.setter
    def survey_filters(self, survey_filters):
        """
        Sets the survey_filters of this AsyncConversationQuery.
        Filters that target surveys

        :param survey_filters: The survey_filters of this AsyncConversationQuery.
        :type: list[SurveyDetailQueryFilter]
        """
        
        self._survey_filters = survey_filters

    @property
    def order(self):
        """
        Gets the order of this AsyncConversationQuery.
        Sort the result set in ascending/descending order. Default is ascending

        :return: The order of this AsyncConversationQuery.
        :rtype: str
        """
        return self._order

    @order.setter
    def order(self, order):
        """
        Sets the order of this AsyncConversationQuery.
        Sort the result set in ascending/descending order. Default is ascending

        :param order: The order of this AsyncConversationQuery.
        :type: str
        """
        allowed_values = ["asc", "desc"]
        if order.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for order -> " + order
            self._order = "outdated_sdk_version"
        else:
            self._order = order

    @property
    def order_by(self):
        """
        Gets the order_by of this AsyncConversationQuery.
        Specify which data element within the result set to use for sorting. The options  to use as a basis for sorting the results: conversationStart, segmentStart, and segmentEnd. If not specified, the default is conversationStart

        :return: The order_by of this AsyncConversationQuery.
        :rtype: str
        """
        return self._order_by

    @order_by.setter
    def order_by(self, order_by):
        """
        Sets the order_by of this AsyncConversationQuery.
        Specify which data element within the result set to use for sorting. The options  to use as a basis for sorting the results: conversationStart, segmentStart, and segmentEnd. If not specified, the default is conversationStart

        :param order_by: The order_by of this AsyncConversationQuery.
        :type: str
        """
        allowed_values = ["conversationStart", "conversationEnd", "segmentStart", "segmentEnd"]
        if order_by.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for order_by -> " + order_by
            self._order_by = "outdated_sdk_version"
        else:
            self._order_by = order_by

    @property
    def limit(self):
        """
        Gets the limit of this AsyncConversationQuery.
        Specify number of results to be returned

        :return: The limit of this AsyncConversationQuery.
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """
        Sets the limit of this AsyncConversationQuery.
        Specify number of results to be returned

        :param limit: The limit of this AsyncConversationQuery.
        :type: int
        """
        
        self._limit = limit

    @property
    def start_of_day_interval_matching(self):
        """
        Gets the start_of_day_interval_matching of this AsyncConversationQuery.
        Add a filter to only include conversations that started after the beginning of the interval start date (UTC)

        :return: The start_of_day_interval_matching of this AsyncConversationQuery.
        :rtype: bool
        """
        return self._start_of_day_interval_matching

    @start_of_day_interval_matching.setter
    def start_of_day_interval_matching(self, start_of_day_interval_matching):
        """
        Sets the start_of_day_interval_matching of this AsyncConversationQuery.
        Add a filter to only include conversations that started after the beginning of the interval start date (UTC)

        :param start_of_day_interval_matching: The start_of_day_interval_matching of this AsyncConversationQuery.
        :type: bool
        """
        
        self._start_of_day_interval_matching = start_of_day_interval_matching

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

