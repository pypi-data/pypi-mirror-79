from agent.scheduler import logger
from agent.scheduler.scheduled_task import ScheduledTask


class RabbitMQTask(ScheduledTask):
    def execute(self):
        from agent.rabbitmq.client import RabbitMqClient

        client = RabbitMqClient.get_instance()
        if not client.thread.is_alive():
            client.thread.join()
            client.start_consuming_messages_to_control_center()
            logger.info("RabbitMqClient restarted!")
