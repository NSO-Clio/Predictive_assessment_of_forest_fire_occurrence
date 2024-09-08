import argparse
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from meteostat import Point, Daily

team_name = "CLIO"


def call_api(lat, lng, date):
    results_dict = {}
    date_sp = date.split('-')
    y, m, d = int(date_sp[0]), int(date_sp[1]), int(date_sp[2])
    end = datetime(y, m, d)

    start = end - timedelta(weeks=2)
    # Create Point for Vancouver, BC
    place = Point(lat, lng)

    # Get daily data for 2018
    data = Daily(place, start, end)
    data = data.fetch()
    data = data.reset_index(drop=True)

    results_dict = data.to_dict()
    return results_dict



# Функция для сохранения результатов в JSON файл
def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, help="Широта")
    parser.add_argument("--lng", type=float, help="Долгота")
    parser.add_argument("--date", type=str, help="Дата в формате YYYY-MM-DD")
    args = parser.parse_args()

    if not all([args.lat, args.lng, args.date]):
        print("Не все обязательные аргументы предоставлены.")
        parser.print_help()
        exit(1)

    results = call_api(args.lat, args.lng, args.date)
    save_json(results, f'{team_name}.json')