from backup_file_to_baidu_netdisk.utils.service_type_hint import generate_stubs,get_service
from backup_file_to_baidu_netdisk.controller import get_service_manager





if __name__ == "__main__":
    # generate_stubs()
    print(get_service_manager().check_service_index())
    print(get_service('TestService1'))