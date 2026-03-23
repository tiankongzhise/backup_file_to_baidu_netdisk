from typing import overload, Literal, Type, Tuple

from test.t2 import TestDependency1, TestResult1, TestService1
from test.x.t3 import TestDependency, TestResult, TestService2
from ..type_ import S, D, R

@overload
def get_service(service_name: Literal["TestService1"]) -> Tuple[Type[TestService1], Type[TestDependency1], Type[TestResult1]]: ...
@overload
def get_service(service_name: Literal["TestService2"]) -> Tuple[Type[TestService2], Type[TestDependency], Type[TestResult]]: ...
@overload
def get_service(service_name: str) -> Tuple[Type[S], Type[D], Type[R]]:
   '''此重载用于未知服务名，如见此提示请检查服务是否注册,或联系管理员检查服务类型标注模块'''
   ...
