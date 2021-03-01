import urllib

from celery import Celery

app = Celery()

app.conf.broker_url = 'sqs://'

app.conf.broker_transport_options = {
    'predefined_queues': {
        'sqs-us-east-1-amazonaws-com_160043208412_try2': {
            'url': 'https://sqs.us-east-1.amazonaws.com/160043208412/sqs-us-east-1-amazonaws-com_160043208412_try2',
            'access_key_id': '***',
            'secret_access_key': '***',
            'backoff_policy': {1: 10, 2: 15, 3: 30, 4: 60, 5: 120, 6: 240, 7: 480},
            'backoff_tasks': ['svc.tasks.tasks.task1']
        }
    },
    'region': 'us-east-1',
    'polling_interval': 10,
}


@app.task(acks_late=True, acks_on_failure_or_timeout=False)
def task1():
    print("this shit is not working")
    ex = 1/0
    return

