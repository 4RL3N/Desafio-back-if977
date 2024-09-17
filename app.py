from flask import Flask, request, jsonify
from models import db, Book

app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Rota para listar todos os livros
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.serialize() for book in books])

# Rota para obter um livro pelo ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.serialize())

# Rota para adicionar um novo livro
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], year=data['year'], gender=data['gender'], stock=data['stock'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.serialize()), 201

# Rota para atualizar um livro existente
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    book.title = data['title']
    book.author = data['author']
    book.year = data['year']
    book.gender = data['gender']
    book.stock = data['stock']

    db.session.commit()
    return jsonify(book.serialize())

# Rota para deletar um livro
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return '', 204

# Rota para obter um livro pelo genero
@app.route('/books/gender/<string:book_gender>', methods=['GET'])
def get_books_gender(book_gender):
    books = Book.query.filter(Book.gender.ilike(f'%{book_gender}%')).all()
    return jsonify([book.serialize() for book in books])

if __name__ == '__main__':
    app.run(debug=True)