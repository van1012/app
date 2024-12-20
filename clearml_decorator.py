from clearml import Task #Импортируем объект Task из библиотеки ClearML, который позволяет создавать задачи и логировать данные.
import functools #Модуль для создания декораторов.
import inspect #Модуль для анализа функций, их параметров и структуры.

def clearml_task(project_name, task_name=None, tags=None): #Основная функция-декоратор принимает три параметра:
    def decorator(func): #Вложенная функция-декоратор, которая оборачивает целевую функцию func (ту, которую мы хотим декорировать).
        @functools.wraps(func) #Сохраняет метаданные оригинальной функции (например, имя, документацию).
        def wrapper(*args, **kwargs): #Обёртка для выполнения декорируемой функции с дополнительной логикой.
            # Определение имени задачи
            automatic_task_name = task_name or func.__name__ #•	Если имя задачи (task_name) не указано, автоматически используется имя функции (func.__name__).
            # Создание задачи в ClearML
            task = Task.init( #Создаёт задачу в ClearML
                project_name=project_name, #Указывает, в каком проекте создать задачу.
                task_name=automatic_task_name, #Имя задачи.
                tags=tags or [] #Список меток для задачи.
            )
            # Логирование параметров
            task.connect_configuration(
                {k: v for k, v in inspect.signature(func).parameters.items()}, #•	Используется inspect.signature, чтобы получить параметры функции
                name="function_signature" #Логируются параметры функции (имена и значения по умолчанию) как "конфигурация задачи".
            )
            try:
                # Выполнение основной функции
                result = func(*args, **kwargs) #Вызывается оригинальная функция с переданными аргументами args и kwargs.
                                                #Результат выполнения сохраняется в переменную result.

                # Логирование успешного выполнения
                task.get_logger().report_scalar(
                    title='Execution', #Категория лога.
                    series='Success', #Тип события (в данном случае "успех").
                    value=1, #Указывает, что задача выполнена успешно.
                    iteration=0 #Указывается нулевая итерация, так как здесь нет циклов.
                )


                return result
            except Exception as e:
                # Логирование ошибок
                task.get_logger().report_scalar(
                    title='Execution', #
                    series='Success',
                    value=1,
                    iteration=0  # добавляем параметр iteration
                )
                task.get_logger().report_text(str(e))
                raise
        return wrapper
    return decorator
