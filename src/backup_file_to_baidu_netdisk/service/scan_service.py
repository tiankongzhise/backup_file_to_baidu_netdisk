from ..domain import ServicePort
from ..utils.type_ import ActionResult
from ..utils.wrap import class_method_action_result_wrapper
from typing import Any,Literal
from .service_register import register_service
from typing import Never

@register_service(type[Never],dict,2)
class ScanService(ServicePort):
    @class_method_action_result_wrapper
    def start(self)->ActionResult[str|Exception]:...
    
    @class_method_action_result_wrapper
    def stop(self)->ActionResult[str|Exception]:...
    
    @class_method_action_result_wrapper
    def pause(self)->ActionResult[Any]:
        ...
    
    @class_method_action_result_wrapper
    def resume(self)->ActionResult[Any]:
        ...
    
    @class_method_action_result_wrapper
    def get_status(self):
        ...