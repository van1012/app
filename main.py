from clearml_decorator import clearml_task

@clearml_task(
    project_name="ML_Lab_Experiments",
    task_name="Data_Processing",
    tags=["preprocessing", "v1"]
)
def process_data(input_file, threshold=0.5):
    # Пример обработки данных
    import pandas as pd
    data = pd.read_csv(input_file) #Чтение CSV-файла
    processed_data = data[data['score'] > threshold] #Фильтрация данных
    return processed_data #Возвращает обработанные данныеpe
#o	Принимает файл CSV и пороговое значение threshold.
#Загружает данные с помощью Pandas.
#Фильтрует строки, где значение в столбце score превышает threshold.

# Вызов функции
if __name__ == "__main__":
    result = process_data('dataset.csv', threshold=0.7)
    print(result)
#При выполнении программы:
#1.	Создаётся задача ClearML с логированием.
#2.	Загружается файл dataset.csv.
#3.	Обрабатываются данные (фильтрация по порогу threshold).
#4.	Результат обработки выводится на экран.




