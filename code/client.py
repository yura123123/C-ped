import global_vars

import re

from flask_socketio import disconnect

from defines import (
    SERVER_PERMISSION_NONE,
    SERVER_PERMISSION_BASIC,
    USER_ID_ANONYMOUS,
)


def get_user_by_session(session_obj, request_obj):
    """
    Returns Client_Info of an authenticated user, if
    session_obj is who they pretend to be.

    Returns None otherwise.
    """
    """
    user_id = session_obj.get("user_id")
    key = session_obj.get("key")
    salt = session_obj.get("salt")

    if all(user_id, key, salt):
        db_user_cursor = db.cursor()

        combo_super_secret = key + salt
        hashed_super_secret = hashlib.sha512(
             combo_super_secret.encode('utf-8')
        ).digest()

        db_user_cursor.execute(
            "SELECT super_secret FROM users WHERE user_id=?",
            (user_id,)
        )

        for row in db_user_cursor.fetchall():
            if(hashed_super_secret == row[0]):
                lookup = global_vars.client_infos_by_user_id.keys()
                if str(user_id) in lookup:
                    return global_vars.client_infos_by_user_id[str(user_id)]
                else:
                    return Client_Info(
                        user_id=user_id,
                        ip=request_obj.remote_addr
                    )
    """
    return None


class Client_Info:
    def __init__(self, user_id=USER_ID_ANONYMOUS, ip=""):
        self.user_id = user_id

        # These we will get from the db.
        self._email = ""
        self._discord_id = ""
        self._permissions = SERVER_PERMISSION_BASIC

        global_vars.client_infos_by_user_id[str(user_id)] = self

        if ip in global_vars.client_infos_by_ip:
            global_vars.client_infos_by_ip[ip].append(self)
        else:
            global_vars.client_infos_by_ip[ip] = [self]

        self.clients_connected = 0

        if user_id != USER_ID_ANONYMOUS:
            self.load_from_db()

        self.loaded = True

    def load_from_db(self):
        """
        db_user_cursor = db.cursor()

        db_user_cursor.execute(
            "SELECT email, discord_id, permissions FROM users WHERE user_id=?",
            (self.user_id,)
        )
        for row in db_user_cursor.fetchall():
            self.email = row[0]
            self.discord_id = row[1]
            self.permissions = row[2]
        """
        pass

    def update_db(
        self,
        email="",
        discord_id="",
        permissions=SERVER_PERMISSION_NONE
    ):
        """
        if(self.user_id == USER_ID_ANONYMOUS):
            return

        if(email != "" and email != self.email):
            self.email = email
        if(discord_id != "" and discord_id != self.discord_id):
            self.discord_id = discord_id
        if(
            permissions != SERVER_PERMISSION_BASIC
            and permissions != self.permissions
        ):
            self.permissions = permissions

        update_user(self.user_id, email, discord_id, permissions)
        """
        pass

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email):
        if new_email != self._emaill:
            self._email = new_email
            self.update_db(email=new_email)

    @property
    def discord_id(self):
        return self._discord_id

    @discord_id.setter
    def discord_id(self, new_discord_id):
        if new_discord_id != self._discord_id:
            self._discord_id = new_discord_id
            self.update_db(permissions=new_discord_id)

    @property
    def permissions(self):
        return self._permissions

    @permissions.setter
    def permissions(self, new_permissions):
        if new_permissions != self._permissions:
            self._permissions = new_permissions
            self.update_db(permissions=new_permissions)

    def clean_username(self, username):
        delimeters_to_remove = "".join(global_vars.DELIMETERS)
        username_stripped = re.sub(
            "[" + delimeters_to_remove + "]",
            "",
            username
        )
        # Remove trailing spaces.
        username_stripped = username_stripped.strip()

        return username

    def on_client_connection(self, client):
        self.clients_connected += 1

        if self.clients_connected == 1:
            global_vars.client_count += 1

    def on_client_disconnection(self, client):
        self.clients_connected -= 1

        if self.clients_connected == 0:
            global_vars.client_count -= 1


class Client:
    def __init__(self, session_obj, request_obj):
        self.ip = request_obj.remote_addr
        self.sid = request_obj.sid

        self.update_client_info(session_obj, request_obj)

        self.disconnecting = False

    def update_client_info(self, session_obj, request_obj):
        saved_info = get_user_by_session(session_obj, request_obj)
        if saved_info is not None:
            self.client_info = saved_info
            return

        if self.ip in global_vars.client_infos_by_ip.keys():
            for pos_client_info in global_vars.client_infos_by_ip[self.ip]:
                if pos_client_info.user_id == USER_ID_ANONYMOUS:
                    self.client_info = pos_client_info
                    return

        self.client_info = Client_Info(ip=self.ip)

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
