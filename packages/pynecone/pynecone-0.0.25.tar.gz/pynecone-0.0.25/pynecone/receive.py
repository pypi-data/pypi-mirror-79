from .amqp_command import AMQPCommand
from .script_command import ScriptCommand


class ReceiveCommand(AMQPCommand):

    def __init__(self):
        super().__init__("receive")

    def execute(self, args, channel):
        channel.basic_consume(queue=args.amqp_queue_name,
                              on_message_callback=ScriptCommand.load_script(args.script_path, args.func_name, args))
        channel.start_consuming()

    def add_command_arguments(self, parser):
        parser.add_argument('script_path', help="path to the script to be executed")
        parser.add_argument('func_name', help="name of the function in the script to be executed")

    def get_help(self):
        return 'receive help'