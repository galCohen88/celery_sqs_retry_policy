import warnings

from celery.contrib import rdb

from kombu.asynchronous.aws.sqs import connection
from kombu.transport import virtual
from kombu.transport.SQS import Channel

class QoS(virtual.QoS):
    def reject(self, delivery_tag, requeue=False):
        super().reject(delivery_tag, requeue=requeue)
        queue_name, backoff_tasks, backoff_policy = self.extract_backoff_policy_configuration(delivery_tag)
        if queue_name and backoff_tasks and backoff_policy:
            self.apply_backoff_policy(queue_name, delivery_tag, backoff_policy, backoff_tasks)

    def extract_backoff_policy_configuration(self,  delivery_tag):
        queue_name = self._delivered.get(delivery_tag).delivery_info.get('routing_key')
        if not queue_name:
            return None, None, None
        queue_config = self.channel.predefined_queues.get(queue_name, {})
        backoff_tasks = queue_config.get('backoff_tasks')
        backoff_policy = queue_config.get('backoff_policy')
        return queue_name, backoff_tasks, backoff_policy

    def apply_backoff_policy(self, queue_name, delivery_tag, backoff_policy, backoff_tasks):
        warnings.warn(f"[apply_backoff_policy] {queue_name}, {delivery_tag} {backoff_tasks}, {backoff_policy}")
        queue_url = self.channel._queue_cache[queue_name]
        task_name, number_of_retries = self.extract_task_name_and_number_of_retries(delivery_tag)
        warnings.warn(f"[apply_backoff_policy] {task_name}, {number_of_retries}")
        if task_name in backoff_tasks:
            c = self.channel.sqs(queue_name)
            c.change_message_visibility(
                QueueUrl=queue_url,
                ReceiptHandle=delivery_tag,
                VisibilityTimeout=backoff_policy.get(number_of_retries)
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
