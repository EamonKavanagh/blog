import re
import hmac
import random
import string
from secret import secret

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PW_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
    
def valid_username(username):
    return USER_RE.match(username)
        
def valid_password(password):
    return PW_RE.match(password)
    
def valid_email(email):
    return EMAIL_RE.match(email)
    
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))
    
def make_secure_val(val):
    h = hmac.new(secret,val).hexdigest()
    return "%s|%s" %(val,h)
    
def make_pw_hash(username, password, salt=None):
    if not salt:
        salt = make_salt()
    h = hmac.new(secret,username+password+salt).hexdigest()
    return '%s|%s' %(salt, h)
    
def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val
    
def check_pw(username, password, h):
    salt = h.split('|')[0]
    return h == make_pw_hash(username, password, salt)
    
