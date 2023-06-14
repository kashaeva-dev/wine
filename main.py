import datetime
import logging.config
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pprint import pprint

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

from settings import logger_config

logging.config.dictConfig(logger_config)
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

logger.debug(get_age())

wines_df = pd.read_excel('wine.xlsx').fillna('')
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
pprint(wines_by_category)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    age=get_age(),
    wines_by_category=wines_by_category,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
