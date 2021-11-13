from flask import Flask, jsonify, abort, request, Response
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'test.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class QuoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(32), unique=False)
    text = db.Column(db.String(255), unique=False)

    def __init__(self, author, text):
        self.author = author
        self.text = text

    def __repr__(self):
        return f"Quote: {self.author}/ {self.text[:15]}..."

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))
        return d


@app.route("/quotes")
def quotes_list():
    quotes = QuoteModel.query.all()
    quotes = [quote.to_dict() for quote in quotes]
    return jsonify(quotes)  # Сериализация  object --> dict --> json


@app.route("/quotes/<int:id>")
def get_quote(id):
    quote = QuoteModel.query.get(id)
    if quote is None:
        abort(404, description=f"Quote with id={id} not found")
    return jsonify(quote.to_dict())


@app.route("/quotes", methods=["POST"])
def create_quote():
    new_data = request.json
    # quote = QuoteModel(new_quote["author"], new_quote["quote"])
    quote = QuoteModel(**new_data)
    db.session.add(quote)
    db.session.commit()
    return jsonify(quote.to_dict()), 201


@app.route("/quotes/<int:id>", methods=["PUT"])
def edit_quote(id):
    new_data = request.json
    quote = QuoteModel.query.get(id)
    if quote:  # Если цитата найдена в базе - изменяем
        quote.author = new_data.get("author") or quote.author
        quote.text = new_data.get("text") or quote.text
        db.session.commit()
        return quote.to_dict(), 200
    else:  # Если нет - создаем новую
        new_quote = QuoteModel(**new_data)
        db.session.add(new_quote)
        db.session.commit()
        return quote.to_dict(), 200


@app.route("/quotes/<int:id>", methods=['DELETE'])
def delete(id: int):
    # delete quote with id
    quote = QuoteModel.query.get(id)
    if quote:
        db.session.delete(quote)
        db.session.commit()
        return quote.to_dict(), 200
    abort(404, description=f"Quote with id={id} not found")


if __name__ == "__main__":
    app.run(debug=True)

