from flask import Flask, jsonify, abort, request, Response
from random import choice
from tools_db import create_connection, execute_query, execute_read_query, BASE_DIR


app = Flask(__name__)
quotes = [
    {
        "id": 1,
        "author": "Rick Cook",
        "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает.",
    },
    {
        "id": 2,
        "author": "Waldi Ravens",
        "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
    },
    {
        "id": 3,
        "author": "Mosher’s Law of Software Engineering",
        "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
    },
    {
        "id": 4,
        "author": "Yoggi Berra",
        "text": "В теории, теория и практика неразделимы. На практике это не так."
    },

]

about_me = {
    "name": "Alexandr",
    "surname": "Igorevich",
    "fastname": "Goncharenko",
    "age": 31
}


@app.route("/count_quotes")
def count_quotes():
    return {
        "count": len(quotes)
    }


@app.route("/quotes")
def quotes_list():
    query = "SELECT * FROM quotes;"
    connection = create_connection(BASE_DIR / 'db.sqlite')
    results = execute_read_query(connection, query)
    keys = ("id", "author", "text")
    quotes = []
    for data in results:
        quote = dict(zip(keys, data))
        quotes.append(quote)
    return jsonify(quotes)  # Сериализация  dict --> json


@app.route("/random_qoutes")
def random_quotes():
    return jsonify(choice(quotes))


@app.route("/quotes/<int:id>")
def get_quote(id):
    query = f"SELECT * FROM quotes WHERE id={id};"
    connection = create_connection(BASE_DIR / 'db.sqlite')
    data = execute_read_query(connection, query, only_one=True)
    if data is None:
        abort(404, description=f"Quote with id={id} not found")
    # print(f"{data=}")
    keys = ("id", "author", "text")
    quote = dict(zip(keys, data))
    return jsonify(quote)


@app.route("/quotes", methods=["POST"])
def create_quote():
    new_quote = request.json
    try:
        query = f"INSERT INTO quotes (author, text) VALUES ('{new_quote['author']}', '{new_quote['text']}');"
    except KeyError:
        abort(400, "field author and text required")
    connection = create_connection(BASE_DIR / 'db.sqlite')
    execute_query(connection, query)
    return {}, 201


@app.route("/quotes/<int:id>", methods=["PUT"])
def edit_quote(id):
    new_data = request.json
    for quote in quotes:
        if quote["id"] == id:
            if new_data.get("author"):
                quote["author"] = new_data["author"]
            if new_data.get("text"):
                quote["text"] = new_data["text"]
            return quote, 200
        new_data['id'] = quotes[-1]["id"] + 1
        quotes.append(new_data)
        return new_data, 201


@app.route("/quotes/<int:id>", methods=['DELETE'])
def delete(id: int):
    # delete quote with id
    for quote in quotes:
        if quote["id"] == id:
            quotes.remove(quote)
            return f"Quote with id {id} was deleted.", 200
    abort(404, description=f"Quote with id={id} not found")


if __name__ == "__main__":
    app.run(debug=True)
