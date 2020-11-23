from kombu.kombu.transport import virtual
from kombu.transport.SQS import Channel

exponential_retry_tasks = ['svc.tasks.tasks.task1']

# retry policy (after first task was executed)
# 1st - 2mins
# 2nd - 5mins
# 3rd - 30min
# 4th - 1hr
# 5th - 3hr
# 6th - 6hr
# 7th - 8.5hr
retry_policy = {1: 120, 2: 300, 3: 1800, 4: 3600, 5: 10800, 6: 21600, 7: 30600}
queue_name = 'SQS_queue'


class QoS(virtual.QoS):
    def reject(self, delivery_tag, requeue=False):
        super().reject(delivery_tag, requeue=requeue)
        self.change_message_visibility_timeout(delivery_tag)

    def change_message_visibility_timeout(self, delivery_tag):
        queue_url = self.channel._queue_cache[queue_name]
        task_name, number_of_retries = self.extract_task_name_and_number_of_retries(delivery_tag)
        if task_name in exponential_retry_tasks:
            c = self.channel.sqs(queue_name)
            c.change_message_visibility(
                QueueUrl=queue_url,
                ReceiptHandle=delivery_tag,
                VisibilityTimeout=retry_policy.get(number_of_retries)
            )

    def extract_task_name_and_number_of_retries(self, delivery_tag):
        message = self._delivered.get(delivery_tag)
        message_headers = message.headers
        task_name = message_headers.get['task']
        number_of_retries = message_headers['retries']
        return task_name, number_of_retries


Channel.QoS = QoS