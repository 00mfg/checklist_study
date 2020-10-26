import os
import sys
import click

from flask import Flask, render_template
from flask_mongoengine import MongoEngine


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'watchlist',
}
db = MongoEngine(app)

class User(db.Document):  # 表名将会是 user（自动生成，小写处理）
    name = db.StringField(max_length=50, required=True)  # 名字

class Movie(db.Document):  # 表名将会是 movie
    title = db.StringField(max_length=50, required=True) # 电影标题
    year = db.IntField(max_length=4, required=True)  # 电影年份



@app.cli.command()
def forge():
    """Generate fake data."""

    # 全局的两个变量移动到这个函数内
    name = 'Chao Liu'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name).save()
    for m in movies:
        movie = Movie(title=m['title'], year=m['year']).save()

    click.echo('Done.')


@app.route('/')
def index():
    user = User.objects.first()
    movies = Movie.objects.all()
    return render_template('index.html', movies=movies, user=user)

@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    user = User.objects.first()
    return render_template('404.html', user=user), 404  # 返回模板和状态码