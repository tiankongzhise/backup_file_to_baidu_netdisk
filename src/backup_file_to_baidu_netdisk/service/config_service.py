from ..domain import ServicePort,ConfigPort
from ..utils.type_ import ActionResult
from typing import Any
from .service_register import register_service
from typing import Never
from ..utils.wrap import class_method_action_result_wrapper

@register_service(type[Never],dict,1)
class ConfigService(ConfigPort):

    def get_config(self)->ActionResult[Any]:
        ...
    
    def register_runtime_environment(self)->ActionResult[Any]:
        ...
    
    def unregister_runtime_environment(self)->ActionResult[Any]:
        ...
    
    def get_runtime_environment(self,environment_name:str,default_value:Any = None)->ActionResult[Any]:
        ...
    
    def set_runtime_environment(self,environment:dict[str,Any])->ActionResult[Any]:
        ...
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