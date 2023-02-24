# Authentication

In this branch I will try to implement the authentication so only
logged in users could add quotes/authors.

This
[video](https://www.youtube.com/watch?v=71EU8gnZqZQ&ab_channel=ArpanNeupane)
helped a lot.

- [x] create db table for User model
- [x] create register/login forms
- [x] create register/login templates
- [x] create register/login routes
- [x] create password hashing with bcrypt
- [x] save user's username and hashed password to db
- [x] create validation(when user types password, must match with the
      hashed alternative in db)
- [x] create dashboard template/route
- [x] only logged in users can access dashboard
- [x] remove add_quote/author from common navbar and place it in dashboard
- [x] modify add_quote/author so only logged in users can add new ones
- [x] registration is allowed for all now, but in the future it should be
      disabled
- [x] when logged in user tries to access login route - get's
      redirected to dashboard

![demo](./demo.gif "demo of the branch")
