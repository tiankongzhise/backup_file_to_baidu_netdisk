from ..domain import ServicePort
from ..utils.type_ import ActionResult
from .service_register import register_service
from typing import Any,Never
from ..utils.wrap import class_method_action_result_wrapper
@register_service(type[Never],dict,3)
class BackupService(ServicePort):
    @class_method_action_result_wrapper
    def start(self)->ActionResult[Any]:
        ...
    
    @class_method_action_result_wrapper
    def stop(self)->ActionResult[Any]:
        ...
    
    @class_method_action_result_wrapper
    def pause(self)->ActionResult[Any]:
        ...
    
    @class_method_action_result_wrapper
    def resume(self)->ActionResult[Any]:
        ...