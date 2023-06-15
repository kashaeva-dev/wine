import datetime
import argparse
import logging.config
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pprint import pprint

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

from settings import logger_config

logger = logging.getLogger("main_logger")


def get_age():
    foundation_year = 1920
    age = datetime.datetime.today().year - foundation_year
    match age % 100:
        case 11 | 12 | 13 | 14:
            return f'{age} лет'
        case _:
            match age % 10:
                case 1:
                    return f'{age} год'
                case 2 | 3 | 4:
                    return f'{age} года'
                case _:
                    return f'{age} лет'


def get_wines(filepath):
    wines_df = pd.read_excel(filepath).fillna('')
    wines_df.rename(columns={
        'Категория': 'category',
        'Название': 'name',
        'Сорт': 'type',
        'Цена': 'price',
        'Картинка': 'picture',
        'Акция': 'promo',
        }, inplace=True)

    wines = wines_df.to_dict(orient='records')
    wines_by_category = defaultdict(list)
    for wine in wines:
        wines_by_category[wine['category']].append(wine)
    wines_by_category = dict(sorted(wines_by_category.items()))

    return wines_by_category


def create_parser():
    parser = argparse.ArgumentParser(
        prog="Site about new Russian wine",
        description='The script allows you to start '
                    'site to sell wines. It shows the information about you wines.'
    )
    parser.add_argument(
        'path',
        help='You can specify the path to your data file',
        default='wine.xlsx',
    )
    return parser


def main():
    logging.config.dictConfig(logger_config)

    parser = create_parser()
    user_input = parser.parse_args()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        age=get_age(),
        wines_by_category=get_wines(user_input.path),
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__=="__main__":
    main()
