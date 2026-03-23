import sys
from pathlib import Path
from typing import  Optional, Type
from backup_file_to_baidu_netdisk.controller.main import get_service_manager,S,D,R

def generate_stubs(output_path: Optional[str] = None) -> None:
    """
    根据已注册的服务生成 .pyi 存根文件，其中包含 get_service 的精确重载。
    
    :param output_path: 输出的 .pyi 文件路径。若为 None，则自动生成与当前模块同名的 .pyi 文件。
    """
    manager = get_service_manager()
    services = manager.list_services()

    if not services:
        print("警告：没有注册任何服务，生成的存根文件将为空。")
        return

    # 确定输出路径
    if output_path is None:
        current_file = Path(__file__)
        output_path = (current_file.parent / 'service_type_hint.pyi').as_posix()  # 如 services.py -> services.pyi
  
        # 更健壮的做法是要求用户传递输出路径，或使用 __name__ 获取模块名
        # 此处简化处理

    # 收集所有用到的类型及其导入信息
    type_imports = {}  # 模块 -> 需要导入的类名/类型变量名列表
    current_module = __name__

    for service_name, ctx in services.items():
        for typ in (ctx["service_class"], ctx["service_dependency"], ctx["result_type"]):
            module = typ.__module__
            name = typ.__name__
            if module != current_module:
                type_imports.setdefault(module, set()).add(name)



    # 构建导入语句
    imports = [
        "from typing import overload, Literal, Type, Tuple",
        "",
    ]
    for module, names in type_imports.items():
        # 如果是当前模块的子模块，使用相对导入
        if module.startswith(current_module):
            relative = '.' + module[len(current_module):].lstrip('.')
            imports.append(f"from {relative} import {', '.join(sorted(names))}")
        else:
            imports.append(f"from {module} import {', '.join(sorted(names))}")

    # 添加对 S, D, R 的泛型导入
    imports.append(f"from ...dao.type_ import S, D, R")
    
    imports.append("")  # 空行分隔

    # 构建重载函数签名
    overload_lines = []
    for service_name, ctx in services.items():
        s_class = ctx["service_class"].__name__
        s_dep = ctx["service_dependency"].__name__
        s_result = ctx["result_type"].__name__
        overload_lines.append(
            f"@overload\n"
            f"def get_service(service_name: Literal[\"{service_name}\"]) -> Tuple[Type[{s_class}], Type[{s_dep}], Type[{s_result}]]: ..."
        )

    # 添加后备的泛型重载（用于未知服务名）
    overload_lines.append(
        f"@overload\n"
        "def get_service(service_name: str) -> Tuple[Type[S], Type[D], Type[R]]:\n"
        "   '''此重载用于未知服务名，如见此提示请检查服务是否注册,或联系管理员检查服务类型标注模块'''\n"
        "   ...\n"
    )

    # 组合全部内容
    content = "\n".join(imports + overload_lines)

    # 写入文件
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"成功生成存根文件: {output_path}")
