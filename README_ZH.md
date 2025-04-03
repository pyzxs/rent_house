[English](README.md) | [中文](README_ZH.md)

## 房屋出租项目

房屋出租项目

技术栈：
- 数据库： mysql
- 缓存： redis
- 消息队列： redis+celery
- 定时任务： redis+celery

### 一、项目安装
```shell
pip install -r requirement.txt
```

### 二、配置项目

配置项目都在`config`目录下各文件

* `settings.py`配置服务
* `development.py`测试服配置
* `production.py`正式服配置项
* `routers.py` 路由地址配置



数据库配置

```shell
ASYNC_SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://root:123456@127.0.0.1:3306/partner"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@127.0.0.1:3306/partner"
```



缓存配置

```shell
CACHE_DB_ENABLE = False
CACHE_DB_URL = "redis://:123456@127.0.0.1:6379/0"
```


定时任务及任务队列

```shell
SCHEDULE_ENABLE = True
SCHEDULE_BROKER_URL = 'redis://:123456@127.0.0.1:6379/0'
SCHEDULE_RESULT_URL = 'redis://:123456@127.0.0.1:6379/1'
SCHEDULE_RESULT_EXPIRE = 60 * 60 * 24
```

### 三、项目启动

启动web服务，默认端口9527

```shell
python main.py run
```

初始化超级管理员和管理员角色

```shell
python main.py migrate
```

启动消息队列
```shell
python main.py queue
```

启动定时任务
```shell
python main.py crontab
```
