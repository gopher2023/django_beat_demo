from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u0urs)ak(oo!2ixa=2e!kn(=!1wr^132c^n4o#benb3rl#$dat'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    # 'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01',
    'django_celery_beat', # 注册刚刚第三方模块
    # 'django_celery_results',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_celery_crawl.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_celery_crawl.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'django_celery', # 去mysql中创建数据库
#         'HOST':'localhost',
#         'PORT':'3306',
#         'USER':'root',
#         'PASSWORD':'123' # 自己写自己的密码
#     }
# }

DATABASES = {
    'default': {
        # 配置数据库引擎 ， 使用 MySQL 数据库
        'ENGINE': 'django.db.backends.mysql',
        'NAME' : 'book_store',
        'HOST' : 'localhost',
        'PORT' : '3306',
        'USER' : 'root',
        'PASSWORD' : '123',
        # 配置连接的数据库 ， 数据库必须先创建 ， 才可以进行链
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

############# celery的配置信息######
# 1 Broker配置，使用Redis作为消息中间件
BROKER_URL = 'redis://127.0.0.1:6379/1'
# 2 BACKEND配置，使用redis
RESULT_BACKEND = 'redis://127.0.0.1:6379/2'

BROKER_CONNECTION_RETRY_ON_STARTUP = True

# RESULT_BACKEND = 'django-db'  #使用django orm 作为结果存储
# CELERY_RESULT_BACKEND = 'django-db'

# 3 序列化方案--》json
ACCEPT_CONTENT = ['json']
TASK_SERIALIZER = 'json'
# 结果序列化方案
RESULT_SERIALIZER = 'json'

# 4 任务结果过期时间，秒
TASK_RESULT_EXPIRES = 60 * 60 * 24

# 5 时区配置
TIMEZONE = 'Asia/Shanghai'

USE_TZ = True
# 6 配置定时任务
# from datetime import timedelta
########## 以后不用这种思路设置定时任务--》注释掉 ##########
# CELERYBEAT_SCHEDULE = {
#     'every_5_second': {
#         'task': 'app01.tasks.add',
#         'schedule': timedelta(seconds=5),
#         'args': (33, 44),
#     }
# }
#只要配了这个，原来celery中的定时任务统一不能用了，需要我们手动配置了
CELERYBEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'



#### 发送邮件配置
# EMAIL_HOST = 'smtp.qq.com'  # 如果是 163 改成 smtp.163.com
# EMAIL_PORT = 465
# EMAIL_HOST_USER = '306334678@qq.com'  # 帐号
# EMAIL_HOST_PASSWORD = 'nbjpdbazeeflbjej'  # 密码
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
#这样收到的邮件，收件人处就会这样显示
#DEFAULT_FROM_EMAIL = 'lqz<'306334678@qq.com>'
# EMAIL_USE_SSL = True   #使用ssl
#EMAIL_USE_TLS = False # 使用tls

#EMAIL_USE_SSL 和 EMAIL_USE_TLS 是互斥的，即只能有一个为 True