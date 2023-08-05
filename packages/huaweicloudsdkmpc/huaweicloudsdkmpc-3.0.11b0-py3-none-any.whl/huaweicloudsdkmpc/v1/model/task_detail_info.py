# coding: utf-8

import pprint
import re

import six





class TaskDetailInfo:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'task_id': 'str',
        'status': 'str',
        'create_time': 'str',
        'start_time': 'str',
        'end_time': 'str',
        'input': 'ObsObjInfo',
        'output': 'ObsObjInfo',
        'description': 'str',
        'media_detail': 'MediaDetail',
        'xcode_error': 'ErrorResponse'
    }

    attribute_map = {
        'task_id': 'task_id',
        'status': 'status',
        'create_time': 'create_time',
        'start_time': 'start_time',
        'end_time': 'end_time',
        'input': 'input',
        'output': 'output',
        'description': 'description',
        'media_detail': 'media_detail',
        'xcode_error': 'xcode_error'
    }

    def __init__(self, task_id=None, status=None, create_time=None, start_time=None, end_time=None, input=None, output=None, description=None, media_detail=None, xcode_error=None):
        """TaskDetailInfo - a model defined in huaweicloud sdk"""
        
        

        self._task_id = None
        self._status = None
        self._create_time = None
        self._start_time = None
        self._end_time = None
        self._input = None
        self._output = None
        self._description = None
        self._media_detail = None
        self._xcode_error = None
        self.discriminator = None

        if task_id is not None:
            self.task_id = task_id
        if status is not None:
            self.status = status
        if create_time is not None:
            self.create_time = create_time
        if start_time is not None:
            self.start_time = start_time
        if end_time is not None:
            self.end_time = end_time
        if input is not None:
            self.input = input
        if output is not None:
            self.output = output
        if description is not None:
            self.description = description
        if media_detail is not None:
            self.media_detail = media_detail
        if xcode_error is not None:
            self.xcode_error = xcode_error

    @property
    def task_id(self):
        """Gets the task_id of this TaskDetailInfo.

        任务ID。

        :return: The task_id of this TaskDetailInfo.
        :rtype: str
        """
        return self._task_id

    @task_id.setter
    def task_id(self, task_id):
        """Sets the task_id of this TaskDetailInfo.

        任务ID。

        :param task_id: The task_id of this TaskDetailInfo.
        :type: str
        """
        self._task_id = task_id

    @property
    def status(self):
        """Gets the status of this TaskDetailInfo.

        任务执行状态，取值如下。 

        :return: The status of this TaskDetailInfo.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this TaskDetailInfo.

        任务执行状态，取值如下。 

        :param status: The status of this TaskDetailInfo.
        :type: str
        """
        self._status = status

    @property
    def create_time(self):
        """Gets the create_time of this TaskDetailInfo.

        转码任务启动时间 

        :return: The create_time of this TaskDetailInfo.
        :rtype: str
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this TaskDetailInfo.

        转码任务启动时间 

        :param create_time: The create_time of this TaskDetailInfo.
        :type: str
        """
        self._create_time = create_time

    @property
    def start_time(self):
        """Gets the start_time of this TaskDetailInfo.

        下发xcode任务成功时间 

        :return: The start_time of this TaskDetailInfo.
        :rtype: str
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this TaskDetailInfo.

        下发xcode任务成功时间 

        :param start_time: The start_time of this TaskDetailInfo.
        :type: str
        """
        self._start_time = start_time

    @property
    def end_time(self):
        """Gets the end_time of this TaskDetailInfo.

        转码任务结束时间 

        :return: The end_time of this TaskDetailInfo.
        :rtype: str
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this TaskDetailInfo.

        转码任务结束时间 

        :param end_time: The end_time of this TaskDetailInfo.
        :type: str
        """
        self._end_time = end_time

    @property
    def input(self):
        """Gets the input of this TaskDetailInfo.


        :return: The input of this TaskDetailInfo.
        :rtype: ObsObjInfo
        """
        return self._input

    @input.setter
    def input(self, input):
        """Sets the input of this TaskDetailInfo.


        :param input: The input of this TaskDetailInfo.
        :type: ObsObjInfo
        """
        self._input = input

    @property
    def output(self):
        """Gets the output of this TaskDetailInfo.


        :return: The output of this TaskDetailInfo.
        :rtype: ObsObjInfo
        """
        return self._output

    @output.setter
    def output(self, output):
        """Sets the output of this TaskDetailInfo.


        :param output: The output of this TaskDetailInfo.
        :type: ObsObjInfo
        """
        self._output = output

    @property
    def description(self):
        """Gets the description of this TaskDetailInfo.

        转码任务描述，当转码出现异常时，此字段为异常的原因。 

        :return: The description of this TaskDetailInfo.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this TaskDetailInfo.

        转码任务描述，当转码出现异常时，此字段为异常的原因。 

        :param description: The description of this TaskDetailInfo.
        :type: str
        """
        self._description = description

    @property
    def media_detail(self):
        """Gets the media_detail of this TaskDetailInfo.


        :return: The media_detail of this TaskDetailInfo.
        :rtype: MediaDetail
        """
        return self._media_detail

    @media_detail.setter
    def media_detail(self, media_detail):
        """Sets the media_detail of this TaskDetailInfo.


        :param media_detail: The media_detail of this TaskDetailInfo.
        :type: MediaDetail
        """
        self._media_detail = media_detail

    @property
    def xcode_error(self):
        """Gets the xcode_error of this TaskDetailInfo.


        :return: The xcode_error of this TaskDetailInfo.
        :rtype: ErrorResponse
        """
        return self._xcode_error

    @xcode_error.setter
    def xcode_error(self, xcode_error):
        """Sets the xcode_error of this TaskDetailInfo.


        :param xcode_error: The xcode_error of this TaskDetailInfo.
        :type: ErrorResponse
        """
        self._xcode_error = xcode_error

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, TaskDetailInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
