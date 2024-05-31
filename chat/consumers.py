from django.template.defaultfilters import slugify

from channels.generic.websocket import (
    AsyncJsonWebsocketConsumer
)

from .utils import (
    is_room_member,
    get_chat_rooms_updated,
    is_group_room_member,
    create_ws_room_msg_object,
    create_room_message_object,
)


class GroupActivityAsyncConsumer(AsyncJsonWebsocketConsumer):
    """
    This consumer is used to handle the messages sent to the Group activity chat.
    It is a async consumer. If the request's user does not belongs to the group room
    then he is not allowed to connect and send the messages.
    """

    async def connect(self):

        await self.accept()
        query_params = dict(
            (x.split('=') for x in self.scope['query_string'].decode().split("&")))
        group = query_params.get('group')
        user = self.scope['user']

        if user.is_authenticated and group:
            try:
                is_member, group_room = await is_group_room_member(user, group)
                print(is_member, group_room)
                if is_member:
                    self.group_name = slugify(
                        f'{group_room.group_name}-{group_room.id}')
                    await self.channel_layer.group_add(self.group_name, self.channel_name)
                else:
                    await self.send_json("You are not member of this group room")
                    await self.close(code=4000)
            except:
                await self.send_json("Invalid group id")
                await self.close(code=4000)
        else:
            await self.send_json("valid token and group is required in params to establish the connection!")
            await self.close(code=4000)

    async def receive_json(self, content, **kwargs):
        group = content.get('group')
        message = content.get('message')

        user = self.scope['user']
        if user.is_authenticated:
            message_obj = await create_ws_room_msg_object(group, user, message)
            message = message_obj
            await self.channel_layer.group_send(
                self.group_name, {
                    'type': 'chat.message',
                    'message': message
                }
            )

        else:
            await self.send_json("login required")

    async def chat_message(self, event):
        await self.send_json(event['message'])

    async def disconnect(self, code):
        # When disconnected remove the user from group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

class DashboardChatConsumer(AsyncJsonWebsocketConsumer):
    """
        This consumer is being used for personal chat. It is an async consumer.
        There are only two users in the room of this consumer between which personal
        chat will be executed. If the request's user does not belong to the
        group room then he is not allowed to connect and send the messages.
    """

    async def connect(self):
        await self.accept()
        query_params = dict(
            (x.split('=') for x in self.scope['query_string'].decode().split("&")))
        room_id = query_params.get('room_id')
        user = self.scope['user']

        if user.is_authenticated and room_id:
            try:
                is_member, group_name = await is_room_member(user, room_id)
                if is_member:
                    self.group_name = group_name
                    await self.channel_layer.group_add(self.group_name, self.channel_name)
                else:
                    await self.send_json("You are not member of this room")
                    await self.close(code=4000)
            except Exception as e:
                print(e)
                await self.send_json("Invalid room id")
                await self.close(code=4000)
        else:
            await self.send_json("valid token and room_id is required in params to establish the connection!")
            await self.close(code=4000)

    async def receive_json(self, content, **kwargs):
        room = content.get('room', )
        message = content.get('message')

        user = self.scope['user']

        if user.is_authenticated:
            is_member, group_name = await is_room_member(user, room)
            print(is_member, group_name)

            if is_member:

                message_obj = await create_room_message_object(
                    room=room,
                    user=user,
                    message=message,
                )

                message = message_obj
                print(message)

                await self.channel_layer.group_send(
                    group_name, {
                        'type': 'chat.message',
                        'message': message
                    }
                )

            else:
                await self.send_json("Invalid room id, i.e you are not the member of the given room")
                await self.close(code=4000)
        else:
            await self.send_json("login required")

    async def chat_message(self, event):

        await self.send_json(event['message'])

    async def disconnect(self, code):
        # When disconnected remove the user from group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )


"""
    This consumer is used to set the online and offline status of a user.
    It is a async consumer.
"""


# class OnlineStatusConsumer(AsyncJsonWebsocketConsumer):
#     async def connect(self):
#
#         user = self.scope['user']
#
#         if user.is_authenticated:
#
#             await self.accept()
#             self.group_name = "online_users"
#             await self.channel_layer.group_add(self.group_name, self.channel_name)
#             await create_online_user_instance(self.channel_name, user)
#             user_online_flag = await is_user_online(user)
#             if user_online_flag:
#                 await set_user_online(user)
#                 all_online_user = await all_online_users(self.channel_name)
#                 await self.channel_layer.group_send(
#                     self.group_name, {
#                         'type': 'user.is_offline',
#                         'message': all_online_user
#                     }
#
#                 )
#         else:
#             await self.send_json("login required")
#             await self.close(code=4000)
#
#     async def receive_json(self, content, **kwargs):
#         user = self.scope['user']
#
#         if user.is_authenticated:
#             self.group_name = "online_users"
#             await self.channel_layer.group_add(self.group_name, self.channel_name)
#             user_online_flag = await is_user_online(user)
#             if user_online_flag:
#                 all_online_user = await all_online_users(self.channel_name)
#                 await self.channel_layer.group_send(
#                     self.group_name, {
#                         'type': 'user.is_offline',
#                         'message': all_online_user
#                     }
#
#                 )
#         else:
#             await self.send_json("login required")
#             await self.close(code=4000)
#
#     async def disconnect(self, code):
#         # When disconnected remove the user from group
#         user = self.scope['user']
#
#         if user.is_authenticated:
#             profile_id = await delete_online_user_instance(user)
#
#             self.is_online_status = await delete_online_user_instance_check(user)
#
#             await self.channel_layer.group_send(
#                 self.group_name, {
#                     'type': 'user.is_offline',
#                     'message': [{
#                         "profile_id": profile_id,
#                         "is_online": self.is_online_status,
#                     }]
#                 }
#             )
#             await self.channel_layer.group_discard(
#                 self.group_name,
#                 self.channel_name,
#             )
#
#     async def user_is_offline(self, event):
#         await self.send_json(event['message'])


class ChatUpdateConsumers(AsyncJsonWebsocketConsumer):
    async def connect(self):

        await self.accept()
        user = self.scope['user']
        if user.is_authenticated:
            self.group_name = "chat_updates"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
        else:
            await self.send_json("login required")
            await self.close(code=4000)

    async def disconnect(self, code):
        # When disconnected remove the user from group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def chat_update(self, event):
        await self.send_json(event['message'])

    async def receive_json(self, content, **kwargs):
        user = self.scope['user']
        if user.is_authenticated:

            get_rooms_chat_update_object = await get_chat_rooms_updated(user, self.scope)
            message = get_rooms_chat_update_object

            await self.channel_layer.group_send(
                'chat_updates', {
                    'type': 'chat.update',
                    'message': message
                }
            )

        else:
            await self.send_json("login required")

    async def chat_message(self, event):
        await self.send_json(event['message'])

    async def disconnect(self, code):
        # When disconnected remove the user from group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )


# class UserOnlineStatusConsumer(AsyncJsonWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         user = self.scope['user']
#
#         if user.is_authenticated:
#             self.group_name = "online_users_status"
#             await self.channel_layer.group_add(self.group_name, self.channel_name)
#         else:
#             await self.send_json("login required")
#             await self.close(code=4000)
#
#     async def receive_json(self, content, **kwargs):
#         user = self.scope['user']
#         user_profile_id = content['profile_id']
#         if user.is_authenticated:
#             online_status = await is_user_online_check(user_profile_id)
#
#             if online_status:
#                 await self.channel_layer.group_send(
#                     'online_users_status', {
#                         'type': 'user.online.status',
#                         'message': [{
#                             "profile_id": user_profile_id,
#                             "is_online": True
#                         }]
#                     })
#             else:
#                 await self.channel_layer.group_send(
#                     'online_users_status', {
#                         'type': 'user.online_status',
#                         'message': [{
#                             "profile_id": user_profile_id,
#                             "is_online": online_status
#                         }]
#                     }
#                 )
#
#         else:
#             await self.send_json("login required")
#
#     async def disconnect(self, code):
#         # When disconnected remove the user from group
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name,
#         )
#
#     async def user_online_status(self, event):
#         await self.send_json(event['message'])
