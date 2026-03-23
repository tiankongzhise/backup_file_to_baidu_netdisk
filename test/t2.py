from backup_file_to_baidu_netdisk.controller.main import register_service,get_service_manager
from dataclasses import dataclass
from typing import TypedDict
@dataclass
class TestResult1:
    ...

class TestDependency1(TypedDict):
    a:int
class TestService1:
    def __init__(self,dependency:TestDependency1):
        self.dependency = dependency
        self.a = 1


TestService1 = register_service(TestDependency1,TestResult1,2)(TestService1)

if __name__ == "__main__":
    service_manager = get_service_manager()
    print(service_manager.list_services())
    t2 = TestService1(TestDependency1(a=1))
    print(t2.a)