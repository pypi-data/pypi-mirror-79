from .amqp_command import AMQPCommand


class Send(AMQPCommand):

    def execute(self, args, channel):
        channel.basic_publish(exchange='',
                              routing_key=args.queue_name,
                              body=args.message)

    def add_command_arguments(self, parser):
        parser.add_argument('queue_name', help="target queue")
        parser.add_argument('message', help="message to be sent")

    def get_help(self):
        return 'send message to channel'