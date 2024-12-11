from clearml_decorator import clearml_task

@clearml_task(
    project_name="ML_Lab_Experiments",
    task_name="Data_Processing",
    tags=["preprocessing", "v1"]
)
def process_data(input_file, threshold=0.5):
    # Пример обработки данных
    import pandas as pd
    data = pd.read_csv(input_file)
    processed_data = data[data['score'] > threshold]
    return processed_data

# Вызов функции
if __name__ == "__main__":
    result = process_data('dataset.csv', threshold=0.7)
    #result = process_data('C:/Users/Этот компьютер/Рабочий стол/dataset.csv', threshold=0.7)
    print(result)



