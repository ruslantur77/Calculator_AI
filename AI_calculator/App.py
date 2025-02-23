from sanic_cors import CORS
from sanic import Sanic, response
from tensorflow.keras import layers, models
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import ast
app = Sanic("CalculatorApp")
CORS(app)


# Загрузка модели и данных
model = load_model(
    './Model/AI_calculator.h5',
    custom_objects={'mse': 'mean_squared_error'}
)

dataset = pd.read_csv('./Model/dataset.csv')
data = dataset['data'].apply(ast.literal_eval)
result = dataset['result'].apply(ast.literal_eval)
data = pd.DataFrame(data.tolist(), columns=['num1','num2','operation_idx'], dtype=np.float32)
result = pd.DataFrame(result.tolist(), columns=['result'])

# Нормализация данных
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()
X_normalized = scaler_X.fit_transform(data)
y_normalized = scaler_y.fit_transform(result)

@app.route("/")
async def index(request):
    return await response.file("./frontend/index.html")

app.static("/static", "./frontend/static")


@app.route("/Calc", methods=["POST"])
async def Calc(request):
    try:
        data = request.json
        num1 = float(data['num1'])
        num2 = float(data['num2'])
        operation = data['operation']
        
        operations = {'+': 0, '-': 1, '*': 2, '/': 3}
        operation_idx = operations.get(operation, 0)

        # Предсказание
        input_data = np.array([[num1, num2, operation_idx]])
        input_normalized = scaler_X.transform(input_data)
        prediction = model.predict(input_normalized)
        predicted_result = scaler_y.inverse_transform(prediction)[0][0]

        # Реальный расчет
        calc_operations = {
            '+': lambda a,b: a+b,
            '-': lambda a,b: a-b,
            '*': lambda a,b: a*b,
            '/': lambda a,b: a/b if b !=0 else 0
        }
        real_result = calc_operations[operation](num1, num2)

       
        return response.json({
            "predicted": float(round(predicted_result, 4)),  
            "real": float(round(real_result, 4))             
        })
    except Exception as e:
        return response.json({"error": str(e)}, status=400)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001, debug=True)