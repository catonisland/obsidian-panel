from app import db
import datetime
import hashlib
import re

# password salt
SALT = b"\x87\x93\xfb\x00\xfa\xc2\x88\xba$\x86\x98\'\xba\xa8\xc6"

class AdminUsers(db.Model):
    __tablename__ = "ob_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    """
    username
    """
    username = db.Column(db.String(80),unique=True)

    """
    User password (hashed of course.)
    """
    hash = db.Column(db.String(120))

    """
    User's email address (optional)

    """
    email = db.Column(db.String(120))
    """
    User join time
    """
    join_time = db.Column(db.DateTime,default=datetime.datetime.now())

    """
    :privilege: defines the user's authorization group.
    There are 2 kinds of users:
    1) Super User (only 1), Owns all privileges and can control all instances. [privilege=0]
    2) Ordinary Admin User. Owns all privileges in self-created instance. [privilege=1]
    """
    privilege = db.Column(db.Integer , default=0)

    def __init__(self, username, _password, privilege, email=None):
        self.username   = username
        self._password  = _password
        self.privilege  = privilege
        self.email = email
        self.hash = None

    def __repr__(self):
        return "<User %s, priv=%s>" % (self.username, self.privilege)

    def create(self):
        if len(self.username) > 32:
            raise ValueError("username `%s` is too long!" % self.username)

        password_re = "^\w{6,30}$"
        if re.match(password_re,self._password) == None:
            raise ValueError("password format doesn't matches!")

        self.hash = hashlib.md5(self._password.encode('utf-8')+SALT).hexdigest()

        db.session.add(self)
        db.session.commit()

        return True