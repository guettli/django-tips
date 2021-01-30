# Güttli's opinionated Django Tips

# If you are new to Software Development

If you are new to software development, then there is a long road before you. But Django is a good choice, since it is a well established and very good documented framework.

First learn Python, then some HTML and CSS. Then Django and SQL.

After you learned the basics (Python, some HTML, some CSS), then use the [Django tutorial](https://docs.djangoproject.com/en/dev/intro/tutorial01/).

Avoid ReactJS or Vue, since you might not need them. First start with the traditional approach: Create HTML on
the server and send it to the web browser.

If you want to use a CSS library, then use [Bootstrap5](https://getbootstrap.com/).

Avoid JQuery. It is dead. Unfortunately a lot of code snippets and examples depend on it, but
this will change during the next years.

You can start with SQLite, but sooner or later you should switch to PostgreSQL.

My hint: Don't dive too deep into JavaScript. It is less important than most people think.

# How to extend the user model in Django?

The answer is simple: Don't extend the Django user model via inheritance and don't replace the original implementation.

Just use a [OneToOneField](https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.OneToOneField)

There is a nice article about how to integrate this into the admin: [Vitor Freitas "How to Add User Profile To Django Admin"](https://simpleisbetterthancomplex.com/tutorial/2016/11/23/how-to-add-user-profile-to-django-admin.html)

# Project vs App

It is important to understand the difference between a project and an application in the context of Django.
Please read [Projects and Applications](https://docs.djangoproject.com/en/3.1/ref/applications/#projects-and-applications)

I always try to keep the project small. The project is a small container. It contains the app.
The project contains settings, but almost no code.

# Project `mysite`

I always call the project `mysite`, like in the Django tutorial.
 
This has the benefit that settings.py, pytest.ini, wsgi.py and many other
files are almost identical between my different projects.

# Templates

## Use CSS, not "cycle"
Don't use (or try to understand) the [cycle](https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#cycle) templatetag. Today you don't need to alter the css class to create cebra-tables. Vanialla CSS is enough.

## Keep opening and closing tag together

foo/start-overview.html
```
<table>
 <tr><th>Col1</th>...</tr>
 ...
```

foo/end-overview.html
```
</table>
```

===> NO!

Keep the opening and closing tag together!

foo/overview.html
```
<table>
 {% include 'foo/overview-heading.html' %}
 ...
</table>
```

## Global Constants (Brand)

Imagine you have a setting called `brand` which is the name of your site. And since you develop re-usable software ([White-label product
](https://en.wikipedia.org/wiki/White-label_product)) the brand is customizable.

Usualy I would store this value in the database, but for customizing the django admin, it easier if the value is available before
the databaes connection is made.

settings.py
```
BRAND = 'foo'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
               ...
                'foo.context_processor.constants',  # make some global constants available in all templates
```



mysite/urls.py
```

admin.site.site_header = '{} Admin'.format(settings.BRAND)
admin.site.index_title = '{} Admin'.format(settings.BRAND)
admin.site.site_title = '{} Admin'.format(settings.BRAND)

urlpatterns = [
    path('admin/', admin.site.urls),
    ...
```

foo/context_processor.py
```
from django.conf import settings

def constants(request):
    return dict(brand=settings.BRAND)
```

# Django Debug Toolbar

The [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/) is really useful. I even enable it
in production.


# Testing

## pytest-django for Unittests

Use the library [pytest-django](https://github.com/pytest-dev/pytest-django). Their docs are good.

If you want to get an exception (as opposed to an empty string) if a template variable is unknown, then you can use this config:

pytest.ini:
```
[pytest]
DJANGO_SETTINGS_MODULE = mysite.settings
FAIL_INVALID_TEMPLATE_VARS = True
```

`FAIL_INVALID_TEMPLATE_VARS` causes the rendering of a template to fail, if a template variable does not exist. I like this. See Zen-of-Python "Errors should never pass silently."

See [pytest-django docs "fail for invalid variables in templates](https://pytest-django.readthedocs.io/en/latest/usage.html#fail-on-template-vars-fail-for-invalid-variables-in-templates)

Or you use [django-shouty-templates](https://pypi.org/project/django-shouty-templates/) which monkey-patches some django methods to shout as soon as there is something strange.

## Avoid Selenium Tests

Selenium automates browsers. It can automated modern browsers and IE. It is flaky. It will randomly fail, and you will waste a lot of time.
Avoid to support IE, and prefer to focus on development.

[Google Trend "Selenium"](https://trends.google.com/trends/explore?date=all&q=%2Fm%2F0c828v) is going down.

## Fixtures

Software test fixtures initialize test functions. They provide a fixed baseline so that tests execute reliably and produce consistent, repeatable, results. 

I don't need [Django Fixtures](https://docs.djangoproject.com/en/3.1/howto/initial-data/). If I need data in a production systems, I can use a script or database migration.

If I need data for a test, then I use [pytest fixtures](https://docs.pytest.org/en/stable/fixture.html)

And I don't see a reason to use a library like [factory-boy](https://factoryboy.readthedocs.io/en/stable/). Pytest and Django-ORM gives me all I need.

# Django Packages Overview

[djangopackages.org](https://djangopackages.org/)

# htmx

If you follow the current hype, you get the impression that web applications must be build like this: 

There is a backend (for example Django) which provides an http-API. This API gets used by a
JavaScript application written in Angular, React, or Vue.

Wait, slow down.

I think there is a simpler and more efficient way to develop an web application: Just create
HTML on the server side with Django.

To make your application load/submit HTML snippets (to avoid the full screen refresh) you can use [htmx](https://htmx.org).

This way you have a simple stack which gives you a solid foundation for your application.

# One Page, there forms

You want to create one HTML page which should three forms. The Django forms library is great, but it does not solve this problem for you.

You could use [Prefixes for forms](https://docs.djangoproject.com/en/3.1/ref/forms/api/#prefixes-for-forms) and put your three django-forms
into one big html `<form>`. Depending on the context, this often feels too heavy. 

That's where [htmx](#htmx) can help you: With htmx you can load/submit html fragments easily. No need to write a SPA (Single Page Application),
but if you want to, htmx gives you all you need.


# Responsive Web Design with Bootstrap

To make your HTML look good on mobile and desktop I use [Bootstrap5](https://getbootstrap.com/docs/5.0/getting-started/introduction/).

# Learn to distinguish between Django and Python

The Python ecosystem is much bigger than the Django ecosystem. 

For example you want to visualize data.
Don't search for a django solution, search for a Python solution. For example: [Holoviews](https://github.com/holoviz/holoviews)

Or use a JS based solution. For example [d3](https://github.com/d3/d3)

# Avoid request.user

Imagine you write a page so that the user is able to edit his/her address. You used request.user and everything works fine. 


Now you want to make the same form available
to a superuser, so that the superuser can edit the address of a user.

Now things get mixed up. Because `request.user` is not longer the user of the address ....

You can avoid the confusion if you avoid `request.user` and instead require that the caller explicitly gives you
an user object.


# Development Environment

In the past I had the whole stack installed in my local development environment (Apache or Nginx/Gunicorn), but
I don't do this any more. The `runserver` of Django is enough for development. You usualy don't need https during development, http is enough.

This contradicts the guideline that the development environment and the production environment should be equal.
Several years I used the same setup on dev and prod. But now I think runserver is enough. The runserver reloads code fast,
which is great for a fluent "edit test" cycle.

I develop on Ubuntu Linux.

But I use PostgreSQL even for development. If you use the same username for your PostgreSQL-user like for your
Linux-user, then you don't need to configure a password for the database.

# Production Environment

I use a cheap VPS from Hetzner. Every system I run on the VPS has its own Linux user. Every Linux-User has a virtualenv in $HOME,
which gets activated in .bashrc. This is handy if you want to check something with SSH.

I run `gunicorn` webserver via an Systems like explained in the [Gunicorn Deploying Docs](https://docs.gunicorn.org/en/stable/deploy.html#systemd)

This way I can run several systems on one VPS. This means there are N gunicorn processes.

As reverse proxy and https endpoint I use Nginx.

# Backup

First I run pg_dump, then [timegaps](https://pypi.org/project/timegaps/) to remove outdated dumps, then rsync to a second VPS.

# Login via Google, Amazon, ...?

Use [django-allauth](https://django-allauth.readthedocs.io/en/latest/)

# Static files

Use the library WhiteNoise, [even during development](http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development)

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

# Deploy: PaaS

* You can rent a VPS (Virtual Private Server). It is cheap. You can fiddle with ssh, vi and commandline tools to serve your application. Or you can use configuration management tools liks Ansible or Terraform.
* You can rent a PaaS (Heroku, Azure, AWS, ...)
* You can use an open source PaaS on your own VPS. See [Open Source PaaS List](https://github.com/guettli/open-source-paas)

# FBV vs CBV

"Function based Views" vs "Class based Views".

I like both.

CBV have some draw-back. If something does not work the way you want, then it is harder to debug the root-cause.

Example:

```
class MyView(FormView):
    form = MyForm
```

This will give you:

```
TypeError 'NoneType' object is not callable

.../django/views/generic/edit.py, line 33, in get_form
 return form_class(**self.get_form_kwargs()) 
 ```
 
 It will need some time to detect the root-cause. In this example the reason is a typo. You need to use `form_class = MyForm`.


# Uncaught Exception Handling: Sentry

During development on your local machine you get a nice debug-view if there is an uncaught exception.

On the production system you can a white page "Server Error (500)".

And of course, you want to know if users of your site get server error.

Personally I prefer simple open source solutions to free and great commercial solutions. But in this case I settled with [Sentry](//sentry.io/).

It is simple to set up, is free and shows all uncaught exceptions in an easy to use web GUI.

If someone knows an open source alternative, please let me know!

# Uptime Monitoring

Sentry won't help you, if there is something broken and your http server does not start. To be sure that your site is running you can use a free service.
There are several, I use https://uptimerobot.com/

They check your site every N minutes from outside via http.

# Page Speed

You can use [Lighthouse](https://developers.google.com/web/tools/lighthouse) (via Chrome) or [PageSpeed Insights (Google)](https://developers.google.com/speed/pagespeed/insights/) to check your page.

# Django settings.EMAIL_HOST

If you get `(421, '4.7.0 Try again later, closing connection.')` while sending mails via `settings.EMAIL_HOST = 'smtp.gmail.com'`, then
have a look at [this StackOverflow answer](https://stackoverflow.com/questions/65377421/django-force-ipv4-for-email-host-gmail-421-4-7-0-try-again-later-closing). It works if you use IPv4.

# Software built with Django

* [OpenSlides](https://openslides.com/) OpenSlides is the all-in-one solution for running your plenary meetings and conferences. 
* [Taiga](https://github.com/taigaio/taiga-back) Agile project management platform. Built on top of Django and AngularJS
* [Saleor](https://saleor.io/) e-commerce plattform

# Things which could get improved

"There are only two hard things in Computer Science: cache invalidation and naming things."

In ModelForm it is called "instance". In a class-based-view it is called "object". In Admin templates it is called "original". It would be nice to have **one** term for the thing.

# Dependecies to non-Python packages

Example: include a JS library like Bootstrap:

https://github.com/xstatic-py/xstatic


# Related

* [Güttli django-htmx-fun](https://github.com/guettli/django-htmx-fun) Small intro to htmx.
* [Güttli's opinionated Python Tips](https://github.com/guettli/python-tips)
* [Güttli working-out-loud](https://github.com/guettli/wol)


