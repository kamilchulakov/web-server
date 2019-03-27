from dbase import db
from flask import session


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)  # будем хранить хэш пароля

    def __repr__(self):
        return '<User {} {}>'.format(self.id, self.username)

    @staticmethod
    def add(username, password):
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        db.session.commit()


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    content = db.Column(db.String(80), unique=False, nullable=True)  # пусть текст можно будет оставить пустым
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    picture = db.Column(db.String(80), unique=False, nullable=True)
    user = db.relationship('User', backref=db.backref('news_list', lazy=True))

    def __repr__(self):
        return '<News {} {} {}>'.format(self.id, self.title, self.user_id)

    @staticmethod
    def add(title, content, picture, user):
        news = News(title=title, content=content, picture=picture, user=user)
        db.session.add(news)
        db.session.commit()
        return news

    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        db.session.commit()

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'picture': self.picture,
            'user_id': self.user_id}
    
    
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    content = db.Column(db.String(80), unique=False, nullable=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False)
    news = db.relationship('News', backref=db.backref('comments_list', lazy=True))

    def __repr__(self):
        return '<Comments {} {} {}>'.format(self.id, self.title, self.user_id)

    @staticmethod
    def add(title, content, news):
        comment = Comments(title=title, content=content, news_id=news)
        db.session.add(comment)
        db.session.commit()
        return comment

    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        db.session.commit()

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'news_id': self.news_id}


class Matches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team1 = db.Column(db.String(80), unique=False, nullable=False)
    team2 = db.Column(db.String(80), unique=False, nullable=False)
    tournament = db.Column(db.String(80), unique=False, nullable=False)
    data = db.Column(db.String(80), unique=False, nullable=False)
    result = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Macthes {} {} {}>'.format(self.id, self.team1, self.team2)

    @staticmethod
    def add(title, content, user):
        news = News(title=title, content=content, user=user)
        db.session.add(news)
        db.session.commit()
        return news

    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        db.session.commit()

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id
        }


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scarve = db.Column(db.String(80), unique=False, nullable=False)
    hat = db.Column(db.String(80), unique=False, nullable=False)
    sum = db.Column(db.String(80), unique=False, nullable=False)
    result = db.Column(db.Boolean, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('orders_list', lazy=True))

    def __repr__(self):
        return '<Order {} {} {}>'.format(self.id, self.hat, self.scarve)

    @staticmethod
    def add(hat, scarve, user):
        sum = hat * 50 + scarve * 100
        orders = Orders(hat=hat, scarve=scarve, result=False, sum=sum, user=user)
        db.session.add(orders)
        db.session.commit()
        return orders

    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        db.session.commit()

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'hat': self.hat,
            'scarve': self.scarve,
            'result': self.result,
            'user': self.user
        }


class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scarve = db.Column(db.String(80), unique=False, nullable=False)
    hat = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Storage {} {} >'.format(self.hat, self.scarve)

    @staticmethod
    def add(hat, scarve):
        storage = Storage(hat=hat, scarve=scarve)
        db.session.add(storage)
        db.session.commit()
        return storage

    @staticmethod
    def buy(hat, scarve):
        st = Storage.query.filter_by(id=1).first()
        setattr(st, 'hat', int(st.hat) - hat)
        setattr(st, 'scarve', int(st.scarve) - scarve)
        db.session.commit()
        return hat

    @staticmethod
    def get(hat, scarve):
        st = Storage.query.filter_by(id=1).first()
        setattr(st, 'hat', int(st.hat) + hat)
        setattr(st, 'scarve', int(st.scarve) + scarve)
        db.session.commit()
        return hat


    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'hat': self.hat,
            'scarve': self.scarve,
        }

