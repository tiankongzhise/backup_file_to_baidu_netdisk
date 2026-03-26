from typing import  Literal, Type, TypedDict, Generic
from backup_file_to_baidu_netdisk.utils.type_ import S,D,R
from collections import defaultdict


class ServiceContext(TypedDict, Generic[S, D, R]):
    service_class:Type[S]
    service_dependency:Type[D]
    result_type:Type[R]
    run_index:int



class ServiceRegisterManager:
    def __init__(self):
        self._services = {}
        self._service_run_index = defaultdict(list)
    
    def register_service(self,service_name:str,service_class:Type[S],service_dependency:Type[D],result_type:Type[R],run_index:int):
        self._services[service_name] = ServiceContext(run_index=run_index,service_class=service_class,service_dependency=service_dependency,result_type=result_type)
        self._service_run_index[run_index].append(service_name)

    def list_services(self)->dict[str,dict[str,Type[S] | Type[D] | Type[R]]]:
        result = {}
        index = sorted(self._service_run_index.keys())
        for i in index:
            for service_name in self._service_run_index[i]:
                result[service_name] = self.get_service(service_name)
        return result

    def get_service(self,service_name:str)->dict[str,Type[S] | Type[D] | Type[R]]:
        return self._services[service_name]
    
    def check_service_index(self)->Literal[True]|Warning:
        """检查服务索引是否存在重复,若存在则返回Warning,否则返回True."""
        for key,value in self._service_run_index.items():
            if len(value) > 1:
                return Warning(f"服务索引{key}存在多个服务: {value}")
        return True
    def unregister_service(self,service_name:str)->Literal[True]|Warning:
        """注销服务,若服务不存在则返回Warning,否则返回True."""
        if service_name not in self._services:
            return Warning(f"服务{service_name}不存在")
        service_context = self._services[service_name]
        self._service_run_index[service_context['run_index']].remove(service_name)
        del self._services[service_name]
        return True
    def update_service_info(self,service_name:str,service_class:Type[S],service_dependency:Type[D],result_type:Type[R],run_index:int)->dict[str,Type[S] | Type[D] | Type[R]]:
        """更新服务信息,若服务不存在则返回创建服务,否则返回更新后的服务信息."""
        if service_name not in self._services:
            self.register_service(service_name,service_class,service_dependency,result_type,run_index)
            return self.get_service(service_name)
        else:
            service_context = self._services[service_name]
            self._service_run_index[service_context['run_index']].remove(service_name)
            self._services[service_name] = ServiceContext(run_index=run_index,service_class=service_class,service_dependency=service_dependency,result_type=result_type)
            self._service_run_index[run_index].append(service_name)
            return self.get_service(service_name)
    


_service_register_manager = None

def get_service_register_manager():
    global _service_register_manager
    if _service_register_manager is None:
        _service_register_manager = ServiceRegisterManager()
    return _service_register_manager

def register_service(dependency_context:Type[D],result_type:Type[R],run_index:int):
    def decorator(cls:Type[S]):
        service_register_manager = get_service_register_manager()
        service_register_manager.register_service(cls.__name__,cls,dependency_context,result_type,run_index)
        return cls
    return decorator


