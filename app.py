import os
import sys
import click

from flask import Flask, render_template, url_for, redirect, flash, request
from flask_mongoengine import MongoEngine


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('请输入正确信息')
            return redirect(url_for('index'))
        movie = Movie(title=title, year=year).save()
        flash('添加成功')
        return redirect(url_for('index'))

    movies = Movie.objects.all()
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.objects.get(id=movie_id)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('请输入正确信息')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        movie.save()
        flash('更新成功.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录


@app.route('/movie/delete/<movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.objects.get_or_404(id=movie_id)  # 获取电影记录
    movie.delete()
    flash('删除成功')
    return redirect(url_for('index'))  # 重定向回主页


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    user = User.objects.first()
    return render_template('404.html', user=user), 404  # 返回模板和状态码


@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = User.objects.first()
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}