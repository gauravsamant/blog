import os
import sys
import json
import importlib
from pathlib import Path
from django.conf import settings

base_dir = Path(settings.BASE_DIR).resolve().parent
sys.path.append(os.path.join(base_dir, "services", "event_bus"))

event_manager_path = sys.path[-1]
messages = importlib.import_module("messages", event_manager_path)
from messages import publish, subcribe


class EventManager:
    def __init__(
        self,
        request,
        event_name=None,
        event_type=None,
        event_topic=None,
        event_queue=None,
        event_body=None,
    ):
        self.request = request
        self.event_name = event_name
        self.event_type = event_type
        self.event_topic = event_topic
        self.event_queue = event_queue
        self.event_body = event_body
        if event_type == "dispatch":
            self.dispatch()
        elif event_type == "recieve":
            self.recieve()

    def create(self):
        token = self.request.headers.get("Authorization")
        if token:
            token = token.split(" ")[1]
        else:
            token = None
        self.data = json.dumps({"Authorization": token, "body": self.event_body})

    def dispatch(self):
        self.create()
        publish(
            event_queue=self.event_queue, event_body=self.data, event_type="dispatch"
        )

    def recieve(self):
        event = subcribe(event_queue="post_created", event_type="recieve")
        print(event)
