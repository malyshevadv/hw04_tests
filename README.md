# Бекенд для социальной сети блогеров (hw04_tests, часть yatube_project)

### Описание
Проект по написанию тестов к созданому сайту

- Тестирование Models
- Тестирование URLs
  - Проверка доступность страниц и названия шаблонов приложения Posts. Проверка учитывает права доступа.
  - Проверка, что запрос к несуществующей странице вернёт ошибку 404.
- Проверка namespase:name и шаблонов
  - Проверка, что во view-функциях используются правильные html-шаблоны.
- Тестирование контекста
  - Проверка, соответствует ли ожиданиям словарь context, передаваемый в шаблон при вызове.
- Дополнительная проверка при создании поста
  - Проверка, что если при создании поста указать группу, то этот пост появляется:
    - на главной странице сайта,
    - на странице выбранной группы,
    - в профайле пользователя.
  - Проверка, что этот пост не попал в группу, для которой не был предназначен.
- Тестирование Forms
  - при отправке валидной формы со страницы создания поста создаётся новая запись в базе данных;
  - при отправке валидной формы со страницы редактирования поста происходит изменение поста с post_id в базе данных.

### Технологии
- Python 3.7
- Django 2.2.19
- Pytest django 3.8.0
### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- В папке с файлом manage.py выполните команду:
```
python3 manage.py runserver
```

Выполнение тестов:
```
python manage.py test
```
### Авторы
Дарья М.
