from .common import *


DEBUG = True

SECRET_KEY = 'django-insecure-+)a(+m@%@7(tywvoc4z@iph5sh_#!^go$9282h=sg4%5cw^cla'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront3',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'password123'
    }
}
