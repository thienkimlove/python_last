### Working on project


#### Setup

* Create virtualenv `mkvirtualenv last`
* Install Django `1.11` `pip3 install Django`

* Create project dir `django-admin startproject last`

* Edit `last/settings.py`

* Create dirs `mkdir static`

* Create database.

* Create needed modules with `pip3`

```textmate
pip3 install django
pip3 install mysqlclient
```
* Run migrate `python3 manage.py migrate`

* Check if this working `python3 manage.py runserver 0.0.0.0:9160`. Access `http://192.168.99.100:9160/` to see.

*  Create admin `python3 manage.py createsuperuser` and using `root/tieungao/quan.dm@teko.vn`

* Access `http://192.168.99.100:9160/admin/`.

* Generation `pip3 freeze > requirements.txt` for later using `pip3 install -r requirements.txt`.

#### For deploy to host

* Edit `deploy` files.

* Commit to github.

* On the host, run below 

```textmate
mkvirtualenv backend
pip3 install -r requirements.txt
python3 manage.py collectstatic
ln -s /var/www/html/last/deploy/last.ini /etc/uwsgi/sites/last.ini
ln -s /var/www/html/last/deploy/local.last.vn /etc/nginx/sites-enabled/local.last.vn
mysql -uroot -ptieungao -e "create database python_last"
python3 manage.py migrate
python3 manage.py createsuperuser
deactivate
sudo systemctl restart uwsgi
service nginx restart
```
* Edit local `hosts` file 
```textmate
42.112.31.173 local.last.vn
```
And access `http://local.last.vn/admin/` to see everything is ok.

#### Customize Django Admin templates.

Please see in `settings.py` we have :

```textmate
'DIRS': [os.path.join(BASE_DIR, 'templates')],
```
Mean that we can copy the django admin templates and override this.


* Check where is django code `python -c "import django; print(django.__path__)"`

* Go do `/usr/local/lib/python3.5/dist-packages/django/contrib/admin/templates/admin`

* Copy `cp base_site.html /var/www/html/backend/templates/admin/base_site.html`

* Edit this template file.

#### Customizing your application’s templates

Astute readers will ask: But if `DIRS` was empty by default, how was Django finding the default admin templates? The answer is that, since `APP_DIRS` is set to `True`, Django automatically looks for a `templates/` subdirectory within each application package, for use as a fallback (don’t forget that `django.contrib.admin` is an application).

However, `templates` that belong to a particular application should be placed in that application’s template directory (e.g. `polls/templates`) rather than the project’s (templates)

#### Start working

* Create core app `django-admin startapp core`

* Copy `Ubold` Template files to `core/static/core`.

* Add `core` to `last/settings.py` INSTALLED_APPS and run `python3 manage.py collectstatic`.

All content from `core/static/core` will be copy to main `static` folder.

* Change `php templates` to `django templates` by read `https://oncampus.oberlin.edu/webteam/2012/09/architecture-django-templates`

```textmate
Check https://docs.djangoproject.com/en/2.0/ref/templates/builtins/#ref-templates-builtins-tags 

for built-in template tags.

check https://docs.djangoproject.com/en/2.0/howto/custom-template-tags/#howto-writing-custom-template-tags

for writing and registering template tags.

```

* URL Django

Check at https://www.webforefront.com/django/regexpdjangourls.html

````textmate

````
* Custom context processors
Custom Django context processors allow you to set up data for access on all Django templates
Read more about : `https://rock-it.pl/how-to-make-your-django-context-processors-lazy/`

* Working with Django View Decorators
View decorators can be used to restrict access to certain views. 
Django come with some built-in decorators, like `login_required`, `require_POST` or `has_permission`.  
For example only letting the user who created an entry of the model to edit or delete it.

Read more on `https://simpleisbetterthancomplex.com/2015/12/07/working-with-django-view-decorators.html`

* Set environment variables using `virtualenv` : `https://stackoverflow.com/questions/9554087/setting-an-environment-variable-in-virtualenv`
* Get Environment Variable with Python `name = os.environ.get('DATABASE_NAME')`

* This is not work perfectly so we setting in `backend/settings.py` and get with:

```textmate
from django.conf import settings
return settings.APP_NAME
```

* For MySQL with Django read `http://django-mysql.readthedocs.io/en/latest/checks.html`

* Using Transaction in Django

```textmate
from django.db import IntegrityError, transaction

@transaction.atomic
def viewfunc(request):
    create_parent()

    try:
        with transaction.atomic():
            generate_relationships()
    except IntegrityError:
        handle_exception()

    add_children()
```
* For setting something related to models, like index both field, table name, ... we using `Meta`

Read more on `https://docs.djangoproject.com/en/2.0/ref/models/options/`

* Multi Databases Django

```textmate
Not work for 2.0
https://github.com/mik3y/django-db-multitenant
https://gist.github.com/gijzelaerr/7a3130c494215a0dd9b2/
```

* Authentication data in Templates `https://docs.djangoproject.com/en/dev/topics/auth/default/#authentication-data-in-templates`

```textmate
Authentication data in templates
Users

When rendering a template RequestContext, the currently logged-in user, either a User instance or an AnonymousUser instance, is stored in the template variable {{ user }}:

{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}. Thanks for logging in.</p>
{% else %}
    <p>Welcome, new user. Please log in.</p>
{% endif %}

This template context variable is not available if a RequestContext is not being used.
Permissions

The currently logged-in user’s permissions are stored in the template variable {{ perms }}. This is an instance of django.contrib.auth.context_processors.PermWrapper, which is a template-friendly proxy of permissions.

Evaluating a single-attribute lookup of {{ perms }} as a boolean is a proxy to User.has_module_perms(). For example, to check if the logged-in user has any permissions in the foo app:

{% if perms.foo %}

Evaluating a two-level-attribute lookup as a boolean is a proxy to User.has_perm(). For example, to check if the logged-in user has the permission foo.can_vote:

{% if perms.foo.can_vote %}

Here’s a more complete example of checking permissions in a template:

{% if perms.foo %}
    <p>You have permission to do something in the foo app.</p>
    {% if perms.foo.can_vote %}
        <p>You can vote!</p>
    {% endif %}
    {% if perms.foo.can_drive %}
        <p>You can drive!</p>
    {% endif %}
{% else %}
    <p>You don't have permission to do anything in the foo app.</p>
{% endif %}

It is possible to also look permissions up by {% if in %} statements. For example:

{% if 'foo' in perms %}
    {% if 'foo.can_vote' in perms %}
        <p>In lookup works, too.</p>
    {% endif %}
{% endif %}


```

* Default permissions

When `django.contrib.auth` is listed in your `INSTALLED_APPS` setting, it will ensure that three default permissions – `add, change and delete` – are created for each Django model defined in one of your installed applications.

These permissions will be created when you run `manage.py migrate`; the first time you run migrate after adding `django.contrib.auth` to `INSTALLED_APPS`, the default permissions will be created for all previously-installed models, as well as for any new models being installed at that time. Afterward, it will create default permissions for new models each time you run `manage.py migrate` (the function that creates permissions is connected to the `post_migrate` signal).

Assuming you have an application with an app_label `foo` and a model named `Bar`, to test for basic permissions you should use:

```textmate
    add: user.has_perm('foo.add_bar')
    change: user.has_perm('foo.change_bar')
    delete: user.has_perm('foo.delete_bar')
```
The `Permission` model is rarely accessed directly.


* Work with Models
 
After create models , run 
```textmate
pip install Pillow
python manage.py makemigrations
python manage.py migrate
``` 
* DataTables from `https://bitbucket.org/pigletto/django-datatables-view`

* Debug Application

- Using `debug.log`

- Add `logto = /var/log/uwsgi/%(project).log` to `uwsgi` file.

- Check `/var/log/nginx/%(project)_error_log`

- Sometime we using wrong environments.

* Django Form 
Basic Form without 3th-packages.

`https://howchoo.com/g/ymuxmda4njk/introduction-to-django-forms`

Customize Form : `https://simpleisbetterthancomplex.com/article/2017/08/19/how-to-render-django-form-manually.html`

* Please check the good ebook `Django pattern and practices` and `Two Scoop Django`

for details about how we can resolve common problem with Django multi inherit.

Please note that with Django, we have many way to resolve problems 

for example using `Class-View` and `view functions`.

When inherit, basic django class and function always provide way to override and add more context

to basic class and function.

* Thinking about customize current Django Admin

- Method 1 (extends template) : `https://stackoverflow.com/questions/6583877/how-to-override-and-extend-basic-django-admin-templates` 

- Method 2 : Using Django default UI and just change code `https://www.webforefront.com/django/admincustomlayout.html`

- Method 3 : `https://medium.com/@hakibenita/how-to-turn-django-admin-into-a-lightweight-dashboard-a0e0bbf609ad`