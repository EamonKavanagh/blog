from handlers import *
        
                
application = webapp2.WSGIApplication([('/blog/?', Front), 
                                        ('/blog/newpost',NewPost),
                                        ('/blog/([0-9]+)',Post),
                                        ('/blog/signup',Signup),
                                        ('/blog/welcome',Welcome),
                                        ('/blog/login',Login),
                                        ('/blog/logout',Logout),
                                        ('/blog/\.json',Json),
                                        ('/blog/([0-9]+)\.json',JsonPost)], 
                                        debug=True)