from celery import Celery

app = Celery()

app.conf.broker_url = ''

app.conf.broker_transport_options = {
    'region': 'us-east-1',
    'polling_interval': 10,
}


@app.task(acks_late=True, acks_on_failure_or_timeout=False)
def task1():
    print("this shit is not working")
    ex = 1/0
    return

