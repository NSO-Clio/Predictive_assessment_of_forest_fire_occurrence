import rasterio
import numpy as np
import cv2
import os
import pandas as pd
from catboost import CatBoostClassifier
from scipy.ndimage import uniform_filter, maximum_filter, minimum_filter


class CatNet:
    def __init__(self) -> None:
        # Инициализация класса и загрузка обученной модели CatBoost из файла
        current_dir = os.getcwd()
        model_path = os.path.join(current_dir, 'model', 'CatBoostNet.cbm')
        
        self.model = CatBoostClassifier()
        self.model.load_model(model_path)
    
    def predict_segment(self, X: pd.DataFrame, shape_img: tuple[int, int], save_path: str = None) -> np.ndarray:
        """
        Предсказание сегментации на основе данных X и сохранение результата в файл (если указан путь).
        
        Аргументы:
        X -- DataFrame с предобработанными данными.
        shape_img -- Размеры исходного изображения (высота, ширина).
        save_path -- Путь для сохранения предсказанного изображения (опционально).
        
        Возвращает:
        y_pred -- Предсказанная маска сегментации.
        """
        y_pred = self.model.predict(X.to_numpy()).reshape(shape_img)
        if save_path is None:
            return y_pred
        cv2.imwrite(save_path, y_pred)
    
    def preproc(self, image_path: str, weather_data_path: str) -> tuple[pd.DataFrame, tuple[int, int]]:
        """
        Предобработка изображения и данных о погоде.
        
        Аргументы:
        image_path -- Путь к GeoTIFF-изображению.
        weather_data_path -- Путь к CSV-файлу с погодными данными.
        
        Возвращает:
        Данные после обработки в виде DataFrame и размеры изображения.
        """
        return (self.__process_image(image_path=image_path, weather_data_path=weather_data_path),
                self.__get_rgb_geotiff(image_path, r_band=1, g_band=2, b_band=3, ik_band=4, mask_band=5, chanel=1).shape[:2])
    
    def __process_image(self, image_path: str, weather_data_path: str) -> pd.DataFrame:
        """
        Обработка изображения и погодных данных для создания признаков.
        
        Аргументы:
        image_path -- Путь к GeoTIFF-изображению.
        weather_data_path -- Путь к CSV-файлу с погодными данными.
        
        Возвращает:
        df -- DataFrame с признаками, созданными на основе изображения и погодных данных.
        """
        weather = pd.read_csv(weather_data_path)
        weather = weather.iloc[weather.time.argmax()].drop("time").drop("Порывы ветра")

        image = self.__get_rgb_geotiff(image_path, r_band=1, g_band=2, b_band=3, ik_band=4, mask_band=5, chanel=1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Преобразование изображения в RGB
        ik = self.__get_rgb_geotiff(image_path, r_band=1, g_band=2, b_band=3, ik_band=4, mask_band=5, chanel=2)

        # Преобразование данных изображения в DataFrame
        data = {
            'R': image_rgb[:, :, 0].flatten(),         # Значение R канала
            'G': image_rgb[:, :, 1].flatten(),         # Значение G канала
            'B': image_rgb[:, :, 2].flatten(),         # Значение B канала
            'IK': ik.flatten(),
        }

        df = pd.DataFrame(data)
        for index in weather.index:
            df[index] = weather[index]
        
        # Радиусы для фильтров
        radiuses = np.arange(2, 10) ** 2
        data = [('R', image_rgb[:, :, 0]), ('G', image_rgb[:, :, 1]), ('B', image_rgb[:, :, 2]), ('IK', ik)]

        # Добавление минимальных значений R, G, B в радиусах ... пикселей
        for radius in radiuses:
            for color, channel in data:
                df[f'{color}_min_{radius}'] = minimum_filter(channel, size=2 * radius + 1, mode='reflect').flatten()
        df = df.copy()
    
        # Добавление максимальных значений R, G, B в радиусах ... пикселей
        for radius in radiuses:
            for color, channel in data:
                df[f'{color}_max_{radius}'] = maximum_filter(channel, size=2 * radius + 1, mode='reflect').flatten()
        df = df.copy()

        # Добавление усреднённых значений R, G, B в радиусах ... пикселей
        for radius in radiuses:
            for color, channel in data:
                df[f'{color}_mean_{radius}'] = uniform_filter(channel, size=2 * radius + 1, mode='reflect').flatten()
        return df.copy()
    
    @staticmethod
    def __get_rgb_geotiff(file_path: str, r_band: int = 1, g_band: int = 2, b_band: int = 3, 
                          ik_band: int = 4, mask_band: int = 5, chanel: int = 1) -> np.ndarray:
        """
        Извлечение данных из GeoTIFF-изображения и создание соответствующих каналов.
        
        Аргументы:
        file_path -- Путь к GeoTIFF-изображению.
        r_band -- Канал для красного спектра.
        g_band -- Канал для зелёного спектра.
        b_band -- Канал для синего спектра.
        ik_band -- Канал для ИК спектра.
        mask_band -- Канал для маски.
        chanel -- Определяет, какой канал вернуть (1 - RGB, 2 - IK, 3 - маска).
        
        Возвращает:
        photo -- Изображение в формате numpy массива.
        """
        try:
            with rasterio.open(file_path) as src:
                red = src.read(r_band)
                green = src.read(g_band)
                blue = src.read(b_band)
                ik = src.read(ik_band)
                mask = src.read(mask_band)

                if chanel == 1:
                    photo = np.clip(np.stack([red, green, blue], axis=-1).astype(float) * 3, 0, 255).astype(np.uint8)  # Отрисовка всего изображения
                elif chanel == 2:
                    photo = np.stack([ik], axis=-1)  # Отрисовка ИК-слоя изображения
                elif chanel == 3:
                    photo = np.stack([mask], axis=-1) * 255  # Отрисовка маски изображения
                photo = photo.astype(np.uint8)
                return photo
        except Exception as e:
            print(f'Ошибка: {e}')
            return np.array([])
