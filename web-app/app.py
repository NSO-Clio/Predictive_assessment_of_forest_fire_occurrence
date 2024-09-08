from flask import Flask, render_template, request
import pandas as pd
from PIL import Image
from pathlib import Path
import os
from model import CatNet

application = Flask(__name__, template_folder='templates')
model = CatNet()

@application.route('/')
def home_page() -> str:
    return render_template('index.html')

@application.route('/upload', methods=['POST'])
def save_info() -> str:
    information = "bad"
    image = request.files.get('image')
    csv_file = request.files.get('csv')

    # Проверяем, существует ли папка, если нет - создаем
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    if image and csv_file:
        # Сохраняем загруженные файлы в папку uploads
        image_path = os.path.join("uploads", image.filename)
        csv_path = os.path.join("uploads", csv_file.filename)
        
        image.save(image_path)
        csv_file.save(csv_path)

        # Предсказание модели
        try:
            model.predict_segment(  
                *model.preproc(image_path=image_path, weather_data_path=csv_path), 
                save_path= f"static/result.png"
            )
            information = f"../static/result.png"
        except Exception as e:
            print(f"Ошибка при предсказании модели: {e}")
            information = "Ошибка"

    # Возвращаем шаблон с результатами
    return render_template('index.html', information=information)

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=5000)
