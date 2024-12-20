from clearml import Task #Импортируем класс Task из библиотеки ClearML, чтобы создавать и управлять задачами.
import functools #Загружаем библиотеку functools, которая содержит полезные инструменты для работы с функциями, включая декораторы.
import inspect #Импортируем модуль inspect, чтобы получать информацию о функциях (например, их параметры).

def clearml_task(project_name, task_name=None, tags=None): #Определяем функцию-декоратор, которая принимает( имя проекта в ClearML,имя задачи (опционально),список тегов для задачи (опционально))
    def decorator(func): #Определяем вложенную функцию decorator, которая оборачивает целевую функцию func.
        @functools.wraps(func) #Используем functools.wraps, чтобы сохранить метаданные исходной функции (например, её имя).
        def wrapper(*args, **kwargs): #Создаем функцию wrapper, которая выполняет дополнительную логику вокруг вызова целевой функции.

            # Определение имени задачи. Если task_name не указано, используем имя функции.
            automatic_task_name = task_name or func.__name__

            # Создание задачи в ClearML с помощью Task.init
            task = Task.init(
                project_name=project_name,
                task_name=automatic_task_name,
                tags=tags or []
            )
            # Логирование параметров
            task.connect_configuration( #Логируем эти параметры в ClearML.
                {k: v for k, v in inspect.signature(func).parameters.items()}, #Получаем параметры функции.
                name="function_signature"
            )
            try: #Пытаемся выполнить целевую функцию.
                # Выполнение основной функции
                result = func(*args, **kwargs) #Вызываем функцию с её аргументами.
                # Логирование успешного выполнения
                task.get_logger().report_scalar( #Логируем успешное выполнение.
                    title='Execution',
                    series='Success',
                    value=1
                )
                return result
            except Exception as e: #Если возникает ошибка, логируем её текст и помечаем задачу как неуспешную.
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
