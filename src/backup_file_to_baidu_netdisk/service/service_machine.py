from enum import Enum

from transitions.experimental.utils import with_model_definitions, add_transitions
from transitions import Machine




class State(Enum):
    NOT_STARTED = "未启动"
    STARTING = "启动中"
    RUNNING = "运行中"
    NORMAL_ENDING = "正常结束中"
    NORMAL_END = "正常结束"
    MANUAL_TERMINATING = "手动终止中"
    MANUAL_TERMINATED = "手动终止"
    ABNORMAL_TERMINATING = "异常终止中"
    ABNORMAL_TERMINATED = "异常终止"
    RUNNING_ABNORMAL = "运行异常"
    HANDLING_PAUSE_DEPENDENCIES = "程序正在处理暂停相关依赖"
    PAUSED = "暂停运行"
    RESUMING = "从暂停恢复中"


class ServiceMachineModel:
    def __init__(self,service_name:str):
        self.service_name = service_name
    state: State = State.NOT_STARTED
    @add_transitions({"source": State.NOT_STARTED, "dest": State.STARTING})
    def start(self):...

    @add_transitions({"source": State.STARTING, "dest": State.RUNNING})
    def started(self):...

    @add_transitions({"source": State.RUNNING, "dest": State.NORMAL_ENDING})
    def normal_end(self):...

    @add_transitions({"source": State.NORMAL_ENDING, "dest": State.NORMAL_END})
    def normal_ended(self):...

    @add_transitions({"source": State.RUNNING, "dest": State.MANUAL_TERMINATING})
    def manual_stop(self):...

    @add_transitions({"source": State.MANUAL_TERMINATING, "dest": State.MANUAL_TERMINATED})
    def manual_stopped(self):...

    @add_transitions({"source": State.RUNNING, "dest": State.ABNORMAL_TERMINATING})
    def abnormal_stop(self):...

    @add_transitions({"source": State.ABNORMAL_TERMINATING, "dest": State.ABNORMAL_TERMINATED})
    def abnormal_stopped(self):...

    @add_transitions({"source": State.RUNNING, "dest": State.RUNNING_ABNORMAL})
    def runtime_error(self):...


    @add_transitions({"source": [State.RUNNING_ABNORMAL, State.RUNNING], "dest": State.HANDLING_PAUSE_DEPENDENCIES})
    def pause(self):...

    @add_transitions({"source": [State.RUNNING_ABNORMAL, State.RUNNING, State.HANDLING_PAUSE_DEPENDENCIES], "dest": State.PAUSED})
    def pause_processed(self):...

    @add_transitions({"source": State.PAUSED, "dest": State.RESUMING})
    def resume(self):...

    @add_transitions({"source": State.RESUMING, "dest": State.RUNNING})
    def resumed(self):...

    @add_transitions({"source": State.RUNNING, "dest": State.NORMAL_ENDING})
    @add_transitions({"source": State.NORMAL_ENDING, "dest": State.NORMAL_END})
    @add_transitions({"source": State.NOT_STARTED, "dest": State.RUNNING})
    def next_stage(self):...
    @add_transitions({"source": [State.NORMAL_END, State.MANUAL_TERMINATED, State.ABNORMAL_TERMINATED, State.RUNNING_ABNORMAL], "dest": State.NOT_STARTED})
    def reset(self):...


@with_model_definitions  # don't forget to define your model with this decorator!
class MyMachine(Machine):
    pass


_service_machine = {}

def get_service_machine(service_name:str):
    if service_name not in _service_machine:
        _service_machine[service_name] = ServiceMachineModel(service_name)
        MyMachine(_service_machine[service_name], states=State, initial=_service_machine[service_name].state)
    return _service_machine[service_name]



 
