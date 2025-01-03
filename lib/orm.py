from lib import db
from datetime import datetime


class Url(db.Model):
    __tablename__ = 'url'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    platform = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)


class Cache(db.Model):
    __tablename__ = 'cache'
    
    # Define columns for the cache table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_name = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text)
    class_ = db.Column('class', db.Text)  # 'class' is a reserved keyword, hence 'class_'
    size = db.Column(db.Text)
    image = db.Column(db.Text)
    link = db.Column(db.Text)
    platform = db.Column(db.String(128))
    price = db.Column(db.Text)
    history_price = db.Column(db.Text)

    @staticmethod
    def to_list(string: str, symbol: str = '@'):
        ls = string.split(symbol)
        ls = [l for l in ls if len(l) > 0]
        return ls
    
    @staticmethod
    def to_pts_list(string: str, symbol: str = '@'):
        ls = Cache.to_list(string, symbol=symbol)
        
        if len(ls) % 2 != 0: return []
        
        pts = []
        for i in range(len(ls)):
            if i % 2 == 0:
                tmp = [ls[i]]
            else:
                tmp.append(ls[i])
                pts.append(tmp)
                
        return pts
    
    @staticmethod
    def to_str(ls: list, symbol: str = '@'):
        ret = ''
        for l in ls:
            if isinstance(l, list):
                for l_ in l:
                    ret += str(l_) + symbol
            else:
                assert isinstance(l, str), 'Only accepts string'
                ret += str(l) + symbol
        return ret
