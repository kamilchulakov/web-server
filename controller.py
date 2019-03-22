from flask_restful import abort

from flask import Flask, redirect, session, request
from flask import render_template as flask_render_template
import extra.auth as auth
from api.v1 import init as init_api_v1
from forms import *

from models import User, News, Orders


def init_route(app, db):

    # Переопределение стандартного рендера, добавляет параметр auth_user
    def render_template(*args, **kwargs):
        kwargs['auth_user'] = auth.get_user()
        return flask_render_template(*args, **kwargs)

    init_api_v1(app, auth)  # Инициализация маршрутов для API

    @app.route('/')
    @app.route('/index')
    @app.route('/news')
    def index():
        if not auth.is_authorized():
            return render_template(
                'index.html',
                title='Главная',
            )

        news_list = News.query.filter_by(user_id=1)
        return render_template(
            'news-list.html',
            title="Главная",
            news_list=news_list
        )

    @app.route('/install')
    def install():
        db.create_all()
        return render_template(
            'install-success.html',
            title="Главная"
        )

    @app.route('/squad')
    def view_squad():
        return render_template(
            'squad.html',
            title="Состав"
        )

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        has_error = False
        login = ''
        if request.method == 'POST':
            username = request.form['username']
            if auth.login(username, request.form['password']):
                return redirect('/')
            else:
                has_error = True
        return render_template(
            'login.html',
            title='Вход',
            login=login,
            has_error=has_error
        )

    @app.route('/logout', methods=['GET'])
    def logout():
        auth.logout()
        return redirect('/')

    @app.route('/user/create', methods=['GET', 'POST'])
    def registration():
        has_error = False
        form = UserCreateForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user:
                has_error = True
            else:
                User.add(username=username, password=password)
                auth.login(username, password)
                return redirect('/')
        return render_template(
            'registration.html',
            title='Зарегистрироваться',
            form=form,
            has_error=has_error
        )

    @app.route('/news/create', methods=['GET', 'POST'])
    def news_create_form():
        if not auth.is_authorized():
            return redirect('/login')
        form = NewsCreateForm()
        if auth.get_user().id != 1:
            abort(403)
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            picture = form.picture.data

            News.add(title=title, content=content, picture=picture, user=auth.get_user())
            return redirect('/')
        return render_template(
            'news-create.html',
            title='Создать новость',
            form=form
        )

    @app.route('/news/<int:id>')
    def news_view(id: int):
        if not auth.is_authorized():
            return redirect('/login')
        news = News.query.filter_by(id=id).first()
        if not news:
            abort(404)

        user = news.user
        return render_template(
            'news-view.html',
            title='Новость - ' + news.title,
            news=news,
            user=user
        )

    @app.route('/news/delete/<int:id>')
    def news_delete(id: int):
        if not auth.is_authorized():
            return redirect('/login')
        news = News.query.filter_by(id=id).first()
        if auth.get_user().id != 1:
            abort(403)
        News.delete(news)
        return redirect('/news')

    @app.route('/matches')
    def show_matches():
        abort(403)

    @app.route('/shop', methods=['GET', 'POST'])
    def make_shopping():
        global z
        if not auth.is_authorized():
            return redirect('/login')
        form = ShopForm()
        if any([form.scarves.data, form.hat.data]) != 0:
            scarves = form.scarves.data
            hat = form.hat.data
            Orders.add(hat=hat, scarve=scarves, user=auth.get_user())
            orders = Orders.query.filter_by(hat=hat, scarve=scarves, user=auth.get_user()).first()
            return redirect('/orders/{}'.format(orders.id))
        return render_template(
            'shop.html',
            title="Магазин",
            form=form)

    @app.route('/orders/<int:id>')
    def orders_view(id: int):
        if not auth.is_authorized():
            return redirect('/login')

        orders = Orders.query.filter_by(id=id).first()
        user = orders.user
        if auth.get_user().id != user.id:
            abort(403)
        return render_template(
            'orders_view.html',
            title='Заказ № ' + str(orders.id),
            orders=orders,
            user=user
        )

    @app.route('/pay/<int:id>')
    def orders_pay(id: int):
        if not auth.is_authorized():
            return redirect('/login')

        orders = Orders.query.filter_by(id=id).first()
        user = orders.user
        if auth.get_user().id != user.id:
            abort(403)
        orders.result = True
        db.session.commit()
        return render_template(
            'orders_pay.html',
            orders=orders
        )

    @app.route('/about')
    def about():
       return render_template(
            'about.html')
