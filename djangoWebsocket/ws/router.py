from channels.routing import route_class

from ws import consumers

channel_routing = [
    route_class(consumers.ChatServer, path=r"^/chat/"),
]
