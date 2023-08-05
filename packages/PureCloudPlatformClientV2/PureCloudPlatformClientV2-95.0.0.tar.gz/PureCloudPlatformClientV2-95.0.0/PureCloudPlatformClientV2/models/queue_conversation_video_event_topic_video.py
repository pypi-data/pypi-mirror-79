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

class QueueConversationVideoEventTopicVideo(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        QueueConversationVideoEventTopicVideo - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'state': 'str',
            'pcSelf': 'QueueConversationVideoEventTopicAddress',
            'id': 'str',
            'context': 'str',
            'audio_muted': 'bool',
            'video_muted': 'bool',
            'sharing_screen': 'bool',
            'provider': 'str',
            'script_id': 'str',
            'peer_id': 'str',
            'disconnect_type': 'str',
            'connected_time': 'datetime',
            'disconnected_time': 'datetime',
            'msids': 'list[str]',
            'wrapup': 'QueueConversationVideoEventTopicWrapup',
            'after_call_work': 'QueueConversationVideoEventTopicAfterCallWork',
            'additional_properties': 'object'
        }

        self.attribute_map = {
            'state': 'state',
            'pcSelf': 'self',
            'id': 'id',
            'context': 'context',
            'audio_muted': 'audioMuted',
            'video_muted': 'videoMuted',
            'sharing_screen': 'sharingScreen',
            'provider': 'provider',
            'script_id': 'scriptId',
            'peer_id': 'peerId',
            'disconnect_type': 'disconnectType',
            'connected_time': 'connectedTime',
            'disconnected_time': 'disconnectedTime',
            'msids': 'msids',
            'wrapup': 'wrapup',
            'after_call_work': 'afterCallWork',
            'additional_properties': 'additionalProperties'
        }

        self._state = None
        self._pcSelf = None
        self._id = None
        self._context = None
        self._audio_muted = None
        self._video_muted = None
        self._sharing_screen = None
        self._provider = None
        self._script_id = None
        self._peer_id = None
        self._disconnect_type = None
        self._connected_time = None
        self._disconnected_time = None
        self._msids = None
        self._wrapup = None
        self._after_call_work = None
        self._additional_properties = None

    @property
    def state(self):
        """
        Gets the state of this QueueConversationVideoEventTopicVideo.


        :return: The state of this QueueConversationVideoEventTopicVideo.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this QueueConversationVideoEventTopicVideo.


        :param state: The state of this QueueConversationVideoEventTopicVideo.
        :type: str
        """
        allowed_values = ["ALERTING", "DIALING", "CONTACTING", "OFFERING", "CONNECTED", "DISCONNECTED", "TERMINATED", "NONE"]
        if state.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for state -> " + state
            self._state = "outdated_sdk_version"
        else:
            self._state = state

    @property
    def pcSelf(self):
        """
        Gets the pcSelf of this QueueConversationVideoEventTopicVideo.


        :return: The pcSelf of this QueueConversationVideoEventTopicVideo.
        :rtype: QueueConversationVideoEventTopicAddress
        """
        return self._pcSelf

    @pcSelf.setter
    def pcSelf(self, pcSelf):
        """
        Sets the pcSelf of this QueueConversationVideoEventTopicVideo.


        :param pcSelf: The pcSelf of this QueueConversationVideoEventTopicVideo.
        :type: QueueConversationVideoEventTopicAddress
        """
        
        self._pcSelf = pcSelf

    @property
    def id(self):
        """
        Gets the id of this QueueConversationVideoEventTopicVideo.


        :return: The id of this QueueConversationVideoEventTopicVideo.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this QueueConversationVideoEventTopicVideo.


        :param id: The id of this QueueConversationVideoEventTopicVideo.
        :type: str
        """
        
        self._id = id

    @property
    def context(self):
        """
        Gets the context of this QueueConversationVideoEventTopicVideo.


        :return: The context of this QueueConversationVideoEventTopicVideo.
        :rtype: str
        """
        return self._context

    @context.setter
    def context(self, context):
        """
        Sets the context of this QueueConversationVideoEventTopicVideo.


        :param context: The context of this QueueConversationVideoEventTopicVideo.
        :type: str
        """
        
        self._context = context

    @property
    def audio_muted(self):
        """
        Gets the audio_muted of this QueueConversationVideoEventTopicVideo.


        :return: The audio_muted of this QueueConversationVideoEventTopicVideo.
        :rtype: bool
        """
        return self._audio_muted

    @audio_muted.setter
    def audio_muted(self, audio_muted):
        """
        Sets the audio_muted of this QueueConversationVideoEventTopicVideo.


        :param audio_muted: The audio_muted of this QueueConversationVideoEventTopicVideo.
        :type: bool
        """
        
        self._audio_muted = audio_muted

    @property
    def video_muted(self):
        """
        Gets the video_muted of this QueueConversationVideoEventTopicVideo.


        :return: The video_muted of this QueueConversationVideoEventTopicVideo.
        :rtype: bool
        """
        return self._video_muted

    @video_muted.setter
    def video_muted(self, video_muted):
        """
        Sets the video_muted of this QueueConversationVideoEventTopicVideo.


        :param video_muted: The video_muted of this QueueConversationVideoEventTopicVideo.
        :type: bool
        """
        
        self._video_muted = video_muted

    @property
    def sharing_screen(self):
        """
        Gets the sharing_screen of this QueueConversationVideoEventTopicVideo.


        :return: The sharing_screen of this QueueConversationVideoEventTopicVideo.
        :rtype: bool
        """
        return self._sharing_screen

    @sharing_screen.setter
    def sharing_screen(self, sharing_screen):
        """
        Sets the sharing_screen of this QueueConversationVideoEventTopicVideo.


        :param sharing_screen: The sharing_screen of this QueueConversationVideoEventTopicVideo.
        :type: bool
        """
        
        self._sharing_screen = sharing_screen

    @property
    def provider(self):
        """
        Gets the provider of this QueueConversationVideoEventTopicVideo.


        :return: The provider of this QueueConversationVideoEventTopicVideo.
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """
        Sets the provider of this QueueConversationVideoEventTopicVideo.


        :param provider: The provider of this QueueConversationVideoEventTopicVideo.
        :type: str
        """
        
        self._provider = provider

    @property
    def script_id(self):
        """
        Gets the script_id of this QueueConversationVideoEventTopicVideo.


        :return: The script_id of this QueueConversationVideoEventTopicVideo.
        :rtype: str
        """
        return self._script_id

    @script_id.setter
    def script_id(self, script_id):
        """
        Sets the script_id of this QueueConversationVideoEventTopicVideo.


        :param script_id: The script_id of this QueueConversationVideoEventTopicVideo.
        :type: str
        """
        
        self._script_id = script_id

    @property
    def peer_id(self):
        """
        Gets the peer_id of this QueueConversationVideoEventTopicVideo.


        :return: The peer_id of this QueueConversationVideoEventTopicVideo.
        :rtype: str
        """
        return self._peer_id

    @peer_id.setter
    def peer_id(self, peer_id):
        """
        Sets the peer_id of this QueueConversationVideoEventTopicVideo.


        :param peer_id: The peer_id of this QueueConversationVideoEventTopicVideo.
        :type: str
        """
        
        self._peer_id = peer_id

    @property
    def disconnect_type(self):
        """
        Gets the disconnect_type of this QueueConversationVideoEventTopicVideo.


        :return: The disconnect_type of this QueueConversationVideoEventTopicVideo.
        :rtype: str
        """
        return self._disconnect_type

    @disconnect_type.setter
    def disconnect_type(self, disconnect_type):
        """
        Sets the disconnect_type of this QueueConversationVideoEventTopicVideo.


        :param disconnect_type: The disconnect_type of this QueueConversationVideoEventTopicVideo.
        :type: str
        """
        allowed_values = ["ENDPOINT", "CLIENT", "SYSTEM", "TIMEOUT", "TRANSFER", "TRANSFER_CONFERENCE", "TRANSFER_CONSULT", "TRANSFER_FORWARD", "TRANSFER_NOANSWER", "TRANSFER_NOTAVAILABLE", "TRANSPORT_FAILURE", "ERROR", "PEER", "OTHER", "SPAM", "UNCALLABLE"]
        if disconnect_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for disconnect_type -> " + disconnect_type
            self._disconnect_type = "outdated_sdk_version"
        else:
            self._disconnect_type = disconnect_type

    @property
    def connected_time(self):
        """
        Gets the connected_time of this QueueConversationVideoEventTopicVideo.


        :return: The connected_time of this QueueConversationVideoEventTopicVideo.
        :rtype: datetime
        """
        return self._connected_time

    @connected_time.setter
    def connected_time(self, connected_time):
        """
        Sets the connected_time of this QueueConversationVideoEventTopicVideo.


        :param connected_time: The connected_time of this QueueConversationVideoEventTopicVideo.
        :type: datetime
        """
        
        self._connected_time = connected_time

    @property
    def disconnected_time(self):
        """
        Gets the disconnected_time of this QueueConversationVideoEventTopicVideo.


        :return: The disconnected_time of this QueueConversationVideoEventTopicVideo.
        :rtype: datetime
        """
        return self._disconnected_time

    @disconnected_time.setter
    def disconnected_time(self, disconnected_time):
        """
        Sets the disconnected_time of this QueueConversationVideoEventTopicVideo.


        :param disconnected_time: The disconnected_time of this QueueConversationVideoEventTopicVideo.
        :type: datetime
        """
        
        self._disconnected_time = disconnected_time

    @property
    def msids(self):
        """
        Gets the msids of this QueueConversationVideoEventTopicVideo.


        :return: The msids of this QueueConversationVideoEventTopicVideo.
        :rtype: list[str]
        """
        return self._msids

    @msids.setter
    def msids(self, msids):
        """
        Sets the msids of this QueueConversationVideoEventTopicVideo.


        :param msids: The msids of this QueueConversationVideoEventTopicVideo.
        :type: list[str]
        """
        
        self._msids = msids

    @property
    def wrapup(self):
        """
        Gets the wrapup of this QueueConversationVideoEventTopicVideo.


        :return: The wrapup of this QueueConversationVideoEventTopicVideo.
        :rtype: QueueConversationVideoEventTopicWrapup
        """
        return self._wrapup

    @wrapup.setter
    def wrapup(self, wrapup):
        """
        Sets the wrapup of this QueueConversationVideoEventTopicVideo.


        :param wrapup: The wrapup of this QueueConversationVideoEventTopicVideo.
        :type: QueueConversationVideoEventTopicWrapup
        """
        
        self._wrapup = wrapup

    @property
    def after_call_work(self):
        """
        Gets the after_call_work of this QueueConversationVideoEventTopicVideo.


        :return: The after_call_work of this QueueConversationVideoEventTopicVideo.
        :rtype: QueueConversationVideoEventTopicAfterCallWork
        """
        return self._after_call_work

    @after_call_work.setter
    def after_call_work(self, after_call_work):
        """
        Sets the after_call_work of this QueueConversationVideoEventTopicVideo.


        :param after_call_work: The after_call_work of this QueueConversationVideoEventTopicVideo.
        :type: QueueConversationVideoEventTopicAfterCallWork
        """
        
        self._after_call_work = after_call_work

    @property
    def additional_properties(self):
        """
        Gets the additional_properties of this QueueConversationVideoEventTopicVideo.


        :return: The additional_properties of this QueueConversationVideoEventTopicVideo.
        :rtype: object
        """
        return self._additional_properties

    @additional_properties.setter
    def additional_properties(self, additional_properties):
        """
        Sets the additional_properties of this QueueConversationVideoEventTopicVideo.


        :param additional_properties: The additional_properties of this QueueConversationVideoEventTopicVideo.
        :type: object
        """
        
        self._additional_properties = additional_properties

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

