from abc import abstractmethod
import os
import pika
from .command import Command

class AMQPCommand(Command):

    def add_arguments(self, parser):
        parser.add_argument('--amqp_client_key',
                            help="AMQP client key, will be read from AMQP_CLIENT_KEY environment variable by default",
                            default=os.getenv('AMQP_CLIENT_KEY'))
        parser.add_argument('--amqp_client_secret',
                            help="AMQP client secret, will be read from AMQP_CLIENT_SECRET environment variable by default",
                            default=os.getenv('AMQP_CLIENT_SECRET'))
        parser.add_argument('--amqp_host',
                            help="AMQP host, will be read from AMQP_HOST environment variable by default",
                            default=os.getenv('AMQP_HOST'))
        parser.add_argument('--amqp_port',
                            help="AMQP port, will be read from AMQP_PORT environment variable by default",
                            default=os.getenv('AMQP_PORT', 5742))
        parser.add_argument('--amqp_path',
                            help="AMQP path, will be read from AMQP_HOST environment variable by default",
                            default=os.getenv('AMQP_PATH', '/'))
        parser.add_argument('--amqp_queue_name',
                            help="AMQP queue name, will be read from AMQP_QUEUE_NAME environment variable by default",
                            default=os.getenv('AMQP_QUEUE_NAME'))

        parser.add_argument('--debug', action='store_true', help="debug")
        parser.add_argument('--listen', action='store_true', help="listen")

        self.add_command_arguments(parser)

    def run(self, args):
        credentials = pika.PlainCredentials(args.amqp_client_key, args.amqp_client_secret)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(args.amqp_host, args.amqp_port, args.amqp_path, credentials))
        channel = connection.channel()

        if args.listen:
            self.listen(args, channel)
        else:
            self.execute(args, channel)

    def listen(self, args, channel):
        channel.basic_consume(queue=args.amqp_queue_name,
                              on_message_callback=self.execute(args, channel))
        channel.start_consuming()

    @abstractmethod
    def execute(self, args, channel):
        pass

    @abstractmethod
    def add_command_arguments(self, parser):
        pass


