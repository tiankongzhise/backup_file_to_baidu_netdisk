import inspect
import functools
from .type_ import ActionResult

def class_method_action_result_wrapper(func):
    """装饰器：在方法调用时打印类名和方法名"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 获取方法名
        method_name = func.__name__

        # 尝试获取类名
        class_name = None
        if args:
            # 第一个参数可能是 self 或 cls
            first_arg = args[0]
            if hasattr(first_arg, '__class__'):
                # 实例方法：self.__class__.__name__
                class_name = first_arg.__class__.__name__
            elif hasattr(first_arg, '__name__'):
                # 类方法：cls.__name__
                class_name = first_arg.__name__
        if class_name is None:
            # 备用方案：通过 inspect 从栈帧中获取类名（适用于静态方法）
            frame = inspect.currentframe()
            if frame is not None:
                try:
                    # 向上找一层，获取调用者的局部变量，可能包含 'self' 或 'cls'
                    outer_frame = frame.f_back
                    # 如果外层局部变量中有 'self'，尝试获取其类名
                    if outer_frame is not None and 'self' in outer_frame.f_locals:
                        class_name = outer_frame.f_locals['self'].__class__.__name__
                    elif outer_frame is not None and 'cls' in outer_frame.f_locals:
                        class_name = outer_frame.f_locals['cls'].__name__
                finally:
                    del frame  # 避免循环引用

        # 如果仍然没有类名，则使用默认值
        if class_name is None:
            class_name = "UnknownClass"

        print(f"调用方法：{class_name}.{method_name}")
        try:
            result = func(*args, **kwargs)
            return ActionResult(status=True,context={'message':f'{class_name}->{method_name}成功','result':result})
        except Exception as e:
            return ActionResult(status=False,context={'message':f'{class_name}->{method_name}失败','error':e})

    return wrapper