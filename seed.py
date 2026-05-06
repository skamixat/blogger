from main_blog.models import Article, Category
from django.utils.text import slugify

def make_slug(title):
    slug = title.lower().replace("++", "plus").replace("#", "sharp")
    return slugify(slug)  # только латиница

# Категории
categories_data = ['Python', 'Arduino', 'C++']
categories = {}
for name in categories_data:
    cat = Category.objects.create(
        name=name,
        slug=make_slug(name)
    )
    categories[name] = cat

# Статьи (по 5 на категорию)
articles_data = {
    'Python': [
        'Основы Python для начинающих',
        'Работа со списками в Python',
        'Функции и модули в Python',
        'Обработка исключений в Python',
        'Работа с файлами в Python'
    ],
    'Arduino': [
        'Введение в Arduino',
        'Работа с датчиками на Arduino',
        'Управление светодиодами',
        'Подключение дисплеев к Arduino',
        'Создание простого проекта на Arduino'
    ],
    'C++': [
        'Основы C++',
        'Указатели и ссылки в C++',
        'ООП в C++',
        'Работа с памятью в C++',
        'Стандартная библиотека C++'
    ]
}

# Создание статей
for category_name, titles in articles_data.items():
    for idx, title in enumerate(titles, start=1):
        Article.objects.create(
            title=title,
            slug=make_slug(title),          # Обязательно формируем slug
            content=f"Это статья на тему: {title}",
            photo=f'article/default_{idx}.jpg',  # Задаём тестовую картинку, можно любую
            is_published=True,
            cat=categories[category_name]
        )

print("База данных заполнена корректными данными, slug заполнены!")