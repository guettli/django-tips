# Güttli's opinionated Django Tips

# If you are new to Software Development

If you are new to software development, then there is a long road before you. But Django is a good choice, since it is a well established and very good documented framework.

First learn Python, then some HTML and CSS. Then Django and SQL.

After you learned the basics (Python, some HTML, some CSS), then use the [Django tutorial](https://docs.djangoproject.com/en/dev/intro/tutorial01/).

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

# Testing:

[pytest-django](https://github.com/pytest-dev/pytest-django)

pytest.ini:
```
[pytest]
DJANGO_SETTINGS_MODULE = mysite.settings
FAIL_INVALID_TEMPLATE_VARS = True
```

`FAIL_INVALID_TEMPLATE_VARS` causes the rendering of a template to fail, if a template variable does not exist. I like this. See Zen-of-Python "Errors should never pass silently."

See [pytest-django docs "fail for invalid variables in templates](https://pytest-django.readthedocs.io/en/latest/usage.html#fail-on-template-vars-fail-for-invalid-variables-in-templates)

Or you use [django-shouty-templates](https://pypi.org/project/django-shouty-templates/) which monkey-patches some django methods to shout as soon as there is something strange.

# Django Packages Overview

[djangopackages.org](https://djangopackages.org/)

# Angular, React, Vue .... or ....

If you follow the current hype, you get the impression that web applications must be build like this: 

There is a backend (for example Django) which provides an http-API. This API gets used by a
JavaScript application written in Angular, React, or Vue.

Wait, slow down.

I think there is a simpler and more efficient way to develop an web application: Just create
HTML on the server side with Django.

To make your HTML look good on mobile and desktop use [Bootstrap5](https://getbootstrap.com/docs/5.0/getting-started/introduction/).

To make your application load/submit HTML snippets (to avoid the full scree refresh) you can use [htmx](https://htmx.org).

This way you have a simple stack which gives you a solid fundation for your application.


# Login via Google, Amazon, ...?

Use [django-allauth](https://django-allauth.readthedocs.io/en/latest/)

# Ask Questions

Asking questions is important. It pushes you and others forward.

But you need to dinstinguish between vague and specific questions.


## Vague Question?

Ask in the [Django Forum](https://forum.djangoproject.com/) or in a Django Facebook Group. For example [Django Python Web Framework](https://www.facebook.com/groups/python.django)

For example: "Which IDE should I use for ...". 

## Specific Question?

Ask on [Stackoverflow](https://stackoverflow.com/questions/tagged/django)

The best questions provide some example code which can be executed easily. This increases the likelihood that
someone will provide an answer soon.

If your code creates a stacktrace, then please add the whole stacktrace to the question.

# Survey

[Community Survey 2020](https://www.djangoproject.com/weblog/2020/jul/28/community-survey-2020/)

Unfortunately not that cool like [state of js](https://stateofjs.com/) or [state of css](https://stateofcss.com/),
but the Django Survey gives you a nice overview, too.

# Software built with Django

* [OpenSlides](https://openslides.com/) OpenSlides is the all-in-one solution for running your plenary meetings and conferences. 
* [Taiga](https://github.com/taigaio/taiga-back) Agile project management platform. Built on top of Django and AngularJS

# Related

* [Güttli's opinionated Python Tips](https://github.com/guettli/python-tips)
* [Güttli working-out-loud](https://github.com/guettli/wol)


