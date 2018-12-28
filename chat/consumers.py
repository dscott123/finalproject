from django.conf import settings
from orders.models import Room
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ClientError(Exception):
	def __init__(self, code):
		super(ClientError, self).__init__(code)
		self.code = code

@database_sync_to_async
def get_room_or_error(room_id, user):
	try:
		room = Room.objects.get(pk=room_id)
	except Room.DoesNotExist:
		raise ClientError("ROOM_INVALID")
	if room.staff_only and not user.is_staff:
		raise ClientError("ROOM_ACCESS_DENIED")
	return room


class ChatConsumer(AsyncJsonWebsocketConsumer):
	async def connect(self):
		if self.scope["user"].is_anonymous:
			await self.close()
		else:
			await self.accept()
		self.rooms = set()

	async def receive_json(self, content):
		command = content.get("command", None)
		try:
			if command == "join":
				await self.join_room(content["room"])
			elif command == "leave":
				await self.leave_room(content["room"])
			elif command == "send":
				await self.send_room(content["room"], content["message"])
		except ClientError as e:
			await self.send_json({"error": e.code})

	async def disconnect(self, code):
		for room_id in list(self.rooms):
			try:
				await self.leave_room(room_id)
			except ClientError:
				pass

	async def join_room(self, room_id):
		room = await get_room_or_error(room_id, self.scope["user"])
		if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
			await self.channel_layer.group_send(
				room.group_name,
				{
					"type": "chat.join",
					"room_id": room_id,
					"username": self.scope["user"].username,
				}
			)
		self.rooms.add(room_id)
		await self.channel_layer.group_add(
			room.group_name,
			self.channel_name,
		)
		await self.send_json({
			"join": str(room.id),
			"title": room.name
			})

	async def leave_room(self, room_id):
		room = await get_room_or_error(room_id, self.scope["user"])
		if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
			await self.channel_layer.group_send(
				room.group_name,
				{
					"type": "chat.leave",
					"room_id": room_id,
					"username": self.scope["user"].username,
				}
			)
		self.rooms.discard(room_id)
		await self.channel_layer.group_discard(
			room.group_name,
			self.channel_name,
		)
		await self.send_json({
			"leave": str(room.id)
			})

	async def send_room(self, room_id, message):
		if room_id not in self.rooms:
			raise ClientError("ROOM_ACCESS_DENIED")
		room = await get_room_or_error(room_id, self.scope["user"])
		await self.channel_layer.group_send(
			room.group_name,
			{
				"type": "chat.message",
				"room_id": room_id,
				"username": self.scope["user"].username,
				"message": message,
			}
		)

	async def chat_join(self, event):
		await self.send_json(
			{
				"msg_type": settings.MSG_TYPE_ENTER,
				"room": event["room_id"],
				"username": event["username"],
			},
		)

	async def chat_leave(self, event):
		await self.send_json(
			{
				"msg_type": settings.MSG_TYPE_LEAVE,
				"room": event["room_id"],
				"username": event["username"],
			}
		)

	async def chat_message(self, event):
		await self.send_json(
			{
				"msg_type": settings.MSG_TYPE_MESSAGE,
				"room": event["room_id"],
				"username": event["username"],
				"message": event["message"],
			},
		)