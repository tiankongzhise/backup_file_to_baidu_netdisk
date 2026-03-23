from backup_file_to_baidu_netdisk.controller.main import get_service_manager,register_service

from test.t2 import TestService1
from dataclasses import dataclass
from typing import TypedDict

class TestDependency(TypedDict):
    b:int

@dataclass
class TestResult:
    ...
@register_service(TestDependency,TestResult)
class TestService2():
    def __init__(self,dependency:TestDependency):
        self.dependency = dependency
        self.a = dependency['b']





if __name__ == "__main__":
    # create_service_type_hint_file(get_service_manager)
    
    # print(get_module_path_relative_to_root(TestService2))
    # generate_stubs()
    # get_service('TestService2')
    ...