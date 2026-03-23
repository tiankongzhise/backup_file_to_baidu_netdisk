from pathlib import Path
import json
from backup_file_to_baidu_netdisk.utils import breanch_time
from typing import Any

target_path = r"D:\Program Files"
scan_temp_path = r".\temp_data\scan1.json"
scan_temp_path_2 = r".\temp_data\scan2.json"

def create_report(data:dict[str,dict[str,Any]]):
    result = {
        'root_object':0,
        'file_object':0,
        'dir_object':0,
        'total_object':0,
        'total_size':0
    }
    for key, value in data.items():
        # breakpoint()
        result['total_object'] += value['object_count']
        result['total_size'] += value['size']
        result['root_object'] += 1
        result['file_object'] += value['file_count']
        result['dir_object'] += value['dir_count']
        result[key]={
            'object_count': value['object_count'],
            'file_count': value['file_count'],
            'dir_count': value['dir_count'],
            'size': value['size'],
        }
    return result

def scan_root_path(root_path:Path):
    object_details = []
    for object in root_path.iterdir():
        object_details.append(object)
    return object_details

def add_root_object_details(root_object_details:list[Path], processed_path:list[Path]):
    diff_result = list(set(root_object_details) - set(processed_path))
    return diff_result


def get_child_object_info(object:Path):
    return {
                "name": object.name,
                'object_type': object.suffix if object.is_file() else 'dir',
                "path": object.resolve().as_posix(),
                "size": object.stat().st_size if object.is_file() else 0,
                "modified_time": object.stat().st_mtime,
                "created_time": object.stat().st_ctime,
                "access_time": object.stat().st_atime,
                "is_file": object.is_file(),
                "is_dir": object.is_dir(),
            }
def get_parent_object_info(parent_path:Path,details:list[dict],object_count:int,file_count:int,dir_count:int,size:int):
    return {
        "object_path": parent_path.resolve().as_posix(),
        "details": sorted(details, key=lambda x: x["path"]),
        "object_count": object_count,
        "file_count": file_count,
        "dir_count": dir_count,
        "size": size,
    }
def get_root_iterdir_object_info(iterdir_object:list[Path]):
    temp_list = []
    object_count = 0
    file_count = 0
    dir_count = 0
    size = 0
    for object in iterdir_object:
        object_count += 1
        if object.is_file():
            file_count += 1
        else:
            dir_count += 1
        size += object.stat().st_size if object.is_file() else 0
        temp_list.append(get_child_object_info(object))
    return get_parent_object_info(iterdir_object[0], temp_list, object_count, file_count, dir_count, size)

def scan_target_path(target_path:str):
    local_target_path = Path(target_path)
    result = {}
    processed_path = []
    for root_path in local_target_path.iterdir():
        temp_list = []
        object_count = 0
        file_count = 0
        dir_count = 0
        size = 0
        for object in root_path.rglob("*"):
            object_count += 1
            if object.is_file():
                file_count += 1
            else:
                dir_count += 1
            size += object.stat().st_size if object.is_file() else 0
            temp_path = object.resolve().as_posix()
            processed_path.append(temp_path)
            temp_list.append(get_child_object_info(object))
        result[root_path.name] = get_parent_object_info(root_path, temp_list, object_count, file_count, dir_count, size)
    root_object_details = scan_root_path(local_target_path)
    diff_result = add_root_object_details(root_object_details, processed_path)
    result[local_target_path.name] = get_root_iterdir_object_info(diff_result)

    temp_file_path = Path(scan_temp_path)
    temp_file_path.parent.mkdir(parents=True, exist_ok=True)
    report = create_report(result)
    save_dict = {
        'report': report,
        **result,
    }
    with open(temp_file_path, "w") as f:
        json.dump(save_dict, f)
    # print(f"scan_target_path result: {result}")
    return create_report(result)

def scan_target_path_2(target_path:str):
    path = Path(target_path)
    result = {
        'file_object':0,
        'dir_object':0,
        'total_object':0,
        'total_size':0,
        'details':[]
    }
    for root_path in path.rglob("*"):
        result['total_object'] += 1
        if root_path.is_file():
            result['total_size'] += root_path.stat().st_size
            result['file_object'] += 1
        else:
            result['dir_object'] += 1
        result['details'].append({
            'path': root_path.resolve().as_posix(),
        })
    temp_file_path = Path(scan_temp_path_2)
    temp_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(temp_file_path, "w") as f:
        json.dump(result, f)
    return result

def compare_scan_result(result1:str, result2:str):
    with open(result1, "r") as f:
        result1 = json.load(f)
    with open(result2, "r") as f:
        result2 = json.load(f)
    r1_details = []
    for key, value in result1.items():
        # r1_details.append(value['object_path'])
        if key == 'report':
            continue
        r1_details.extend([ temp_dict['path'] for temp_dict in value['details']])
    r2_details = [ temp_dict['path'] for temp_dict in result2['details']]
    root_str = Path(target_path).resolve().as_posix()
    print(f'is root_str in r1_details: {root_str in r1_details}')
    print(f'is root_str in r2_details: {root_str in r2_details}')
    print(f"r1_details: {len(r1_details)}, r2_details: {len(r2_details)}")
    diff = set(r2_details) - set(r1_details)
    return diff

if __name__ == "__main__":
    with breanch_time("scan_target_path"):
        result = scan_target_path(target_path)
        print(result)
    # with breanch_time("scan_target_path_2"):
    #     result = scan_target_path_2(target_path)
    #     result.pop('details')
    #     print(result)
    with breanch_time("compare_scan_result"):
        diff = compare_scan_result(scan_temp_path, scan_temp_path_2)
        for index, item in enumerate(diff):
            temp_path = Path(item)
            print(f"index: {index},type is {'file' if temp_path.is_file() else 'dir'}, item: {temp_path}")
