# Nominatim

Написать DDT (data driven tests) тесты публичного API геокодинга openstreetmaps.org
(проект nominatim - https://nominatim.org/release-docs/develop/api/Overview/).
Необходимо протестировать прямое (адрес -> координаты) и обратное (координаты -> адрес) геокодирование.
Python, pytest, allure
Логирование, комментирование кода,
возможность обозначить проблему, при падении теста, по отчету

Что я от каждого из вас жду:

1)Устанавливаем PyCharm (как основную, используемую всеми нами автоматизаторами среду) Community Edition (бесплатная) - есть и для Ubuntu 20 и для windows
2)Регистрируемся на GitHub
3)Заводим в PyCharm проект (на python 3.8) и связываем его с GitHub
4)Разбираемся с сервисом www.openstreetmap.org и его API
5)Разбираемся с библиотеками питона request, pytest, allure (кто не знаком с питоном - еще с его базовым синтаксисом)
6)Пишем DDT тесты по заданию
Ожидаю чистый код, грамотные названия классов/методов/тестов, комментарии к классам/методам (их можно на русском), переиспользование кода
Будете заниматься им дома - ОК. Но в целом - в рабочее время, когда нет активных задач на ручное тестирование. (Задачи на ручное приоритетнее)

Полезные ссылки -
python - http://uchcom7.botik.ru/L/prog/python/python_01.pdf
DDT - https://jazzteam.org/ru/technical-articles/data-driven-testing/
pytest (несколько старая, но емко-годная) - https://eax.me/pytest/
request - https://python-scripts.com/requests



pytest -s -v --alluredir=allureres
allure serve allureres

Добавлен запуск тестов ч/з github actions

https://pytest-docs-ru.readthedocs.io/ru/latest/example/simple.html - док-ция


https://habr.com/ru/post/448798/ - автоматизация тестов

https://pytest-docs-ru.readthedocs.io/ru/latest/example/simple.html - инф об упавших тестах