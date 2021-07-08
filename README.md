# Güttli's opinionated Django Tips

# If you are new to Software Development

If you are new to software development, then there is a long road before you. But Django is a good choice, since it is a well established and very good documented framework.

First learn Python, then some HTML and CSS. Then Django and SQL.

After you learned the basics (Python, some HTML, some CSS), then use the [Django tutorial](https://docs.djangoproject.com/en/dev/intro/tutorial01/).

Avoid ReactJS or Vue, since you might not need them. First start with the traditional approach: Create HTML on
the server and send it to the web browser.

If you want to use a CSS library, then I recommend [Bootstrap5](https://getbootstrap.com/).

You can start with SQLite, but sooner or later you should switch to PostgreSQL.

My hint: Don't dive too deep into JavaScript. It is less important than most people think.

# How to extend the user model in Django?

The answer is simple: Don't extend the Django user model via inheritance and don't replace the original implementation.

Just use a [OneToOneField](https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.OneToOneField)

There is a nice article about how to integrate this into the admin: [Vitor Freitas "How to Add User Profile To Django Admin"](https://simpleisbetterthancomplex.com/tutorial/2016/11/23/how-to-add-user-profile-to-django-admin.html)

# Project vs App

It is important to understand the difference between a project and an application in the context of Django.
Please read [Projects and Applications](https://docs.djangoproject.com/en/3.1/ref/applications/#projects-and-applications)

I always try to keep the project small. The project is a small container. One projects contains several apps.
The project contains settings, but almost no code.

# Project `mysite`

I always call the project `mysite`, like in the Django tutorial.
 
This has the benefit that the env var `DJANGO_SETTINGS_MODULE` is always "mysite.settings" in all my personal projects.

# Templates

## Use CSS, not "cycle"

Don't use (or try to understand) the [Django cycle](https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#cycle) templatetag. Today you don't need to alter the css class to create cebra-tables. Vanilla CSS is enough.

## How to debug Django's url resolving?

If you are new to a big project, you might not easily see which view function does handle an URL.

You can use [resolve()](https://docs.djangoproject.com/en/dev/ref/urlresolvers/#resolve) to get the answer:

```
import django
django.setup()
from django.urls import resolve
print(resolve('/foo/bar/'))

--> ResolverMatch(func=foocms.views.bar_handler, args=('/foo/bar/',), kwargs={}, url_name=foocms, ...)

```

Now you know that `foocms.views.bar_handler` will handle requests to the URL `/foo/bar/`.

## Django Debug Toolbar.

The DDT is great.

Third party panel for DDT:

* https://github.com/mikekeda/django-debug-toolbar-line-profiler/

## Connect to production DB (read-only)

Sometimes you want to check some code against the production DB just for testing.

Getting changes through CI would take too long.

You can connect you local Django to the production DB, **and** make the connection
read-only.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ...
        'USER': ...
        'PASSWORD': ...
        'OPTIONS': {
            'options': '-c default_transaction_read_only=on'
        }
    }
}
```

Now you can run your local code connected to the production DB, and be sure that you don't break things.

See: https://stackoverflow.com/a/66986980/633961
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

# dot-env

settings.py

```
from dotenv import load_dotenv
from distutils.util import strtobool

load_dotenv()
DEBUG = strtobool(os.getenv('DEBUG'))
...

```


# Django Debug Toolbar

The [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/) is really useful. I even enable it
in production.


# Testing

## pytest-django for Unittests

I use the library [pytest-django](https://github.com/pytest-dev/pytest-django). Their docs are good.

If you want to get an exception (as opposed to an empty string) if a template variable is unknown, then you can use this config:

pytest.ini:
```
[pytest]
DJANGO_SETTINGS_MODULE = mysite.settings
FAIL_INVALID_TEMPLATE_VARS = True
```

`FAIL_INVALID_TEMPLATE_VARS` causes the rendering of a template to fail, if a template variable does not exist. I like this. See Zen-of-Python "Errors should never pass silently."

See [pytest-django docs "fail for invalid variables in templates](https://pytest-django.readthedocs.io/en/latest/usage.html#fail-on-template-vars-fail-for-invalid-variables-in-templates)

## django_assert_num_queries

[django_assert_num_queries](https://pytest-django.readthedocs.io/en/latest/helpers.html#django-assert-num-queries) is handy, if you want to ensure that the number of SQL queries does not increase over time.

## Avoid Selenium Tests

Selenium automates browsers. It can automated modern browsers and IE. It is flaky. It will randomly fail, and you will waste a lot of time.
Avoid to support IE, and prefer to focus on development.

[Google Trend "Selenium"](https://trends.google.com/trends/explore?date=all&q=%2Fm%2F0c828v) is going down.

I heared that PlayWright is modern solution to automate Chromium, Firefox and WebKit with a single API.

## html_form_to_dict()

If possible, I test methods without a http request in a small unittest.

On the other hand I would like to know if the html forms are usable by a web-browser.

I like to test my django forms like this:

1. I use `reverse()` to get an URL
1. I use the [pytest client](https://pytest-django.readthedocs.io/en/latest/helpers.html#client-django-test-client) to get a http response
1. I use [html_form_to_dict()](https://github.com/guettli/html_form_to_dict) to get a dictionary of the form which is in `response.content`
1. I set some values on `data`
1. I use the `client.post(url, data)` to submit the form

For an example, please see the README of [html_form_to_dict()](https://github.com/guettli/html_form_to_dict)

## Fixtures

Software test fixtures initialize test functions. They provide a fixed baseline so that tests execute reliably and produce consistent, repeatable, results. 

I don't need [Django Fixtures](https://docs.djangoproject.com/en/3.1/howto/initial-data/). If I need data in a production systems, I can use a script or database migration.

If I need data for a test, then I use [pytest fixtures](https://docs.pytest.org/en/stable/fixture.html)

And I don't see a reason to use a library like [factory-boy](https://factoryboy.readthedocs.io/en/stable/). Pytest and Django-ORM gives me all I need.

# Keep models.py small

The file `models.py` is a mixture. A mixture of schema definition and logic. That's handy and makes you fast at the beginning.

But don't put too much logic into this file. Your subclasses of `Model` should only contain basic methods.

Creating HTML and other stuff should live somewhere else.

I usualy create a file per model: If the model is called `Foo`, then I create a file called `fooutils.py` which contains
methods which get instance of the class `Foo` as first argument.

Example for a model called `Customer`:

```
# customerutils.py

def create_weekly_report(customer):
    ...
```
# Django Typed Models

[Django Typed Models](https://github.com/craigds/django-typed-models) brings [Single Table Inheritance](https://en.wikipedia.org/wiki/Single_Table_Inheritance) to Django.

I like it for use-cases like this: Imagine you want to track the changes which get done by a user. The user creates an account,
then the user adds his address. Later he creates an order, ....

You could create a model like this:

```Python
class Log(models.Model):
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_add_now=True)
    action = ....
    data = models.JSONField()    
```

`action` could be a CharField with choices, or a ForeignKey to a Model which contains all the possible choices as rows.

`data` stores the changes which fit to the specific action.

Example: the action "Order Created" needs a link to the relevant offer.

Every action has its own data schema.... Things get fuzzy if you use JSON.

OR you could use Single Table Inheritance:

```Python
class Log(TypedModel):
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_add_now=True)

class OrderCreatedLog(Log):
    offer = models.ForeignKey(Offer)
```    

This way you don't need JSON, you can use database column to store the values.

# Check HTML Middleware

I wrote a small Check HTML Middleware, so that typos in HTML get detected soon:

[django-check-html-middleware](https://github.com/guettli/django-check-html-middleware)


# Signal on changed fields

[django-fieldsignals](https://github.com/craigds/django-fieldsignals) is a handy library, so
that you can easily receive a signal if a field of a model has changed.



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

# One Page, three forms

You want to create one HTML page which contains three forms. The Django forms library is great, but it does not solve this problem for you.

You could use [Prefixes for forms](https://docs.djangoproject.com/en/3.1/ref/forms/api/#prefixes-for-forms) and put your three django-forms
onto one big page. Depending on the context, this often feels too heavy. 

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

Imagine you write a page so that the user is able to edit his/her address. You use request.user and everything works fine. 

Now you want to make the same form available
to a superuser, so that the superuser can edit the address of a user.

Now things get mixed up. Because `request.user` is not longer the user of the address ....

You can avoid the confusion if you avoid `request.user` and instead require that the caller explicitly gives you
an `user` object.


# Development Environment

In the past I had the whole stack installed in my local development environment (Apache or Nginx/Gunicorn), but
I don't do this any more. The `runserver` of Django is enough for development. You usualy don't need https during development, http is enough.

This contradicts the guideline that the development environment and the production environment should be equal.
The runserver reloads code fast,
which is great for a fluent "edit test" cycle.

I develop on Ubuntu Linux with PyCharm.

But I use PostgreSQL even for development. If you use the same username for your PostgreSQL-user like for your
Linux-user, then you don't need to configure a password for the database.

# Production Environment

I use a cheap VPS from Hetzner. Every system I run on the VPS has its own Linux user. Every Linux-User has a virtualenv in $HOME,
which gets activated in .bashrc. This is handy if you want to check something with SSH.

I run `gunicorn` webserver via an Systems like explained in the [Gunicorn Deploying Docs](https://docs.gunicorn.org/en/stable/deploy.html#systemd)

This way I can run several systems on one VPS. This means there are N gunicorn processes.

As reverse proxy and https endpoint I use Nginx.

Sooner or alter I will switch to containers, but at the moment my current setup works fine.

# Django's Jobs vs Webserver's Jobs: GZipMiddleware


You should understand that's the job of the webserver to provide `https` (Certificates ...) or to compress the responses.

It makes no sense to use the Django [GZipMiddleware](https://docs.djangoproject.com/en/dev/ref/middleware/#module-django.middleware.gzip).

# Django's Jobs vs Webserver's Jobs: SECURE_SSL_REDIRECT

The setting [SECURE_SSL_REDIRECT](https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECURE_SSL_REDIRECT): I think
redirecting from http to https should
be done by the web-server, not by Django.


# Full text search

PostgreSQL can do full text search, and Django supports it: [PG full text search](https://docs.djangoproject.com/en/dev/ref/contrib/postgres/search/)

You make your life easier, if you avoid a second system (for example ElasticSearch).

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

For example: "Which library should I use for ...". 

## Specific Question?

Ask on [Stackoverflow](https://stackoverflow.com/questions/tagged/django)

The best questions provide some example code which can be executed easily. This increases the likelihood that
someone will provide an answer soon.

If your code creates a stacktrace, then please add the whole stacktrace to the question.

# Survey

[Community Survey 2020](https://www.djangoproject.com/weblog/2020/jul/28/community-survey-2020/)

Unfortunately not that cool like [state of js](https://stateofjs.com/) or [state of css](https://stateofcss.com/),
but the Django Survey gives you a nice overview, too.

# Forms

I like the Django Forms Library. I don' use third party packages like crispy forms.

Rule of thumb: Don't access request.GET or request.POST. Always use a form to retrieve the values from the request.

# ORM: No Manager methods

I know [Adding extra manager methods](https://docs.djangoproject.com/en/dev/topics/db/managers/#custom-managers). But I don't like it.

I prefer to write a `@classmethod` if I want to return a custom querysets.


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

# Misc

* [get_object_or_404()](https://docs.djangoproject.com/en/dev/topics/http/shortcuts/#get-object-or-404) is handy.

# CSRF token is not needed.

If you use the default of [SESSION_COOKIE_SAMESITE](https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-samesite), then
you don't need a CSRF token. 

# Uncaught Exception Handling: Sentry

During development on your local machine you get a nice debug-view if there is an uncaught exception.

On the production system you get a white page "Server Error (500)".

And of course, you want to know if users of your site get server error.

Personally I prefer simple open source solutions to free and great commercial solutions. But in this case I settled with [Sentry](//sentry.io/).

It is simple to set up, is free and shows all uncaught exceptions in an easy to use web GUI.

And Sentry is a [Gold Corporate Member](https://www.djangoproject.com/foundation/corporate-members/) of the Django Software Foundation.

# Uptime Monitoring

Sentry won't help you, if there is something broken and your http server does not start. To be sure that your site is running you can use a free service.
There are several, I use https://uptimerobot.com/

They check your site every N minutes from outside via https.

# Cache for ever.

New content, new URL.

[django-storages](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html) `AWS_S3_FILE_OVERWRITE = False` forces you to use create+delete instead of updating content.

# Page Speed

You can use [Lighthouse](https://developers.google.com/web/tools/lighthouse) (via Chrome) or [PageSpeed Insights (Google)](https://developers.google.com/speed/pagespeed/insights/) to check your page.

# Software built with Django

* [OpenSlides](https://openslides.com/) OpenSlides is the all-in-one solution for running your plenary meetings and conferences. 
* [Taiga](https://github.com/taigaio/taiga-back) Agile project management platform. Built on top of Django and AngularJS
* [Saleor](https://saleor.io/) e-commerce plattform

# Things which could get improved

"There are only two hard things in Computer Science: cache invalidation and naming things."

In ModelForm it is called "instance". In a class-based-view it is called "object". In Admin templates it is called "original". It would be nice to have **one** term for the thing.

Don't ask me why in [reverse()](https://docs.djangoproject.com/en/3.1/ref/urlresolvers/#reverse) method is called "url" in Django templates.

The Django template language hides errors. I prefer [format_html()](https://docs.djangoproject.com/en/3.1/ref/utils/#django.utils.html.format_html)

# Migrations

## Don't change old migrations

Don't change old migrations which you already pushed to a central repository. It is likely that someone already pulled your changes into his
development environment. This developer will have trouble if you change the old migration. Create a new migration which fixes the error of the
old migration.

## Linear Migrations

If you develop in a team you will sooner or later get trouble with your migrations, because two developers create a new migration
in their branch. The CI for each branch is fine, but after merging both to the main branch you have two migrations with the same number. Grrr

[django-linear-migrations](https://pypi.org/project/django-linear-migrations/) helps you. At least you know during merging that there is a conflict.

The solution is simple:

> It does this by creating new files in your apps’ migration directories, called max_migration.txt. These files contain the latest migration name for that app, and are automatically updated by makemigrations.

Big thank you to Adam Chainz for this package.

# Raw SQL Queries

Since the ORM solves most use-cases many developers don't use raw SQL queries in Django. This does not mean they are "evil".

With the help of [Subquery](https://docs.djangoproject.com/en/dev/ref/models/expressions/#subquery-expressions) and [OuterRef](https://docs.djangoproject.com/en/dev/ref/models/expressions/#django.db.models.OuterRef) complex queries are possible. But
nevertheless, I think SQL is more readable than ORM queries containing `OuterRef(OuterRef(...))`.

If a raw SQL query is easier to understand than the ORM counterpart (and there is a test for it), then go for SQL.

But of course you should be aware of SQL-injection and use parameters like documented:

```
Person.objects.raw('SELECT * FROM myapp_person WHERE last_name = %s', [lname])
```

# Serving private files

Imagine you have private files which you don't want to serve via a CDN. You could use a hard to guess random
string in the URL, but that's not a real solution.

You can use the "x-sendfile" approach. This way you can do the authentication and permission checking in your
Python code, and then let the webserver (for example Nginx) handle the slow work of sending the file over the wire.

Setting the appropriate http headers is not hard. But you can use [django-sendfile2](https://github.com/moggers87/django-sendfile2), too.

# Fast Inner Feedback Loop

The inner feedback loop:

1. Edit
2. Save
3. Compile
4. Run
5. Check result

With Python and a modern IDE "Save" and "Compile" are not needed.

Nevertheless it takes some time to see the result.

If you are fiddling with HTML+CSS you might be faster if you edit the HTML+CSS directly in the browser. For example in devtools (Chrome).

In most cases step "5. Check result" means to see if a test was successful or not. Test-Driven Development makes you faster in the long run.

# ORM: All Users which are at least in one group:

```
User.objects.filter(groups__isnull=False)
```

Related: https://stackoverflow.com/questions/54367178/django-orm-all-users-which-have-at-least-one-group

# Show SQL

```
User.objects.filter(...).query
```

# Disk-Cache instead of Redis

[python-diskcache](https://github.com/grantjenks/python-diskcache) is an replacement for the [FileBasedCache](https://docs.djangoproject.com/en/dev/topics/cache/#filesystem-caching). For small projects you might need
a Redis server.

# Template Language

## Comma separated list of HTML
You want to list some hyperlinks separated by comma?
```
{% for obj in mylist %}
 <a href="{{obj.get_absolute_url}}">{{obj}}</a>{% if not forloop.last %}, {% endif %}
{% endfor %}
```

See ["for" in Built-in Template Language](https://docs.djangoproject.com/en/dev/ref/templates/builtins/#for)

# Not solved yet: Row based permissions

Row based (AKA "per object permissions") are not easy. There are several solutions:

[django-gardian](https://django-guardian.readthedocs.io/en/stable/) Drawback: Slow. See [Performance](https://django-guardian.readthedocs.io/en/stable/userguide/performance.html)

Use [get_queryset() in the admin](https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_queryset). This is
fast and flexible. But does not distinguish between "read permissions" and "write permissions".

# Dependecies to non-Python packages

Example: include a JS library like Bootstrap:

https://github.com/xstatic-py/xstatic

# Blogs

* [Adam Johnson](https://adamj.eu/tech/)

# Related

* [Güttli django-htmx-fun](https://github.com/guettli/django-htmx-fun) Small intro to htmx.
* [Güttli's opinionated Python Tips](https://github.com/guettli/python-tips)
* [Güttli's Programming Guidelines](https://github.com/guettli/programming-guidelines)
* [Güttli, why I like PyCharm](https://github.com/guettli/why-i-like-pycharm/)
* [Güttli working-out-loud](https://github.com/guettli/wol)


