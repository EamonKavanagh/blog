import webapp2

import handlers
                    
application = webapp2.WSGIApplication([('/', handlers.Front), 
                                        ('/newpost', handlers.NewPost),
                                        ('/([0-9]+)', handlers.Post),
                                        ('/signup', handlers.Signup),
                                        ('/login', handlers.Login),
                                        ('/logout', handlers.Logout),
                                        ('/archives', handlers.Archives),
                                        ('/about', handlers.About),
                                        ('/contact', handlers.Contact)], 
                                        debug=True)