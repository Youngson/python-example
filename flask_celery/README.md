# Flask and Celery

该示例用于描述如何使用celery和flask应用工厂。

## 安装

```
pip install -r requirements.txt
```

## 运行

运行测试服务器：

```
python manage.py develop
```

运行celery worker：

```
celery worker -A celery_worker.celery --loglevel=info
```

运行celery定时任务：

```
celery beat -A celery_worker.celery --loglevel=info
```