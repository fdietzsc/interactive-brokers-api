from celery import Celery
from celery.app import trace

app = Celery('ibc',
             backend='redis://redis:6379',
             broker='pyamqp://guest@rabbitmq//',
             include=['ibc.session',
                      'ibc.tasks.accounts',
                      'ibc.tasks.portfolio'])

# prevent the task logger from showing task results
trace.LOG_SUCCESS = """\
Task %(name)s[%(id)s] succeeded in %(runtime)ss\
"""

app.conf.task_default_queue = 'ibc'
