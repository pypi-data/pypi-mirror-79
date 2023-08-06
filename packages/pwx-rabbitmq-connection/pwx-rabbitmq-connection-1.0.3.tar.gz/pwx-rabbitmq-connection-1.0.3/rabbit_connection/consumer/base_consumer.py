from json import loads
from pika.exceptions import ChannelWrongStateError, AMQPConnectionError, AMQPHeartbeatTimeout
from rabbit_connection import RabbitConnection
from time import sleep


class Consumer(RabbitConnection):
    __slots__ = ['_name', '__queue']

    def __init__(self, name, queue=None, host=None, port=None, number_messages=1, heartbeat=None):
        super().__init__(host, port, heartbeat=heartbeat)
        self._make_connection()
        self._name = name
        self.__queue = self._check_queue(queue)
        self._channel.queue_declare(self.__queue, durable=True)

        self.__set_exchange()
        self.__set_bind()
        self.__set_number_messages_to_receiver(number_messages)

    def __callback(self, ch, method, properties, message):
        pass

    @staticmethod
    def _get_json(message):
        return loads(message)

    def __set_consume(self):
        pass

    def __set_number_messages_to_receiver(self, number_messages):
        self._channel.basic_qos(prefetch_count=number_messages)

    def __set_exchange(self):
        self._channel.exchange_declare(exchange=self.__queue, exchange_type=self.exchange_type)

    def __set_bind(self):
        self._channel.queue_bind(exchange=self.__queue, queue=self.__queue, routing_key=self.__queue)

    @staticmethod
    def _set_ack(ch, method):
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        try:
            self._channel.start_consuming()

        except (ChannelWrongStateError, AMQPConnectionError):
            sleep(3)
            self._make_connection()
            self.start()
