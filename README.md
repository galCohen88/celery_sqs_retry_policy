# celery_sqs_retry_policy

### Exponential retry policy for Celery and SQS

## Look under celery.py

This is a monkey patch for Kombu QoS class, changing SQS visibility timeout exponentially

If you like to change the backoff policy / retry function, you can alter the celery.py=>retry_policy dictionary with a function

### AWS config
Docker-compose takes the queue URL, feel free changing it 
tasks.py file have hard coded values as well, feel free changing it 
app.conf.broker_url under tasks.py should be filled with sqs url with following format: 
```
sqs://<aws access key>:<aws secret>@sqs.us-east-1.amazonaws.com/<account id>/<queue name>
```


