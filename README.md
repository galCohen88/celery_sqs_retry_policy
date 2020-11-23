# Celery SQS exponential retry policy

### Exponential retry policy for Celery and SQS

## Look under celery.py

This is a monkey patch for Kombu QoS class, changing SQS visibility timeout exponentially, depending on number of retries

If you like to change the backoff policy / retry function, you can alter the celery.py=>retry_policy dictionary with a function

### AWS config
1. Docker-compose takes `<queue name>` argument, feel free changing it 
1. svc.app.api takes `<queue name>` parameter as well
1. svc.tasks.tasks takes `broker_transport_options`, change it accourding to your queue settings
1. svc.tasks.tasks takes `app.conf.broker_url`, hould be filled with sqs url with following format
```
sqs://<aws access key>:<aws secret>@sqs.us-east-1.amazonaws.com/<account id>/<queue name>
```
