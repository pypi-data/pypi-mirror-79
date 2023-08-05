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

class Document(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Document - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'change_number': 'int',
            'date_created': 'datetime',
            'date_modified': 'datetime',
            'date_uploaded': 'datetime',
            'content_uri': 'str',
            'workspace': 'DomainEntityRef',
            'created_by': 'DomainEntityRef',
            'uploaded_by': 'DomainEntityRef',
            'content_type': 'str',
            'content_length': 'int',
            'system_type': 'str',
            'filename': 'str',
            'page_count': 'int',
            'read': 'bool',
            'caller_address': 'str',
            'receiver_address': 'str',
            'tags': 'list[str]',
            'tag_values': 'list[TagValue]',
            'attributes': 'list[DocumentAttribute]',
            'thumbnails': 'list[DocumentThumbnail]',
            'upload_status': 'DomainEntityRef',
            'upload_destination_uri': 'str',
            'upload_method': 'str',
            'lock_info': 'LockInfo',
            'acl': 'list[str]',
            'sharing_status': 'str',
            'sharing_uri': 'str',
            'download_sharing_uri': 'str',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'change_number': 'changeNumber',
            'date_created': 'dateCreated',
            'date_modified': 'dateModified',
            'date_uploaded': 'dateUploaded',
            'content_uri': 'contentUri',
            'workspace': 'workspace',
            'created_by': 'createdBy',
            'uploaded_by': 'uploadedBy',
            'content_type': 'contentType',
            'content_length': 'contentLength',
            'system_type': 'systemType',
            'filename': 'filename',
            'page_count': 'pageCount',
            'read': 'read',
            'caller_address': 'callerAddress',
            'receiver_address': 'receiverAddress',
            'tags': 'tags',
            'tag_values': 'tagValues',
            'attributes': 'attributes',
            'thumbnails': 'thumbnails',
            'upload_status': 'uploadStatus',
            'upload_destination_uri': 'uploadDestinationUri',
            'upload_method': 'uploadMethod',
            'lock_info': 'lockInfo',
            'acl': 'acl',
            'sharing_status': 'sharingStatus',
            'sharing_uri': 'sharingUri',
            'download_sharing_uri': 'downloadSharingUri',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._change_number = None
        self._date_created = None
        self._date_modified = None
        self._date_uploaded = None
        self._content_uri = None
        self._workspace = None
        self._created_by = None
        self._uploaded_by = None
        self._content_type = None
        self._content_length = None
        self._system_type = None
        self._filename = None
        self._page_count = None
        self._read = None
        self._caller_address = None
        self._receiver_address = None
        self._tags = None
        self._tag_values = None
        self._attributes = None
        self._thumbnails = None
        self._upload_status = None
        self._upload_destination_uri = None
        self._upload_method = None
        self._lock_info = None
        self._acl = None
        self._sharing_status = None
        self._sharing_uri = None
        self._download_sharing_uri = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this Document.
        The globally unique identifier for the object.

        :return: The id of this Document.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Document.
        The globally unique identifier for the object.

        :param id: The id of this Document.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this Document.


        :return: The name of this Document.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Document.


        :param name: The name of this Document.
        :type: str
        """
        
        self._name = name

    @property
    def change_number(self):
        """
        Gets the change_number of this Document.


        :return: The change_number of this Document.
        :rtype: int
        """
        return self._change_number

    @change_number.setter
    def change_number(self, change_number):
        """
        Sets the change_number of this Document.


        :param change_number: The change_number of this Document.
        :type: int
        """
        
        self._change_number = change_number

    @property
    def date_created(self):
        """
        Gets the date_created of this Document.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_created of this Document.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this Document.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_created: The date_created of this Document.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def date_modified(self):
        """
        Gets the date_modified of this Document.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_modified of this Document.
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """
        Sets the date_modified of this Document.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_modified: The date_modified of this Document.
        :type: datetime
        """
        
        self._date_modified = date_modified

    @property
    def date_uploaded(self):
        """
        Gets the date_uploaded of this Document.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_uploaded of this Document.
        :rtype: datetime
        """
        return self._date_uploaded

    @date_uploaded.setter
    def date_uploaded(self, date_uploaded):
        """
        Sets the date_uploaded of this Document.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_uploaded: The date_uploaded of this Document.
        :type: datetime
        """
        
        self._date_uploaded = date_uploaded

    @property
    def content_uri(self):
        """
        Gets the content_uri of this Document.


        :return: The content_uri of this Document.
        :rtype: str
        """
        return self._content_uri

    @content_uri.setter
    def content_uri(self, content_uri):
        """
        Sets the content_uri of this Document.


        :param content_uri: The content_uri of this Document.
        :type: str
        """
        
        self._content_uri = content_uri

    @property
    def workspace(self):
        """
        Gets the workspace of this Document.


        :return: The workspace of this Document.
        :rtype: DomainEntityRef
        """
        return self._workspace

    @workspace.setter
    def workspace(self, workspace):
        """
        Sets the workspace of this Document.


        :param workspace: The workspace of this Document.
        :type: DomainEntityRef
        """
        
        self._workspace = workspace

    @property
    def created_by(self):
        """
        Gets the created_by of this Document.


        :return: The created_by of this Document.
        :rtype: DomainEntityRef
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this Document.


        :param created_by: The created_by of this Document.
        :type: DomainEntityRef
        """
        
        self._created_by = created_by

    @property
    def uploaded_by(self):
        """
        Gets the uploaded_by of this Document.


        :return: The uploaded_by of this Document.
        :rtype: DomainEntityRef
        """
        return self._uploaded_by

    @uploaded_by.setter
    def uploaded_by(self, uploaded_by):
        """
        Sets the uploaded_by of this Document.


        :param uploaded_by: The uploaded_by of this Document.
        :type: DomainEntityRef
        """
        
        self._uploaded_by = uploaded_by

    @property
    def content_type(self):
        """
        Gets the content_type of this Document.


        :return: The content_type of this Document.
        :rtype: str
        """
        return self._content_type

    @content_type.setter
    def content_type(self, content_type):
        """
        Sets the content_type of this Document.


        :param content_type: The content_type of this Document.
        :type: str
        """
        
        self._content_type = content_type

    @property
    def content_length(self):
        """
        Gets the content_length of this Document.


        :return: The content_length of this Document.
        :rtype: int
        """
        return self._content_length

    @content_length.setter
    def content_length(self, content_length):
        """
        Sets the content_length of this Document.


        :param content_length: The content_length of this Document.
        :type: int
        """
        
        self._content_length = content_length

    @property
    def system_type(self):
        """
        Gets the system_type of this Document.


        :return: The system_type of this Document.
        :rtype: str
        """
        return self._system_type

    @system_type.setter
    def system_type(self, system_type):
        """
        Sets the system_type of this Document.


        :param system_type: The system_type of this Document.
        :type: str
        """
        allowed_values = ["DOCUMENT", "FAX", "RECORDING"]
        if system_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for system_type -> " + system_type
            self._system_type = "outdated_sdk_version"
        else:
            self._system_type = system_type

    @property
    def filename(self):
        """
        Gets the filename of this Document.


        :return: The filename of this Document.
        :rtype: str
        """
        return self._filename

    @filename.setter
    def filename(self, filename):
        """
        Sets the filename of this Document.


        :param filename: The filename of this Document.
        :type: str
        """
        
        self._filename = filename

    @property
    def page_count(self):
        """
        Gets the page_count of this Document.


        :return: The page_count of this Document.
        :rtype: int
        """
        return self._page_count

    @page_count.setter
    def page_count(self, page_count):
        """
        Sets the page_count of this Document.


        :param page_count: The page_count of this Document.
        :type: int
        """
        
        self._page_count = page_count

    @property
    def read(self):
        """
        Gets the read of this Document.


        :return: The read of this Document.
        :rtype: bool
        """
        return self._read

    @read.setter
    def read(self, read):
        """
        Sets the read of this Document.


        :param read: The read of this Document.
        :type: bool
        """
        
        self._read = read

    @property
    def caller_address(self):
        """
        Gets the caller_address of this Document.


        :return: The caller_address of this Document.
        :rtype: str
        """
        return self._caller_address

    @caller_address.setter
    def caller_address(self, caller_address):
        """
        Sets the caller_address of this Document.


        :param caller_address: The caller_address of this Document.
        :type: str
        """
        
        self._caller_address = caller_address

    @property
    def receiver_address(self):
        """
        Gets the receiver_address of this Document.


        :return: The receiver_address of this Document.
        :rtype: str
        """
        return self._receiver_address

    @receiver_address.setter
    def receiver_address(self, receiver_address):
        """
        Sets the receiver_address of this Document.


        :param receiver_address: The receiver_address of this Document.
        :type: str
        """
        
        self._receiver_address = receiver_address

    @property
    def tags(self):
        """
        Gets the tags of this Document.


        :return: The tags of this Document.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this Document.


        :param tags: The tags of this Document.
        :type: list[str]
        """
        
        self._tags = tags

    @property
    def tag_values(self):
        """
        Gets the tag_values of this Document.


        :return: The tag_values of this Document.
        :rtype: list[TagValue]
        """
        return self._tag_values

    @tag_values.setter
    def tag_values(self, tag_values):
        """
        Sets the tag_values of this Document.


        :param tag_values: The tag_values of this Document.
        :type: list[TagValue]
        """
        
        self._tag_values = tag_values

    @property
    def attributes(self):
        """
        Gets the attributes of this Document.


        :return: The attributes of this Document.
        :rtype: list[DocumentAttribute]
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """
        Sets the attributes of this Document.


        :param attributes: The attributes of this Document.
        :type: list[DocumentAttribute]
        """
        
        self._attributes = attributes

    @property
    def thumbnails(self):
        """
        Gets the thumbnails of this Document.


        :return: The thumbnails of this Document.
        :rtype: list[DocumentThumbnail]
        """
        return self._thumbnails

    @thumbnails.setter
    def thumbnails(self, thumbnails):
        """
        Sets the thumbnails of this Document.


        :param thumbnails: The thumbnails of this Document.
        :type: list[DocumentThumbnail]
        """
        
        self._thumbnails = thumbnails

    @property
    def upload_status(self):
        """
        Gets the upload_status of this Document.


        :return: The upload_status of this Document.
        :rtype: DomainEntityRef
        """
        return self._upload_status

    @upload_status.setter
    def upload_status(self, upload_status):
        """
        Sets the upload_status of this Document.


        :param upload_status: The upload_status of this Document.
        :type: DomainEntityRef
        """
        
        self._upload_status = upload_status

    @property
    def upload_destination_uri(self):
        """
        Gets the upload_destination_uri of this Document.


        :return: The upload_destination_uri of this Document.
        :rtype: str
        """
        return self._upload_destination_uri

    @upload_destination_uri.setter
    def upload_destination_uri(self, upload_destination_uri):
        """
        Sets the upload_destination_uri of this Document.


        :param upload_destination_uri: The upload_destination_uri of this Document.
        :type: str
        """
        
        self._upload_destination_uri = upload_destination_uri

    @property
    def upload_method(self):
        """
        Gets the upload_method of this Document.


        :return: The upload_method of this Document.
        :rtype: str
        """
        return self._upload_method

    @upload_method.setter
    def upload_method(self, upload_method):
        """
        Sets the upload_method of this Document.


        :param upload_method: The upload_method of this Document.
        :type: str
        """
        allowed_values = ["SINGLE_PUT", "MULTIPART_POST"]
        if upload_method.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for upload_method -> " + upload_method
            self._upload_method = "outdated_sdk_version"
        else:
            self._upload_method = upload_method

    @property
    def lock_info(self):
        """
        Gets the lock_info of this Document.


        :return: The lock_info of this Document.
        :rtype: LockInfo
        """
        return self._lock_info

    @lock_info.setter
    def lock_info(self, lock_info):
        """
        Sets the lock_info of this Document.


        :param lock_info: The lock_info of this Document.
        :type: LockInfo
        """
        
        self._lock_info = lock_info

    @property
    def acl(self):
        """
        Gets the acl of this Document.
        A list of permitted action rights for the user making the request

        :return: The acl of this Document.
        :rtype: list[str]
        """
        return self._acl

    @acl.setter
    def acl(self, acl):
        """
        Sets the acl of this Document.
        A list of permitted action rights for the user making the request

        :param acl: The acl of this Document.
        :type: list[str]
        """
        
        self._acl = acl

    @property
    def sharing_status(self):
        """
        Gets the sharing_status of this Document.


        :return: The sharing_status of this Document.
        :rtype: str
        """
        return self._sharing_status

    @sharing_status.setter
    def sharing_status(self, sharing_status):
        """
        Sets the sharing_status of this Document.


        :param sharing_status: The sharing_status of this Document.
        :type: str
        """
        allowed_values = ["NONE", "LIMITED", "PUBLIC"]
        if sharing_status.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for sharing_status -> " + sharing_status
            self._sharing_status = "outdated_sdk_version"
        else:
            self._sharing_status = sharing_status

    @property
    def sharing_uri(self):
        """
        Gets the sharing_uri of this Document.


        :return: The sharing_uri of this Document.
        :rtype: str
        """
        return self._sharing_uri

    @sharing_uri.setter
    def sharing_uri(self, sharing_uri):
        """
        Sets the sharing_uri of this Document.


        :param sharing_uri: The sharing_uri of this Document.
        :type: str
        """
        
        self._sharing_uri = sharing_uri

    @property
    def download_sharing_uri(self):
        """
        Gets the download_sharing_uri of this Document.


        :return: The download_sharing_uri of this Document.
        :rtype: str
        """
        return self._download_sharing_uri

    @download_sharing_uri.setter
    def download_sharing_uri(self, download_sharing_uri):
        """
        Sets the download_sharing_uri of this Document.


        :param download_sharing_uri: The download_sharing_uri of this Document.
        :type: str
        """
        
        self._download_sharing_uri = download_sharing_uri

    @property
    def self_uri(self):
        """
        Gets the self_uri of this Document.
        The URI for this object

        :return: The self_uri of this Document.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this Document.
        The URI for this object

        :param self_uri: The self_uri of this Document.
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

