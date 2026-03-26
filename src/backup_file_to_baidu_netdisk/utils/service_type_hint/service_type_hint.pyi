from typing import overload, Literal, Type, Tuple

from backup_file_to_baidu_netdisk.service.config_service import ConfigService
from builtins import dict, type
from backup_file_to_baidu_netdisk.service.scan_service import ScanService
from backup_file_to_baidu_netdisk.service.backup_service import BackupService
from ..type_ import S, D, R

@overload
def get_service(service_name: Literal["ConfigService"]) -> Tuple[Type[ConfigService], Type[type], Type[dict]]: ...
@overload
def get_service(service_name: Literal["ScanService"]) -> Tuple[Type[ScanService], Type[type], Type[dict]]: ...
@overload
def get_service(service_name: Literal["BackupService"]) -> Tuple[Type[BackupService], Type[type], Type[dict]]: ...
@overload
def get_service(service_name: str) -> Tuple[Type[S], Type[D], Type[R]]:
   '''此重载用于未知服务名，如见此提示请检查服务是否注册,或联系管理员检查服务类型标注模块'''
   ...
