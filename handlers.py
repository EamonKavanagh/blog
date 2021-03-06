import os

import webapp2
import jinja2
from google.appengine.ext import db

from library.models import Posts, Users, Comments
import library.utilities as utils

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
        
    def logout(self):
        self.set_secure_cookie("userID", "")
        
    def read_secure_cookie(self, val):
        cookie_val = self.request.cookies.get(val)
        return cookie_val and utils.check_secure_val(cookie_val)
        
    def verify_referer(self, referer):
        if not referer or referer.endswith('/login') or referer.endswith('/signup'):
            return '/'
        else:
            return referer
        
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
            self.redirect("/blog/")
        
    def post(self):
        subject = self.request.get("subject")
        image = self.request.get("image")
        summary = self.request.get("summary")
        content = self.request.get("content")
        
        if subject and content and image and summary:
            newpost = Posts(subject=subject, content=content, image=image, summary=summary)
            newpost.put()
            self.redirect('/' + str(newpost.key().id()))
        else:
            error = "Subject, content, summary and image required."
            self.render_newpost(subject=subject, content=content,error=error)
            
            
class Post(BlogHandler):
    def get(self, postID):
        post = Posts.get_by_id(int(postID))
        comments = db.GqlQuery("""SELECT * FROM Comments WHERE postID=:1
                                ORDER BY created;""", postID)
        subject = post.subject
        content = post.content
        self.render("post.html",subject=subject,content=content, comments=comments)
        
    def post(self, postID):
        if self.user:
            comment = self.request.get("comment")
            newComment = Comments(postID=postID, commenter=self.user.username, 
                                  comment=comment)
            newComment.put()
            self.redirect('/'+postID)
            
        
class Signup(BlogHandler):

    def register_user(self, username, password, email):
        pw_hash = utils.make_pw_hash(username,password)
        newuser = Users(username = username, pw_hash=pw_hash, email=email)
        newuser.put()
        userID = str(newuser.key().id())
        self.set_secure_cookie("userID", userID)
                    
    def get(self):
        self.render("signup.html", referer=self.request.headers.get('referer', '/'))
        
    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        referer = self.verify_referer(str(self.request.get('referer')))
        
        params = dict(username = username, email = email)
        
        valid_u = utils.valid_username(username)
        valid_p = utils.valid_password(password)
        valid_e = utils.valid_email(email)
        
        already_user = None
        if valid_u:
            already_user = db.GqlQuery("SELECT * FROM Users WHERE username = :1", username).get()
        
        if not valid_u:
            params['error_username'] = "Invalid username.  "
            have_error = True
        if not valid_p:
            params['error_password'] = "Invalid password.  "
            have_error = True
        elif verify != password:
            params['error_password'] = "Passwords didn't match.  "
            have_error = True
        if not valid_e and email != '':
            params['error_email'] = "Invalid email.  "
            have_error = True
        
        if already_user:
            self.render("signup.html", error_username = "Username already taken.")    
        elif have_error:
            self.render("signup.html", **params)
        else:
            self.register_user(username, password, email)
            self.redirect(referer)
            
class Login(BlogHandler):
    def render_login(self, referer, username="",error = ""):
        self.render("login.html",username=username, error=error, referer=referer)
        
    def get(self):
        if self.user:
            self.redirect('/')
        else:
            self.render_login(referer=self.request.headers.get('referer','/'))
        
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        referer = self.verify_referer(str(self.request.get('referer')))
            
        if utils.valid_username(username) and utils.valid_password(password):
            user = Users.login(username,password)
                
        if user:
            self.set_secure_cookie("userID", str(user.key().id()))
            self.redirect(referer)  
        else:
            error = "Invalid login information"
            self.render_login(username,error)
            
            
class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect(self.verify_referer(self.request.headers.get('referer','/')))
        
        
class Archives(BlogHandler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Posts ORDER BY created;")
        self.render("archives.html", posts=posts)


class About(BlogHandler):
    def get(self):
        self.render("about.html")


class Contact(BlogHandler):
    def get(self):
        self.render("contact.html")
