from typing import Type
from backup_file_to_baidu_netdisk.controller.main import get_service_manager,S,D,R
def get_service(service_name:str)->tuple[Type[S],Type[D],Type[R]]:
    service_manager = get_service_manager()
    service_context = service_manager.get_service(service_name)
    return service_context['service_class'],service_context['service_dependency'],service_context['result_type']