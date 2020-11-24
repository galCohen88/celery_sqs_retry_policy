from kombu.asynchronous.aws.sqs import connection
from kombu.transport import virtual
from kombu.transport.SQS import Channel

exponential_retry_tasks = ['svc.tasks.tasks.task1']

# retry policy (after first task was executed)
# 1st - 10sec
# 2nd - 15sec
# 3rd - 30sec
# 4th - 1min
# 5th - 2min
# 6th - 4min
# 7th - 8min
retry_policy = {1: 10, 2: 15, 3: 30, 4: 60, 5: 120, 6: 240, 7: 480}
queue_name = '<queue name>'


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
        task_name = message_headers['task']
        number_of_retries = int(message.properties['delivery_info']['sqs_message']['Attributes']['ApproximateReceiveCount'])
        return task_name, number_of_retries


Channel.QoS = QoS


receive_message = connection.AsyncSQSConnection.receive_message


def receive_message_with_receive_count(self, queue, queue_url, **kwargs):
    kwargs['attributes'] = ('ApproximateReceiveCount',)
    receive_message(self, queue, queue_url, **kwargs)


connection.AsyncSQSConnection.receive_message = receive_message_with_receive_count
