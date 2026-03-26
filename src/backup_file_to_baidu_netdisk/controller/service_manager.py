from ..service import get_service_register_manager
from ..domain import ServicePort,ServiceRuntimeError
from ..utils.type_ import ActionResult
from typing import Literal
class ServiceManager:
    def __init__(self):
        self._service_register_manager = get_service_register_manager()
        self._services:dict[str,ServicePort] = {}
        self._register_services = self._service_register_manager.list_services()
        self.is_stop_all_when_error = False
    
    def _start_service(self,service_name:str):
        print(f'start_service: {service_name}')
        ar = self._services[service_name].start()
        print(ar)
        if not ar.status:
            if self.is_stop_all_when_error:
                self.stop_service('all')
            raise ServiceRuntimeError(f'{self.__class__.__name__}->start_service失败: 服务{service_name}启动失败: {ar.context}')
        return ar
    def _get_service_class(self,service_name:str):
        if service_name not in self._register_services:
            if self.is_stop_all_when_error:
                self.stop_service('all')
            raise ServiceRuntimeError(f'{self.__class__.__name__}->_get_service_class失败: 服务{service_name}不存在')
        return self._register_services[service_name]['service_class']
    
    def _create_service_instance(self,service_name:str):
        if service_name not in self._services:
            self._services[service_name] = self._get_service_class(service_name)()
        return self._services[service_name]
    
    def _get_service_instance(self,service_name:str):
        if service_name not in self._services:
            if self.is_stop_all_when_error:
                self.stop_service('all')
            raise ServiceRuntimeError(f'{self.__class__.__name__}->_get_service_instance失败: 服务{service_name}不存在')
        return self._services[service_name]
    
    def _stop_service(self,service_name:str):
        service = self._get_service_instance(service_name)
        ar = service.stop()
        if not ar.status:
            raise ServiceRuntimeError(f'{self.__class__.__name__}->_stop_service失败: 服务{service_name}停止失败: {ar.context}')
        return ar

    def _pause_service(self,service_name:str):
        service = self._get_service_instance(service_name)
        ar = service.pause()
        if not ar.status:
            raise ServiceRuntimeError(f'{self.__class__.__name__}->_pause_service失败: 服务{service_name}暂停失败: {ar.context}')
        return ar

    def _resume_service(self,service_name:str):
        service = self._get_service_instance(service_name)
        ar = service.resume()
        if not ar.status:
            raise ServiceRuntimeError(f'{self.__class__.__name__}->_resume_service失败: 服务{service_name}恢复失败: {ar.context}')
        return ar

    def start_service(self,service_name:Literal['all']|str|list[str],is_stap_all:bool = False):
        self.is_stop_all_when_error = is_stap_all
        if service_name == 'all':
            for service_name,_ in self._register_services.items():
                self._create_service_instance(service_name)
                self._start_service(service_name)
        elif isinstance(service_name,str):
            self._create_service_instance(service_name)
            self._start_service(service_name)
        else:
            for service_name in service_name:
                self._create_service_instance(service_name)
                self._start_service(service_name)
    
    def stop_service(self,service_name:Literal['all']|str|list[str]):
        if service_name == 'all':
            for service_name,_ in self._services.items():
                self._stop_service(service_name)
        elif isinstance(service_name,str):
            self._stop_service(service_name)
        else:
            for service_name in service_name:
                self._stop_service(service_name)
    
    def pause_service(self,service_name:Literal['all']|str|list[str]):
        if service_name == 'all':
            for service_name,_ in self._services.items():
                self._pause_service(service_name)
        elif isinstance(service_name,str):
            self._pause_service(service_name)
        else:
            for service_name in service_name:
                self._pause_service(service_name)
    
    def resume_service(self,service_name:Literal['all']|str|list[str]):
        if service_name == 'all':
            for service_name,_ in self._services.items():
                self._resume_service(service_name)
        elif isinstance(service_name,str):
            self._resume_service(service_name)
        else:
            for service_name in service_name:
                self._resume_service(service_name)

_service_manager = None

def get_service_manager():
    global _service_manager
    if _service_manager is None:
        _service_manager = ServiceManager()
    return _service_manager