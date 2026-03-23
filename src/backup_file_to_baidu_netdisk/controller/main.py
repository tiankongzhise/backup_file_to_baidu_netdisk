from typing import  Type, TypedDict, Generic
from backup_file_to_baidu_netdisk.dao.type_ import S,D,R


class ServiceContext(TypedDict, Generic[S, D, R]):
    service_class:Type[S]
    service_dependency:Type[D]
    result_type:Type[R]

class ServiceManager:
    def __init__(self):
        self._services = {}
    
    def register_service(self,service_name:str,service_class:Type[S],service_dependency:Type[D],result_type:Type[R]):
        self._services[service_name] = ServiceContext(service_class=service_class,service_dependency=service_dependency,result_type=result_type)
    
    def list_services(self)->dict[str,dict[str,Type[S] | Type[D] | Type[R]]]:
        return self._services
    def get_service(self,service_name:str)->dict[str,Type[S] | Type[D] | Type[R]]:
        return self._services[service_name]
    

_service_manager = None

def get_service_manager():
    global _service_manager
    if _service_manager is None:
        _service_manager = ServiceManager()
    return _service_manager

def register_service(dependency_context:Type[D],result_type:Type[R]):
    def decorator(cls:Type[S]):
        service_manager = get_service_manager()
        service_manager.register_service(cls.__name__,cls,dependency_context,result_type)
        return cls
    return decorator


