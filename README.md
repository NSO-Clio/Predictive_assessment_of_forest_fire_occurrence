# О проекте 🚀
Наша команда разработала сегментационную модель машинного обучения, способную по снимкам со спутников указанной территории и метеорологическим данным возвращать маску потенциальных пожаров в ближайший месяц.

#### Преимущества продукта:
* коэффициент корреляции Мэтьюса (MCC) >= 0.8
* реализован веб интерфейс
* простой в использовании программный модуль

## Стэк технологий 🗂

* numpy
* pandas
* scipy
* rasterio
* catboost
* opencv
 
## Быстрый старт 💥

#### Скачать проект

```sh
git clone --no-checkout https://github.com/NSO-Clio/Predictive_assessment_of_forest_fire_occurrence
cd Predictive_assessment_of_forest_fire_occurrence
# если вам не нужна папка с jupyter ноутбуками (pipelines)
rm -r pipelines # для linux
rd /s /q pipelines # для windows
```

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```
5. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
