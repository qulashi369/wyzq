#coding: utf8
import time

from flask import Flask, render_template

from config import DB_URL
from models import Book, Chapter, Category
from libs.db import get_db_session

app = Flask(__name__, template_folder='templates')
db_session = get_db_session(DB_URL)


@app.route("/")
def index():
    # TODO 要新增一个表来放首页的推荐信息
    books = db_session.query(Book).all()
    recommend_books = books[:12]
    return render_template('index.html',**locals())


@app.route("/book/<id>")
def book(id):
    book = db_session.query(Book).filter_by(id=id).first()
    chapters = db_session.query(Chapter).filter_by(book_id=id)
    last_twelve_chapters = chapters.order_by(Chapter.id.desc()).limit(12)
    first_six_chapters = chapters.limit(6).all()
    first_six_chapters.reverse()
    chapter_count = chapters.count()
    return render_template('book.html', **locals())


@app.route("/chapter")
def chapters():
    return render_template('chapters.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000)
