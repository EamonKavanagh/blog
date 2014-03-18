from google.appengine.ext import db
from library.utilities import *

class Posts(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    
class Users(db.Model):
    username = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()
    
    @classmethod
    def login(cls, username, password):
        user = db.GqlQuery("SELECT * FROM Users WHERE username = :1", username).get()
        if user and check_pw(username, password, user.pw_hash):
            return user
            