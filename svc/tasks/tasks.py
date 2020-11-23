from celery import Celery

app = Celery()

app.conf.broker_url = ''

app.conf.broker_transport_options = {
    'region': 'us-east-1',
    'polling_interval': 10,
}


@app.task(acks_late=True)
def task1():
    print("this shit is working")
    return

