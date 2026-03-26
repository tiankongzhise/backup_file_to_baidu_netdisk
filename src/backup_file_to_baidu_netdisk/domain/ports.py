

from typing import Any, Protocol
from ..utils.type_ import ActionResult
class ServicePort(Protocol):
    def start(self)->ActionResult[Any]:
        ...
    
    def stop(self)->ActionResult[Any]:
        ...
    
    def pause(self)->ActionResult[Any]:
        ...
    
    def resume(self)->ActionResult[Any]:
        ...
    

class ConfigPort(Protocol):
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
    
    def delete_runtime_environment(self,environment_name:str|list[str])->ActionResult[Any]:
        ...
    
    def get_runtime_environment_list(self)->ActionResult[Any]:
        ...