# coding: utf-8

import pprint
import re

import six





class AnimatedGraphicsTask:


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
        'description': 'str',
        'input': 'ObsObjInfo',
        'output': 'ObsObjInfo',
        'output_param': 'AnimatedGraphicsOutputParam'
    }

    attribute_map = {
        'task_id': 'task_id',
        'status': 'status',
        'create_time': 'create_time',
        'start_time': 'start_time',
        'end_time': 'end_time',
        'description': 'description',
        'input': 'input',
        'output': 'output',
        'output_param': 'output_param'
    }

    def __init__(self, task_id=None, status=None, create_time=None, start_time=None, end_time=None, description=None, input=None, output=None, output_param=None):
        """AnimatedGraphicsTask - a model defined in huaweicloud sdk"""
        
        

        self._task_id = None
        self._status = None
        self._create_time = None
        self._start_time = None
        self._end_time = None
        self._description = None
        self._input = None
        self._output = None
        self._output_param = None
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
        if description is not None:
            self.description = description
        if input is not None:
            self.input = input
        if output is not None:
            self.output = output
        if output_param is not None:
            self.output_param = output_param

    @property
    def task_id(self):
        """Gets the task_id of this AnimatedGraphicsTask.

        任务ID 

        :return: The task_id of this AnimatedGraphicsTask.
        :rtype: str
        """
        return self._task_id

    @task_id.setter
    def task_id(self, task_id):
        """Sets the task_id of this AnimatedGraphicsTask.

        任务ID 

        :param task_id: The task_id of this AnimatedGraphicsTask.
        :type: str
        """
        self._task_id = task_id

    @property
    def status(self):
        """Gets the status of this AnimatedGraphicsTask.

        任务状态。  取值如下： - INIT：初始状态。 - WAITING：等待启动。 - PROCESSING：处理中。 - SUCCEED：处理成功。 - FAILED：处理失败。 - CANCELED：已取消。 

        :return: The status of this AnimatedGraphicsTask.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this AnimatedGraphicsTask.

        任务状态。  取值如下： - INIT：初始状态。 - WAITING：等待启动。 - PROCESSING：处理中。 - SUCCEED：处理成功。 - FAILED：处理失败。 - CANCELED：已取消。 

        :param status: The status of this AnimatedGraphicsTask.
        :type: str
        """
        self._status = status

    @property
    def create_time(self):
        """Gets the create_time of this AnimatedGraphicsTask.

        任务创建时间 

        :return: The create_time of this AnimatedGraphicsTask.
        :rtype: str
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this AnimatedGraphicsTask.

        任务创建时间 

        :param create_time: The create_time of this AnimatedGraphicsTask.
        :type: str
        """
        self._create_time = create_time

    @property
    def start_time(self):
        """Gets the start_time of this AnimatedGraphicsTask.

        任务启动时间 

        :return: The start_time of this AnimatedGraphicsTask.
        :rtype: str
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this AnimatedGraphicsTask.

        任务启动时间 

        :param start_time: The start_time of this AnimatedGraphicsTask.
        :type: str
        """
        self._start_time = start_time

    @property
    def end_time(self):
        """Gets the end_time of this AnimatedGraphicsTask.

        任务结束时间 

        :return: The end_time of this AnimatedGraphicsTask.
        :rtype: str
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this AnimatedGraphicsTask.

        任务结束时间 

        :param end_time: The end_time of this AnimatedGraphicsTask.
        :type: str
        """
        self._end_time = end_time

    @property
    def description(self):
        """Gets the description of this AnimatedGraphicsTask.

        错误描述 

        :return: The description of this AnimatedGraphicsTask.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this AnimatedGraphicsTask.

        错误描述 

        :param description: The description of this AnimatedGraphicsTask.
        :type: str
        """
        self._description = description

    @property
    def input(self):
        """Gets the input of this AnimatedGraphicsTask.


        :return: The input of this AnimatedGraphicsTask.
        :rtype: ObsObjInfo
        """
        return self._input

    @input.setter
    def input(self, input):
        """Sets the input of this AnimatedGraphicsTask.


        :param input: The input of this AnimatedGraphicsTask.
        :type: ObsObjInfo
        """
        self._input = input

    @property
    def output(self):
        """Gets the output of this AnimatedGraphicsTask.


        :return: The output of this AnimatedGraphicsTask.
        :rtype: ObsObjInfo
        """
        return self._output

    @output.setter
    def output(self, output):
        """Sets the output of this AnimatedGraphicsTask.


        :param output: The output of this AnimatedGraphicsTask.
        :type: ObsObjInfo
        """
        self._output = output

    @property
    def output_param(self):
        """Gets the output_param of this AnimatedGraphicsTask.


        :return: The output_param of this AnimatedGraphicsTask.
        :rtype: AnimatedGraphicsOutputParam
        """
        return self._output_param

    @output_param.setter
    def output_param(self, output_param):
        """Sets the output_param of this AnimatedGraphicsTask.


        :param output_param: The output_param of this AnimatedGraphicsTask.
        :type: AnimatedGraphicsOutputParam
        """
        self._output_param = output_param

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
        if not isinstance(other, AnimatedGraphicsTask):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
