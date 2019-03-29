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
    viewers = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return '<News {} {} {}>'.format(self.id, self.title, self.user_id)

    @staticmethod
    def add(title, content, picture, user):
        news = News(title=title, content=content, picture=picture, user=user, viewers=0)
        db.session.add(news)
        db.session.commit()
        return news

    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        db.session.commit()

    @staticmethod
    def view(news_id):
        news = News.query.filter_by(id=news_id).first()
        setattr(news, 'viewers', int(news.viewers) + 1)
        db.session.commit()
        return news_id

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
    data = db.Column(db.String(80), unique=False, nullable=False)
    time = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Matches {} {} {}>'.format(self.id, self.team1, self.team2)

    @staticmethod
    def add(team1, team2, data, time):
        news = Matches(team1=team1, team2=team2, data=data, time=time)
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
            'team1': self.team1,
            'team2': self.team2,
            'data': self.data,
            "time": self.time
        }


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scarves = db.Column(db.String(80), unique=False, nullable=False)
    hat = db.Column(db.String(80), unique=False, nullable=False)
    shirt = db.Column(db.String(80), unique=False, nullable=False)
    zna = db.Column(db.String(80), unique=False, nullable=False)
    passport = db.Column(db.String(80), unique=False, nullable=False)
    rucksack = db.Column(db.String(80), unique=False, nullable=False)
    bre = db.Column(db.String(80), unique=False, nullable=False)
    flag = db.Column(db.String(80), unique=False, nullable=False)
    ball = db.Column(db.String(80), unique=False, nullable=False)
    sum = db.Column(db.String(80), unique=False, nullable=False)
    result = db.Column(db.Boolean, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('orders_list', lazy=True))

    def __repr__(self):
        return '<Order {} {} {}>'.format(self.id, self.hat, self.scarves)

    @staticmethod
    def add(hat, scarves, shirt, zna, passport, rucksack, bre, flag, ball, user):
        sum = hat * 150 + scarves * 350 + shirt * 1500 + zna * 50
        sum += passport * 100 + rucksack * 750 + bre * 100 + flag * 250 + ball * 1000
        orders = Orders(hat=hat, scarves=scarves,
                        shirt=shirt, zna=zna,
                        passport=passport, rucksack=rucksack,
                        bre=bre, flag=flag, ball=ball, result=False,
                        sum=sum, user=user)
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
            'scarves': self.scarves,
            'shirt': self.shirt,
            "zna": self.zna,
            "passport": self.passport,
            "rucksack": self.rucksack,
            "bre": self.bre,
            "flag": self.flag,
            "ball": self.ball,
            'result': self.result
        }


class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scarves = db.Column(db.String(80), unique=False, nullable=False)
    hat = db.Column(db.String(80), unique=False, nullable=False)
    shirt = db.Column(db.String(80), unique=False, nullable=False)
    zna = db.Column(db.String(80), unique=False, nullable=False)
    passport = db.Column(db.String(80), unique=False, nullable=False)
    rucksack = db.Column(db.String(80), unique=False, nullable=False)
    bre = db.Column(db.String(80), unique=False, nullable=False)
    flag = db.Column(db.String(80), unique=False, nullable=False)
    ball = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Storage {} {} >'.format(self.hat, self.scarves)

    @staticmethod
    def add(hat, scarves, shirt, zna, passport, rucksack, bre, flag, ball):
        storage = Storage(hat=hat, scarves=scarves,
                        shirt=shirt, zna=zna,
                        passport=passport, rucksack=rucksack,
                        bre=bre, flag=flag, ball=ball)
        db.session.add(storage)
        db.session.commit()
        return storage

    @staticmethod
    def buy(hat, scarves, shirt, zna, passport, rucksack, bre, flag, ball):
        st = Storage.query.filter_by(id=1).first()
        setattr(st, 'hat', int(st.hat) - hat)
        setattr(st, 'scarves', int(st.scarves) - scarves)
        setattr(st, 'shirt', int(st.shirt) - shirt)
        setattr(st, 'zna', int(st.zna) - zna)
        setattr(st, 'passport', int(st.passport) - passport)
        setattr(st, 'rucksack', int(st.rucksack) - rucksack)
        setattr(st, 'bre', int(st.bre) - bre)
        setattr(st, 'flag', int(st.flag) - flag)
        setattr(st, 'ball', int(st.ball) - ball)
        db.session.commit()
        return hat

    @staticmethod
    def get(hat, scarves, shirt, zna, passport, rucksack, bre, flag, ball):
        st = Storage.query.filter_by(id=1).first()
        setattr(st, 'hat', int(st.hat) + hat)
        setattr(st, 'scarves', int(st.scarves) + scarves)
        setattr(st, 'shirt', int(st.shirt) + shirt)
        setattr(st, 'zna', int(st.zna) + zna)
        setattr(st, 'passport', int(st.passport) + passport)
        setattr(st, 'rucksack', int(st.rucksack) + rucksack)
        setattr(st, 'bre', int(st.bre) + bre)
        setattr(st, 'flag', int(st.flag) + flag)
        setattr(st, 'ball', int(st.ball) + ball)
        db.session.commit()
        return hat

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'hat': self.hat,
            'scarves': self.scarves,
        }

