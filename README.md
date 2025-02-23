AI Calculator - a calculator that runs on a trained CNN model. It is enough to enter 2 numbers, select a sign and the result of the trained calculator and the real result will appear.

In the Model.py you can see how the model was trained with dataset. Dataset which contains pairs of numbers, operation number and result. Web app was made with web framework Sanic which offers asynchrony.

To get started, you need to:

Install packages from requirements.txt:
```
pip install -r AI_calculator/requirements.txt
```
Then launch App.py and open in browser:
```
http://localhost:9001/
```
