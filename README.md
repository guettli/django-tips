# My opinionated Django Tips

# If you are new to Software Development

If you are new to software development, then there is a long road before you. But Django is a good choice, since it is a well established and very good documented framework.

First learn Python, then some HTML and CSS. Then Django and SQL.

Avoid ReactJS or Vue, since you might not need them. First start with the traditional approach: Create HTML on
the server and send it to the web browser.

If you want to use a CSS/JS library, then use [Bootstrap5](https://getbootstrap.com/).

Avoid JQuery. It is dead. Unfortunately a lot of code snippets and examples depend on it, but
this will change during the next years.

You can start with SQLite, but sooner or later you should switch to PostgreSQL.

# How to extend the user model in Django?

The answer is simple: Don't extend the Django user model via inheritance and don't replace the original implementation.

Just use a [OneToOneField](https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.OneToOneField)

There is a nice article about how to integrate this into the admin: [Vitor Freitas "How to Add User Profile To Django Admin"](https://simpleisbetterthancomplex.com/tutorial/2016/11/23/how-to-add-user-profile-to-django-admin.html)

# Django Packages Overview

[djangopackages.org](https://djangopackages.org/)

# Login via Google, Amazon, ...?

Use [django-allauth](https://django-allauth.readthedocs.io/en/latest/)

# Vague Question?

Ask in the [Django Forum](https://forum.djangoproject.com/)

or in a Django Facebook Group.

# Particular Question?

Ask on [Stackoverflow](https://stackoverflow.com/questions/tagged/django)

