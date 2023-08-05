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

class PostTextResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        PostTextResponse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'bot_state': 'str',
            'reply_messages': 'list[PostTextMessage]',
            'intent_name': 'str',
            'slots': 'dict(str, str)',
            'bot_correlation_id': 'str',
            'amazon_lex': 'dict(str, object)',
            'google_dialog_flow': 'dict(str, object)',
            'genesys_dialog_engine': 'dict(str, object)'
        }

        self.attribute_map = {
            'bot_state': 'botState',
            'reply_messages': 'replyMessages',
            'intent_name': 'intentName',
            'slots': 'slots',
            'bot_correlation_id': 'botCorrelationId',
            'amazon_lex': 'amazonLex',
            'google_dialog_flow': 'googleDialogFlow',
            'genesys_dialog_engine': 'genesysDialogEngine'
        }

        self._bot_state = None
        self._reply_messages = None
        self._intent_name = None
        self._slots = None
        self._bot_correlation_id = None
        self._amazon_lex = None
        self._google_dialog_flow = None
        self._genesys_dialog_engine = None

    @property
    def bot_state(self):
        """
        Gets the bot_state of this PostTextResponse.
        The state of the bot after completion of the request

        :return: The bot_state of this PostTextResponse.
        :rtype: str
        """
        return self._bot_state

    @bot_state.setter
    def bot_state(self, bot_state):
        """
        Sets the bot_state of this PostTextResponse.
        The state of the bot after completion of the request

        :param bot_state: The bot_state of this PostTextResponse.
        :type: str
        """
        allowed_values = ["Complete", "Failed", "MoreData"]
        if bot_state.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for bot_state -> " + bot_state
            self._bot_state = "outdated_sdk_version"
        else:
            self._bot_state = bot_state

    @property
    def reply_messages(self):
        """
        Gets the reply_messages of this PostTextResponse.
        The list of messages to respond with, if any

        :return: The reply_messages of this PostTextResponse.
        :rtype: list[PostTextMessage]
        """
        return self._reply_messages

    @reply_messages.setter
    def reply_messages(self, reply_messages):
        """
        Sets the reply_messages of this PostTextResponse.
        The list of messages to respond with, if any

        :param reply_messages: The reply_messages of this PostTextResponse.
        :type: list[PostTextMessage]
        """
        
        self._reply_messages = reply_messages

    @property
    def intent_name(self):
        """
        Gets the intent_name of this PostTextResponse.
        The name of the intent the bot is either processing or has processed, this will be blank if no intent could be detected.

        :return: The intent_name of this PostTextResponse.
        :rtype: str
        """
        return self._intent_name

    @intent_name.setter
    def intent_name(self, intent_name):
        """
        Sets the intent_name of this PostTextResponse.
        The name of the intent the bot is either processing or has processed, this will be blank if no intent could be detected.

        :param intent_name: The intent_name of this PostTextResponse.
        :type: str
        """
        
        self._intent_name = intent_name

    @property
    def slots(self):
        """
        Gets the slots of this PostTextResponse.
        Data parameters detected and filled by the bot.

        :return: The slots of this PostTextResponse.
        :rtype: dict(str, str)
        """
        return self._slots

    @slots.setter
    def slots(self, slots):
        """
        Sets the slots of this PostTextResponse.
        Data parameters detected and filled by the bot.

        :param slots: The slots of this PostTextResponse.
        :type: dict(str, str)
        """
        
        self._slots = slots

    @property
    def bot_correlation_id(self):
        """
        Gets the bot_correlation_id of this PostTextResponse.
        The optional ID specified in the request

        :return: The bot_correlation_id of this PostTextResponse.
        :rtype: str
        """
        return self._bot_correlation_id

    @bot_correlation_id.setter
    def bot_correlation_id(self, bot_correlation_id):
        """
        Sets the bot_correlation_id of this PostTextResponse.
        The optional ID specified in the request

        :param bot_correlation_id: The bot_correlation_id of this PostTextResponse.
        :type: str
        """
        
        self._bot_correlation_id = bot_correlation_id

    @property
    def amazon_lex(self):
        """
        Gets the amazon_lex of this PostTextResponse.
        Raw data response from AWS (if called)

        :return: The amazon_lex of this PostTextResponse.
        :rtype: dict(str, object)
        """
        return self._amazon_lex

    @amazon_lex.setter
    def amazon_lex(self, amazon_lex):
        """
        Sets the amazon_lex of this PostTextResponse.
        Raw data response from AWS (if called)

        :param amazon_lex: The amazon_lex of this PostTextResponse.
        :type: dict(str, object)
        """
        
        self._amazon_lex = amazon_lex

    @property
    def google_dialog_flow(self):
        """
        Gets the google_dialog_flow of this PostTextResponse.
        Raw data response from Google Dialogflow (if called)

        :return: The google_dialog_flow of this PostTextResponse.
        :rtype: dict(str, object)
        """
        return self._google_dialog_flow

    @google_dialog_flow.setter
    def google_dialog_flow(self, google_dialog_flow):
        """
        Sets the google_dialog_flow of this PostTextResponse.
        Raw data response from Google Dialogflow (if called)

        :param google_dialog_flow: The google_dialog_flow of this PostTextResponse.
        :type: dict(str, object)
        """
        
        self._google_dialog_flow = google_dialog_flow

    @property
    def genesys_dialog_engine(self):
        """
        Gets the genesys_dialog_engine of this PostTextResponse.
        Raw data response from Genesys' Dialogengine (if called)

        :return: The genesys_dialog_engine of this PostTextResponse.
        :rtype: dict(str, object)
        """
        return self._genesys_dialog_engine

    @genesys_dialog_engine.setter
    def genesys_dialog_engine(self, genesys_dialog_engine):
        """
        Sets the genesys_dialog_engine of this PostTextResponse.
        Raw data response from Genesys' Dialogengine (if called)

        :param genesys_dialog_engine: The genesys_dialog_engine of this PostTextResponse.
        :type: dict(str, object)
        """
        
        self._genesys_dialog_engine = genesys_dialog_engine

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

