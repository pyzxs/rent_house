[English](README.md) | [中文](README_ZH.md)

## House Rental Project

rent house project

Tech Stack:
- database: mysql
- cache: redis
- mq: redis+celery
- crontab: redis+celery


### 1. Project Installation
```shell
# python 3.12.8
pip install -r requirement.txt
```

### 2. Project Configuration

All project configurations are located in the files under the `config` directory:

* `settings.py` - Service configuration
* `development.py` - Test environment configuration
* `production.py` - Production environment configuration
* `routers.py` - Route address configuration

#### Database Configuration

```shell
ASYNC_SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://root:123456@127.0.0.1:3306/rent_house"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@127.0.0.1:3306/rent_house"
```

#### Cache Configuration

```shell
CACHE_DB_ENABLE = False
CACHE_DB_URL = "redis://:123456@127.0.0.1:6379/0"
```

#### Scheduled Tasks and Task Queues

```shell
SCHEDULE_ENABLE = True
SCHEDULE_BROKER_URL = 'redis://:123456@127.0.0.1:6379/0'
SCHEDULE_RESULT_URL = 'redis://:123456@127.0.0.1:6379/1'
SCHEDULE_RESULT_EXPIRE = 60 * 60 * 24
```

### 3. Project Startup

Start the web service (default port: 9527)

```shell
python main.py run
```

Initialize the super administrator and admin role

```shell
python main.py migrate
```

Start the message queue

```shell
python main.py queue
```

Start scheduled tasks

```shell
python main.py crontab
```