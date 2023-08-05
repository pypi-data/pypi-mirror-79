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

class PostTextRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        PostTextRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'bot_id': 'str',
            'bot_alias': 'str',
            'integration_id': 'str',
            'bot_session_id': 'str',
            'post_text_message': 'PostTextMessage',
            'language_code': 'str',
            'bot_session_timeout_minutes': 'int',
            'bot_channels': 'list[str]',
            'bot_correlation_id': 'str',
            'amazon_lex_request': 'AmazonLexRequest',
            'google_dialogflow': 'GoogleDialogflowCustomSettings'
        }

        self.attribute_map = {
            'bot_id': 'botId',
            'bot_alias': 'botAlias',
            'integration_id': 'integrationId',
            'bot_session_id': 'botSessionId',
            'post_text_message': 'postTextMessage',
            'language_code': 'languageCode',
            'bot_session_timeout_minutes': 'botSessionTimeoutMinutes',
            'bot_channels': 'botChannels',
            'bot_correlation_id': 'botCorrelationId',
            'amazon_lex_request': 'amazonLexRequest',
            'google_dialogflow': 'googleDialogflow'
        }

        self._bot_id = None
        self._bot_alias = None
        self._integration_id = None
        self._bot_session_id = None
        self._post_text_message = None
        self._language_code = None
        self._bot_session_timeout_minutes = None
        self._bot_channels = None
        self._bot_correlation_id = None
        self._amazon_lex_request = None
        self._google_dialogflow = None

    @property
    def bot_id(self):
        """
        Gets the bot_id of this PostTextRequest.
        ID of the bot to send the text to.

        :return: The bot_id of this PostTextRequest.
        :rtype: str
        """
        return self._bot_id

    @bot_id.setter
    def bot_id(self, bot_id):
        """
        Sets the bot_id of this PostTextRequest.
        ID of the bot to send the text to.

        :param bot_id: The bot_id of this PostTextRequest.
        :type: str
        """
        
        self._bot_id = bot_id

    @property
    def bot_alias(self):
        """
        Gets the bot_alias of this PostTextRequest.
        Alias/Version of the bot

        :return: The bot_alias of this PostTextRequest.
        :rtype: str
        """
        return self._bot_alias

    @bot_alias.setter
    def bot_alias(self, bot_alias):
        """
        Sets the bot_alias of this PostTextRequest.
        Alias/Version of the bot

        :param bot_alias: The bot_alias of this PostTextRequest.
        :type: str
        """
        
        self._bot_alias = bot_alias

    @property
    def integration_id(self):
        """
        Gets the integration_id of this PostTextRequest.
        the integration service id for the bot's credentials

        :return: The integration_id of this PostTextRequest.
        :rtype: str
        """
        return self._integration_id

    @integration_id.setter
    def integration_id(self, integration_id):
        """
        Sets the integration_id of this PostTextRequest.
        the integration service id for the bot's credentials

        :param integration_id: The integration_id of this PostTextRequest.
        :type: str
        """
        
        self._integration_id = integration_id

    @property
    def bot_session_id(self):
        """
        Gets the bot_session_id of this PostTextRequest.
        GUID for this bot's session

        :return: The bot_session_id of this PostTextRequest.
        :rtype: str
        """
        return self._bot_session_id

    @bot_session_id.setter
    def bot_session_id(self, bot_session_id):
        """
        Sets the bot_session_id of this PostTextRequest.
        GUID for this bot's session

        :param bot_session_id: The bot_session_id of this PostTextRequest.
        :type: str
        """
        
        self._bot_session_id = bot_session_id

    @property
    def post_text_message(self):
        """
        Gets the post_text_message of this PostTextRequest.
        Message to send to the bot

        :return: The post_text_message of this PostTextRequest.
        :rtype: PostTextMessage
        """
        return self._post_text_message

    @post_text_message.setter
    def post_text_message(self, post_text_message):
        """
        Sets the post_text_message of this PostTextRequest.
        Message to send to the bot

        :param post_text_message: The post_text_message of this PostTextRequest.
        :type: PostTextMessage
        """
        
        self._post_text_message = post_text_message

    @property
    def language_code(self):
        """
        Gets the language_code of this PostTextRequest.
        The launguage code the bot will run under

        :return: The language_code of this PostTextRequest.
        :rtype: str
        """
        return self._language_code

    @language_code.setter
    def language_code(self, language_code):
        """
        Sets the language_code of this PostTextRequest.
        The launguage code the bot will run under

        :param language_code: The language_code of this PostTextRequest.
        :type: str
        """
        
        self._language_code = language_code

    @property
    def bot_session_timeout_minutes(self):
        """
        Gets the bot_session_timeout_minutes of this PostTextRequest.
        Override timeout for the bot session. This should be greater than 10 minutes.

        :return: The bot_session_timeout_minutes of this PostTextRequest.
        :rtype: int
        """
        return self._bot_session_timeout_minutes

    @bot_session_timeout_minutes.setter
    def bot_session_timeout_minutes(self, bot_session_timeout_minutes):
        """
        Sets the bot_session_timeout_minutes of this PostTextRequest.
        Override timeout for the bot session. This should be greater than 10 minutes.

        :param bot_session_timeout_minutes: The bot_session_timeout_minutes of this PostTextRequest.
        :type: int
        """
        
        self._bot_session_timeout_minutes = bot_session_timeout_minutes

    @property
    def bot_channels(self):
        """
        Gets the bot_channels of this PostTextRequest.
        The channels this bot is utilizing

        :return: The bot_channels of this PostTextRequest.
        :rtype: list[str]
        """
        return self._bot_channels

    @bot_channels.setter
    def bot_channels(self, bot_channels):
        """
        Sets the bot_channels of this PostTextRequest.
        The channels this bot is utilizing

        :param bot_channels: The bot_channels of this PostTextRequest.
        :type: list[str]
        """
        
        self._bot_channels = bot_channels

    @property
    def bot_correlation_id(self):
        """
        Gets the bot_correlation_id of this PostTextRequest.
        Id for tracking the activity - this will be returned in the response

        :return: The bot_correlation_id of this PostTextRequest.
        :rtype: str
        """
        return self._bot_correlation_id

    @bot_correlation_id.setter
    def bot_correlation_id(self, bot_correlation_id):
        """
        Sets the bot_correlation_id of this PostTextRequest.
        Id for tracking the activity - this will be returned in the response

        :param bot_correlation_id: The bot_correlation_id of this PostTextRequest.
        :type: str
        """
        
        self._bot_correlation_id = bot_correlation_id

    @property
    def amazon_lex_request(self):
        """
        Gets the amazon_lex_request of this PostTextRequest.


        :return: The amazon_lex_request of this PostTextRequest.
        :rtype: AmazonLexRequest
        """
        return self._amazon_lex_request

    @amazon_lex_request.setter
    def amazon_lex_request(self, amazon_lex_request):
        """
        Sets the amazon_lex_request of this PostTextRequest.


        :param amazon_lex_request: The amazon_lex_request of this PostTextRequest.
        :type: AmazonLexRequest
        """
        
        self._amazon_lex_request = amazon_lex_request

    @property
    def google_dialogflow(self):
        """
        Gets the google_dialogflow of this PostTextRequest.


        :return: The google_dialogflow of this PostTextRequest.
        :rtype: GoogleDialogflowCustomSettings
        """
        return self._google_dialogflow

    @google_dialogflow.setter
    def google_dialogflow(self, google_dialogflow):
        """
        Sets the google_dialogflow of this PostTextRequest.


        :param google_dialogflow: The google_dialogflow of this PostTextRequest.
        :type: GoogleDialogflowCustomSettings
        """
        
        self._google_dialogflow = google_dialogflow

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

