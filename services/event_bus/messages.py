import pika


# def event_bus(
#     event_queue,
#     event_exchange="",
#     event_routing_key="basic",
#     event_body=None,
#     event_type=None,
#     *args,
#     **kwargs
# ):

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()


def publish(
    event_queue,
    event_exchange="",
    event_routing_key="basic",
    event_body=None,
    event_type=None,
    *args,
    **kwargs
):

    channel.queue_declare(event_queue)

    channel.basic_publish(
        exchange=event_exchange, routing_key=event_routing_key, body=event_body
    )
    print(" [x] Sent 'Hello World!'", event_body)


def subcribe(
    event_queue,
    event_exchange="",
    event_routing_key="basic",
    event_body=None,
    event_type=None,
    *args,
    **kwargs
):
    print("subcribe event called")

    def callback(ch, method, properties, body):
        print(" [x] Received callback methods", ch, method, properties, body)
        return body

    channel.basic_consume(
        queue=event_queue, auto_ack=True, on_message_callback=callback
    )
    channel.start_consuming()


# if event_type == "dispatch":
#     publish_event()
# elif event_type == "recieve":
#     subcribe_event()


# class EventBus:
#     def __init__(self, token=None, connection=None):
#         self.token = token

#     def produce(
#         self,
#         event_queue,
#         event_exchange="",
#         event_routing_key="basic",
#         event_body=None,
#         *args,
#         **kwargs
#     ):
#         global channel

#     def consume(
#         self,
#         event_queue,
#         event_exchange="",
#         event_routing_key="basic",
#         event_body=None,
#         *args,
#         **kwargs
#     ):
#         global channel

#         def callback(self, ch, method, properties, body):
#             print(" [x] Received callback methods", ch, method, properties, body)

#         channel.basic_consume(
#             queue=event_queue, auto_ack=True, on_message_callback=callback
#         )
#         channel.start_consuming()
