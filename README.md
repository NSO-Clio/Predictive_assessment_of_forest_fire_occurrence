# О проекте 🚀
Наша команда разработала сегментационную модель машинного обучения, способную по снимкам со спутников указанной территории и метеорологическим данным возвращать маску потенциальных пожаров в ближайший месяц.

#### Преимущества продукта:
* коэффициент корреляции Мэтьюса (MCC) >= 0.8
* реализован веб интерфейс
* простой в использовании программный модуль

## Стэк технологий 🗂

* **numpy**
* **pandas**
* scipy
* rasterio
* **catboost**
* opencv
 
# Быстрый старт 💥

Для начала нужно склонировать проект с Github'a:

```sh
git clone --no-checkout https://github.com/NSO-Clio/Predictive_assessment_of_forest_fire_occurrence
cd Predictive_assessment_of_forest_fire_occurrence
# если вам не нужна папка с jupyter ноутбуками (pipelines)
rm -r pipelines # для linux
rd /s /q pipelines # для windows
```

После нужно установить requirements:

```sh
pip install -r requirements.txt
```

# Команда 👨‍💻
* [Сусляков Семён](https://github.com/ssuslyakoff)
* [Андреасян Егор](https://github.com/EgorAndrik)
* [Вершинин Михаил](https://github.com/Rasdafar128)
* [Ротачёв Александр](https://github.com/Sasha2810)
