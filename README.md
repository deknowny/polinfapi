# Polyakov Informatics API Client
> Polyakov Informatics site parser 

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/polinfapi)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/polinfapi)
![PyPI](https://img.shields.io/pypi/v/polinfapi)
[![Coverage Status](https://coveralls.io/repos/github/deknowny/polinfapi/badge.svg?branch=main)](https://coveralls.io/github/deknowny/polinfapi?branch=main)
***
__**Check out documentation**__: [https://deknowny.github.io/polinfapi/latest/](https://deknowny.github.io/polinfapi/latest/)

## Overview
```python
import polinfapi


# Получение всех тренировочных заданий под номером 1
tasks = polinfapi.Task1ModelsAnalysis.fetch()
# Первый из списка
task = tasks[0]

print(
    f"Номер задания: {task.raw.no}\n"
    f"Вопрос: {task.question}\n"
    f"Ответ: {task.answer}"
)

# Сохранение картинки задания на диск
with open("file.jpg", "wb+") as fd:
    image = tasks[0].download_image()
    fd.write(image.getvalue())
```
Output:
```
Номер задания: 4841
Вопрос: На рисунке схема дорог Н-ского района изображена в виде графа, в таблице содержатся сведения о длине этих дорог в километрах. Так как таблицу и схему рисовали независимо друг от друга, нумерация населённых пунктов в таблице никак не связана с буквенными обозначениями на графе. Известно, что длина дороги ЗЕ равна 15 км. Определите длину дороги БГ. В ответе запишите целое число – длину дороги в километрах.
Ответ: 20
```

# Installation
Via PyPI:
```shell
python -m pip install polinfapi
```
Or via GitHub
```shell
python -m pip install https://github.com/deknowny/polinfapi/archive/main.zip
```
# Contributing
Check out [site Contributing section](https://deknowny.github.io/polinfapi/latest/contributing/)
