import random
import tensorflow as tf
import numpy as np
import pandas as pd
import numpy as np
from tensorflow.keras import layers, models
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# Определяем количество примеров в датасете
num_samples = 100000

# Список пар чисел и результатов
data = []
res = []

# Генерация случайных пар чисел и результатов
for i in range(num_samples):
    num1 = random.randint(0, 100)
    num2 = random.randint(0, 100)

    # Вычисление результата
    operation_idx = random.randint(0, 3)
    if operation_idx == 0:
        result = num1 + num2
    elif operation_idx == 1:
        result = num1 - num2
    elif operation_idx == 2:
        result = num1 * num2
    elif operation_idx == 3:
        if num2 != 0:
            result = num1 / num2
        else:
            result = 0  # или другое значение, обозначающее ошибку

    # Добавление пары чисел и результата в датасет
    data.append([num1, num2, operation_idx])
    res.append([result])

# Создаем словарь с данными и результатами
dataset = {
    'data': data,
    'result': res
}

print(dataset)


# Загрузка датасета
data = pd.DataFrame(dataset['data'], columns=["num1", "num2", "operation_idx"]) # Создание таблички с данными, которые послужат признаками (входные данные)
result = pd.DataFrame(dataset['result'], columns=["result"]) # Создание таблички с данными, которые послужат примером правильного ответа (выходные данные)

calc_df = pd.concat([data, result], axis=1) #объединение столбцов data и target

calc_df.head(-30) #Вывод первых 30 последних значений



# Преобразуем данные в тензоры
X = np.array(data).reshape(-1, 3)  # Преобразуем в (num_samples, 3)
y = np.array(res)

# Нормализация данных
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

X_normalized = scaler_X.fit_transform(X)  # Нормализуем X
y_normalized = scaler_y.fit_transform(y)  # Нормализуем y

# Разделение данных
X_train, X_test, y_train, y_test = train_test_split(X_normalized, y_normalized, test_size=0.2, random_state=42)

# Создание модели
model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(3,)))  # 3 входа: num1, num2, operation_idx
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(1))  # Выходной слой для регрессии

# Компиляция модели
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Обучение модели
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_data=(X_test, y_test)
)

# Оценка модели
test_loss, test_mae = model.evaluate(X_test, y_test)
print(f"Test Loss: {test_loss}, Test MAE: {test_mae}")