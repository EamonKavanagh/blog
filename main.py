from handlers import *
        
                
application = webapp2.WSGIApplication([('/blog/?', Front), 
                                        ('/blog/newpost',NewPost),
                                        ('/blog/([0-9]+)',Post),
                                        ('/blog/signup',Signup),
                                        ('/blog/welcome',Welcome),
                                        ('/blog/login',Login),
                                        ('/blog/logout',Logout),
                                        ('/blog/archives',Archives),
                                        ('/blog/about',About),
                                        ('/blog/hire',Hire),
                                        ('/blog/contact',Contact)], 
                                        debug=True)