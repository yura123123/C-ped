import global_vars

import re

from flask_socketio import disconnect

from defines import (
    SERVER_PERMISSION_NONE,
    SERVER_PERMISSION_BASIC,
    USER_ID_ANONYMOUS,
)


class Client_Info:
    def __init__(self, user_id=USER_ID_ANONYMOUS, ip=""):
        # Placeholder, as for setter to work properly.
        self._user_id = USER_ID_ANONYMOUS
        self.user_id = user_id

        if ip in global_vars.client_infos_by_ip.keys():
            global_vars.client_infos_by_ip[ip].append(self)
        else:
            global_vars.client_infos_by_ip[ip] = [self]

        self.clients_connected = 0

        self.loaded = True

    @staticmethod
    def get(user_id, ip):
        if str(user_id) in global_vars.client_infos_by_user_id.keys():
            return global_vars.client_infos_by_user_id[str(user_id)]

        return Client_Info(user_id=user_id, ip=ip)

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, new_id):
        if new_id != self._user_id:
            lookup = global_vars.client_infos_by_user_id
            if str(self._user_id) in lookup.keys():
                lookup.pop(str(self._user_id))
            self._user_id = new_id
            lookup[str(self._user_id)] = self

    def on_client_connection(self, client):
        self.clients_connected += 1

        if self.clients_connected == 1:
            global_vars.client_count += 1

    def on_client_disconnection(self, client):
        self.clients_connected -= 1

        if self.clients_connected == 0:
            global_vars.client_count -= 1


class Client:
    def __init__(self, session_obj, request_obj, current_user):
        self.ip = request_obj.remote_addr
        self.sid = request_obj.sid

        self.user_info = current_user
        if self.user_info.is_authenticated() and self.user_info.is_active():
            self.client_info = Client_Info(
                user_id=self.user_info.user_id, ip=self.ip)
        else:
            self.client_info = Client_Info(ip=self.ip)

        self.disconnecting = False

    """
    def update_info(self, session_obj, request_obj):
        self.user_info = User_Info.get_by_session(session_obj, request_obj)
        if self.user_info is not None:
            self.client_info = Client_Info.get(self.user_info.user_id, self.ip)
            return

        if self.ip in global_vars.client_infos_by_ip.keys():
            for pos_client_info in global_vars.client_infos_by_ip[self.ip]:
                if pos_client_info.user_id == USER_ID_ANONYMOUS:
                    self.user_info = Guest_Info()
                    self.client_info = pos_client_info
                    return

        self.user_info = Guest_Info()
        self.client_info = Client_Info(ip=self.ip)
    """

    def on_connect(self):
        global_vars.clients_by_sid[self.sid] = self
        self.client_info.on_client_connection(self)
        print(
            "Received Connection("
            + str(global_vars.client_count)
            + "/"
            + str(global_vars.max_client_count)
            + ") from user("
            + str(self.ip)
            + ")("
            + str(self.client_info.clients_connected)
            + ")"
        )

    def on_disconnect(self):
        self.disconnecting = True

        global_vars.clients_by_sid.pop(self.sid)
        self.client_info.on_client_disconnection(self)
        print(
            "Lost Connection("
            + str(global_vars.client_count)
            + "/"
            + str(global_vars.max_client_count)
            + ") to user("
            + str(self.ip)
            + ")("
            + str(self.client_info.clients_connected)
            + ")"
        )

        self.client_info.loaded = False

    def disconnect(self):
        disconnect(self.sid)
