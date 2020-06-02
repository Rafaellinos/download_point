from .db import db
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4


class User(db.Model):
    __tablename__ = 'res_users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    login = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    password = db.Column(db.String(120))

    def __init__(self, login, password):
        self.login = login
        self.password = generate_password_hash(password)
        self.admin = False
        self.public_id = str(uuid4())

    def do_commit(self):
        db.session.add(self)
        db.session.commit()
        return self.public_id

    @classmethod
    def search(cls, **kw):
        if not kw:
            res = cls.query.all()
            if not res: return
            return res
        else:
            res = cls.query.filter_by(**kw).first()
            if not res: return
            return res

    def write(self, public_id=None, **kw):
        if not public_id:
            return False
        update = self.update().where(self.public_id == public_id)\
                            .values(kw)
        db.execute(update)
        return True

    def unlink(self):
        db.session.delete(self)
        db.session.commit()
        return True

    @staticmethod
    def check_password(user, password):
        if check_password_hash(user.password, password):
            return True
        return


