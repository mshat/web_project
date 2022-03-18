# web
BMSTU Web development course (2020)

# Цель работы
Разработать клиент-серверное приложение для интернет-магазина рюкзаков

# Краткий перечень функциональных требований
1. Регистрация
2. Вход в систему
3. Выход из системы
4. Просомтр списка товаров
5. Просмотр детальной информации о товаре
6. Просмотр списка компаний-производителей
7. Просмотр детальной информации о компании-производителе
8. Добавление товара в корзину
9. Заказ товаров из корзины
10. Просмотр списка заказов
11. Просмотр детальной информации о заказе
12. Оплата заказа (реализовать заглушкой, изменение статуса заказа на "оплачен, в обработке")
13. Отмена заказа
14. Просомтр списка типов рюкзаков
15. Просмотр детальной информации о типе рюкзака
14. Просомтр списка материалов
15. Просмотр детальной информации о материале

# Use-case диаграмма системы
![Usecase](https://github.com/mshat/web_project/blob/master/git_res/use-case.jpg)

# ER-диаграмма сущностей системы
![ER](https://github.com/mshat/web_project/blob/master/git_res/entity-relationship.png)

# Макет в Figma
https://www.figma.com/file/tTvgv0WeFZP8bHFiTkxjUk/Untitled?node-id=15%3A388

# Запуск сервисов
```shell
# pip install -r requirements.txt
# python manage.py runserver
```

**Запуск nginx и серверов API**
```shell
# docker-compose up
```

**Генерация сертификатов**
```shell
# docker-compose -f docker-compose.ssl.yml run --rm minica
```

**Бенчмарк**
```shell
# docker-compose -f docker-compose.bench.yml run --rm ab -n 1000 -c 2 https://backpack.shop/
```

