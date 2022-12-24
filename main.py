import json
from collections.abc import Iterable
import random
from faker import Faker

from conf import MODEL


def get_field_title() -> Iterable[str]:
    """Функция генериратор. Случайным образом выбирает название книги, считанное из файла books.txt"""
    with open("books.txt", encoding="UTF-8") as f:
        yield random.choice([i.strip() for i in f.readlines()])


def get_field_model() -> str:
    return MODEL


def gen_field_year() -> Iterable[int]:
    """Функция генерирует случайным образом год выпуска книги из
        диапазона 2000-2022
    """
    yield random.randrange(2000, 2022)


def gen_field_pages() -> Iterable[int]:
    """Функция генерирует случайным образом количество страниц в книге"""
    yield random.randrange(10, 1000)


def gen_field_rating() -> Iterable[int]:
    """Функция генерирует случайным образом рейтинг. Диапазон 0-5"""
    yield round(random.uniform(0, 5), 1)


def gen_field_price() -> Iterable[int]:
    """Функция генерирует случайным образом цену книги"""
    yield round(random.uniform(100, 2000), 2)


def gen_field_author() -> Iterable[list]:
    """Функция генерирует случайным образом имя и фамилию автор. женские имена)"""
    fake = Faker("ru")
    yield [" ".join((fake.first_name_female(), fake.last_name_female())) for _ in range(random.randrange(1, 4))]


def gen_field_isbn13() -> Iterable[str]:
    """Функция генерирует isbn10 с помощью модуля Fake"""
    fake = Faker()
    yield fake.isbn10()


def gen_field_pk(start_pk: int = 1) -> Iterable[int]:
    """Функция инкремент.Возвращает значение, которое увеличивается на единицу при генерации нового объекта.
        :param start_pk: автоинкремент
        дефолтное знаечение = 1
        :return: возвращает генератор int"""
    while True:
        yield start_pk
        start_pk += 1


def book_gen(default_pk=1) -> Iterable[dict]:
    """функция генератор
        :param default_pk: дефолтное знаечение = 1
        :return: возвращает итератор словаря
    """
    g = gen_field_pk(default_pk)
    for _ in range(0, 100):
        yield dict({
            "model": get_field_model(),
            "pk": next(g),
            "fields": {
                "title": next(get_field_title()),
                "year": next(gen_field_year()),
                "pages": next(gen_field_pages()),
                "isbn13": next(gen_field_isbn13()),
                "rating": next(gen_field_rating()),
                "price": next(gen_field_price()),
                "author": next(gen_field_author())
            }
        })


def main() -> None:
    """Функция формирует список из 100 книг (список словарей) и записывает его в json файл """

    g = book_gen(default_pk=1)
    list_books = [i for i in g]

    with open("file_with_books.txt", "w", encoding="UTF-8") as file_out:
        json.dump(list_books, file_out, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
