import webapp2

import handlers
                    
application = webapp2.WSGIApplication([('/blog/?', handlers.Front), 
                                        ('/blog/newpost', handlers.NewPost),
                                        ('/blog/([0-9]+)', handlers.Post),
                                        ('/blog/signup', handlers.Signup),
                                        ('/blog/welcome', handlers.Welcome),
                                        ('/blog/login', handlers.Login),
                                        ('/blog/logout', handlers.Logout),
                                        ('/blog/archives', handlers.Archives),
                                        ('/blog/about', handlers.About),
                                        ('/blog/hire', handlers.Hire),
                                        ('/blog/contact', handlers.Contact)], 
                                        debug=True)