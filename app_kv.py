from flask import Flask, jsonify, abort, request, Response
import random

from werkzeug.wrappers import response

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False  # Преобразование кириллицы

about_me = {  # Список с ресурсом, который мы возвращаем
    "name": "Евгений",
    "surname": "Юрченко",
    "email": "eyurchenko@specialist.ru",
}

quotes = [
    {
        "id": 1,
        "author": "Rick",
        "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает.",
        "rating": 5,
    },
    {
        "id": 2,
        "author": "Waldi Ravens",
        "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках.",
        "rating": 3,
    },
    {
        "id": 3,
        "author": "Mosher’s Law of Software Engineering",
        "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили.",
        "rating": 2,
    },
    {
        "id": 4,
        "author": "Yoggi Berra",
        "text": "В теории, теория и практика неразделимы. На практике это не так.",
        "rating": 5,
    },
]


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/about")  # Маршрут
def about():  # Функция-обработчик
    return about_me


@app.route("/quotes/")
def quotes_list():
    return jsonify(quotes), 200


@app.route("/quotes/", methods=["POST"])
def create_quote():
    """ Клиент отправляет либо с ID либо без.
    Если есть, то редактируем, если нет, то добавляем."""
    data = request.json  # Взять данные JSON клиента отправленного

    if "id" in data:  # Проверяем, что в поступивших данных поле ID на месте
        put_id = data["id"]
        qoute_found = "False"
        for qoute in quotes:
            if qoute["id"] == int(put_id):
                qoute.update(data)
                qoute_found = "True"
        if qoute_found == "True":
            return f"Edited: {quotes} ", 200
        else:
            return f"Quote with id {put_id} not found", 404
    # TODO: Поставить ID в словаре на 0-ю позицию
    else:
        list_ids = [quote["id"] for quote in quotes]  # Получаем список всех ID
        newid = max(list_ids) + 1  # Находим максимальный и добавляем +1
        data["id"] = newid
        data["rating"] = 1
        quotes.append(data)
        print("data = ", quotes)

        return f"Created: {quotes}", 201


@app.route("/quotes/<id>")
def get_quote(id:int):
    for qoute in quotes:
        if qoute["id"] == id:  # Поиск в словаре по полю id
            return jsonify(qoute)

    abort(404, description=f"Quote with id={id} not found")


@app.route("/quotes/<int:id>", methods=["DELETE"])
def delete(id):
    # delete quote with id
    for qoute in quotes:
        if qoute["id"] == id:
            quotes.remove(qoute)
            return f"Quote with id {id} was deleted.", 200
    abort(404, description=f"Quote with id={id} not found")


@app.route("/quotes/editrate/<id>=<newrate>", methods=["PUT"])
def editrate(id, newrate):
    "Отредактировать рейтинг цитаты"
    for quote in quotes:
        if quote["id"] == int(id):
            quote["rating"] = int(newrate)
    return f"Changed: {quotes}", 201


@app.route("/quotes/filter?<param>=<value>", methods=["GET"])
def filter_quotes(param, value):
    filtor = request.args.get()
    print(filtor)
    for quote in quotes:
        if quote[param] == value:
            print(quote)
    return {}


@app.route("/count-quotes/")
def count_qoutes():  # Количество элементов в словаре
    # return str(len(quotes))
    return {"count": len(quotes)}


@app.route("/random/")
def show_random():
    rand = random.choice(quotes)
    return f'<b>Случайная цитата</b>: <br>{rand["text"]}'


if __name__ == "__main__":
    app.run(
        debug=True
    )  # запуск приложение с режимом отладки. Иначе будет 500-я ошибка.
