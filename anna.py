from clearml import Task
import functools
import inspect

def clearml_task(project_name, task_name=None, tags=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Определение имени задачи
            automatic_task_name = task_name or func.__name__
            # Создание задачи в ClearML
            task = Task.init(
                project_name=project_name,
                task_name=automatic_task_name,
                tags=tags or []
            )
            # Логирование параметров
            task.connect_configuration(
                {k: v for k, v in inspect.signature(func).parameters.items()},
                name="function_signature"
            )
            try:
                # Выполнение основной функции
                result = func(*args, **kwargs)
                # Логирование успешного выполнения
                task.get_logger().report_scalar(
                    title='Execution',
                    series='Success',
                    value=1
                )
                return result
            except Exception as e:
                # Логирование ошибок
                task.get_logger().report_scalar(
                    title='Execution',
                    series='Error',
                    value=1
                )
                task.get_logger().report_text(str(e))
                raise
        return wrapper
    return decorator
