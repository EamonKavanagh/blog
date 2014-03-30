import os

import webapp2
import jinja2
from google.appengine.ext import db

from library.models import Posts, Users
import library.utilities as utils

#ADD TIMESTAMPS


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)
    
    def render_str(self, template, **params):
        params['user'] = self.user
        t = jinja_env.get_template(template)
        return t.render(params)
        
    def render(self,template, **kw):
        self.write(self.render_str(template, **kw))
        
    def set_secure_cookie(self, cookie, val):
        secure_val = utils.make_secure_val(val)
        self.response.headers.add_header("Set-Cookie","%s=%s; Path=/"%(cookie,secure_val))
        
    def read_secure_cookie(self, val):
        cookie_val = self.request.cookies.get(val)
        return cookie_val and utils.check_secure_val(cookie_val)
        
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        userID = self.read_secure_cookie('userID')
        self.user = userID and Users.get_by_id(int(userID))


class Front(BlogHandler):
    def get(self):
        posts = db.GqlQuery("""SELECT * FROM Posts 
                        ORDER BY created DESC limit 5;""")
        self.render("front.html", posts=posts)
        
        
class NewPost(BlogHandler):
    def render_newpost(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject, content=content, error=error)

    def get(self):
        if self.user and self.user.username == "Eamon":
            self.render_newpost()
        else:
            self.redirect("/blog")
        
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        
        if subject and content:
            newpost = Posts(subject = subject, content = content)
            newpost.put()
            self.redirect('/blog/' + str(newpost.key().id()))
        else:
            error = "Subject and content please"
            self.render_newpost(subject=subject, content=content,error=error)
            
            
class Post(BlogHandler):
    def get(self, postID):
        post = Posts.get_by_id(int(postID))
        subject = post.subject
        content = post.content
        self.render("post.html",subject=subject,content=content)
        
        
class Signup(BlogHandler):
    def render_signup(self, username="", email="",error=""):
        self.render("signup.html",username=username,email=email,error=error)
                    
    def get(self):
        self.render_signup()
        
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        
        valid_u = utils.valid_username(username)
        valid_p = utils.valid_password(password)
        valid_e = utils.valid_email(email)
        
        already_user = db.GqlQuery("SELECT * FROM Users WHERE username = :1", username).get()
        
        if already_user:
            error = "That user already exists"
            self.render_signup(error=error)
            
        elif ((valid_u and valid_p and verify==password and valid_e) or 
            (valid_u and valid_p and verify==password and email=="")):
            pw_hash = utils.make_pw_hash(username,password)
            newuser = Users(username = username, pw_hash=pw_hash, email=email)
            newuser.put()
            userID = str(newuser.key().id())
            self.set_secure_cookie("userID", userID)
            self.redirect("/blog/welcome")   
            
        else:
            error = "Something went wrong"
            self.render_signup(username=username, email=email, error=error)        
    
    
class Welcome(BlogHandler):
    def get(self):
        if self.user:
            self.response.out.write("Welcome, %s!" %self.user.username)
        else:
            self.redirect('/blog/login')
        
            
class Login(BlogHandler):
    def render_login(self,username="",error = ""):
        self.render("login.html",username=username, error=error)
        
    def get(self):
        if self.user:
            self.redirect('/blog/welcome')
        else:
            self.render_login()
        
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        user = Users.login(username,password)
                
        if user:
            self.set_secure_cookie("userID", str(user.key().id()))
            self.redirect("/blog/welcome")  
        else:
            error = "Invalid login information"
            self.render_login(username,error)
            
            
class Logout(BlogHandler):
    def get(self):
        self.set_secure_cookie("userID", "")
        self.redirect("/blog")
        
        
class Archives(BlogHandler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Posts ORDER BY created;")
        self.render("archives.html", posts=posts)


class About(BlogHandler):
    def get(self):
        self.render("about.html")


class Hire(BlogHandler):
    def get(self):
        self.render("hire.html")


class Contact(BlogHandler):
    def get(self):
        self.render("contact.html")
