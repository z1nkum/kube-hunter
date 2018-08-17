import json

import requests

from ...core.events import handler
from ...core.events.types import Event, OpenPortEvent, Service
from ...core.types import Hunter


class ApiServer(Service, Event):
    """The API server is in charge of all operations on the cluster."""
    def __init__(self):
        Service.__init__(self, name="API Server")

@handler.subscribe(OpenPortEvent, predicate=lambda x: x.port==443)
class ApiServerDiscovery(Hunter):
    """Api Server Discovery
    Checks for the existence of a an Api Server
    """
    def __init__(self, event):
        self.event = event

    def execute(self):
        main_request = requests.get("https://{}:{}".format(self.event.host, self.event.port), verify=False).text
        try:
            json.loads(main_request).get("code")
            self.event.role = "Master"
            self.publish_event(ApiServer())
        except:
            pass
