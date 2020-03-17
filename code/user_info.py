import random

from flask_login import UserMixin

from defines import (
    SERVER_PERMISSION_NONE,
    SERVER_PERMISSION_BASIC,
    USER_ID_ANONYMOUS
)
from database import user_db
from security import gen_new_super_secret, int2uni


class User_Info(UserMixin):
    """
    User_Info class is inherently belonging
    to "registered" users, it is used to quickly
    work with DB in scope of the project.
    """

    def __init__(
        self,
        user_id=None,
        name="",
        email="",
        profile_pic="",
        discord_id="",
        google_id="",
        permissions=SERVER_PERMISSION_BASIC,
    ):
        self.user_id = user_id
        self._name = name
        self._email = email
        self._profile_pic = profile_pic
        self._discord_id = discord_id
        self._google_id = google_id
        self._permissions = permissions

    def insert(self):
        """
        This method is used to insert self
        into DB.
        """
        temp_cursor = user_db.cursor()

        super_secret_obj = gen_new_super_secret()

        temp_cursor.execute(
            """
            INSERT INTO
            users
            (super_secret,
            secret_salt,
            name,
            email,
            pfp,
            google_id,
            permissions)
            VALUES (?,?,?,?,?,?,?)
            """,
            (
                super_secret_obj["super_secret"],
                super_secret_obj["salt"],
                self.name,
                self.email,
                self.profile_pic,
                self.google_id,
                self.permissions,
            ),
        )

        user_db.commit()

        self.user_id = temp_cursor.lastrowid

        return {
            "user_id": temp_cursor.lastrowid,
            "key": super_secret_obj["key"],
        }

    @staticmethod
    def init_from_db(db_repr):
        """
        Initiates self from full db_repr.

        !!! NB !!!
        Is only compatible if db_repr was selected via SELECT *.
        """
        if type(db_repr) is not tuple:
            raise TypeError(
                "Expected tuple as db_repr, received: " + str(type(db_repr))
            )

        return User_Info(
            user_id=db_repr[0],
            email=db_repr[3],
            profile_pic=db_repr[4],
            google_id=db_repr[5],
            permissions=db_repr[6],
        )

    @staticmethod
    def get(
        user_id=None, discord_id=None, google_id=None, email=None,
    ):
        """
        Returns any User_Info instance
        matching given unique identificators.
        Returns None if none is found.
        """
        temp_cursor = user_db.cursor()

        pos_selectors = {
            "user_id": user_id,
            "discord_id": discord_id,
            "google_id": google_id,
            "email": email,
        }

        user = None
        for selector in pos_selectors.keys():
            sel_value = pos_selectors[selector]
            if sel_value is None:
                continue
            user = temp_cursor.execute(
                "SELECT * FROM users WHERE " + selector + " = ?", (sel_value,)
            ).fetchone()

            if user is not None:
                return User_Info.init_from_db(user)

        return None

    """

    DEPRECATED, AS TO USE Flask-Login.
    If that option becomes unfeasible, look here.

    @staticmethod
    def get_auth(user_id, key):
        # This method returns user by id only if
        # their super_secret is the same as super_secret
        # given as argument.

        temp_cursor = user_db.cursor()

        user = temp_cursor.execute(
            "SELECT * FROM users WHERE user_id=? AND super_secret=?",
            (user_id, super_secret),
        ).fetchone()

        if user is None:
            return None

        salt = user[2]
        hashed_super_secret = gen_super_secret(key, salt)

        if hashed_super_secret == user[1]
            return User_Info.init_from_db(user)

        return None

    @staticmethod
    def get_by_session(session_obj, request_obj):
        # Returns User_Info of an authenticated user, if
        # session_obj is who they pretend to be.

        # Returns None otherwise.
        user_id = session_obj.get("user_id")
        key = session_obj.get("key")

        if all([user_id, key]):
            return User_Info.get_auth(user_id, key)
        return None
    """

    def new_super_secret(self):
        """
        This method is used to regenerate a new
        super secret for user represented by self.
        """
        super_secret_obj = gen_new_super_secret()

        temp_cursor = user_db.cursor()

        temp_cursor.execute(
            """
            UPDATE users
            SET super_secret=?,
            secret_salt=?
            WHERE user_id=?
            """,
            (
                super_secret_obj["super_secret"],
                super_secret_obj["salt"],
                self.user_id,
            ),
        )
        user_db.commit()

        return {
            "key": super_secret_obj["key"],
            "salt": super_secret_obj["salt"]
        }

    def update_field(
        self, field, value,
    ):
        """
        This method is used to update any
        related fields to self in DB.
        """
        temp_cursor = user_db.cursor()

        sql = "UPDATE users"
        sql += " SET " + field + "=" + str(value)

        sql += " WHERE user_id=" + str(self.user_id)

        temp_cursor.execute(sql)
        user_db.commit()

    # If user somewhere has this class in place,
    # they are by default - authenticated.
    def is_authenticated(self):
        return True

    # TO-DO: consider doing something with this.
    def is_active(self):
        return True

    def is_anonymous(self):
        return not self.is_authenticated()

    def get_id(self):
        return int2uni(self.user_id)

    # Getters-setters, please, do not set/get any of these variables
    # directly, use appropriate getter-setter.
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if new_name != self._name:
            self._name = new_name
            self.update_field("name", new_name)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email):
        if new_email != self._emaill:
            self._email = new_email
            self.update_field("email", new_email)

    @property
    def profile_pic(self):
        return self._profile_pic

    @profile_pic.setter
    def profile_pic(self, new_pfp):
        if new_pfp != self._profile_pic:
            self._profile_pic = new_pfp
            self.update_field("pfp", new_pfp)

    """
    PLACEHOLDER

    @property
    def discord_id(self):
        return self._discord_id

    @discord_id.setter
    def discord_id(self, new_discord_id):
        if new_discord_id != self._discord_id:
            self._discord_id = new_discord_id
            self.update_field("discord_id", new_discord_id)
    """

    @property
    def google_id(self):
        return self._google_id

    @google_id.setter
    def google_id(self, new_google_id):
        if new_google_id != self._google_id:
            self._google_id = new_google_id
            self.update_field("google_id", new_google_id)

    @property
    def permissions(self):
        return self._permissions

    @permissions.setter
    def permissions(self, new_permissions):
        if new_permissions != self._permissions:
            self._permissions = new_permissions
            self.update_field("permissions", new_permissions)


class Guest_Info(User_Info):
    """
    Guest_Info is a class that defines any user,
    which are not registered in our database.
    """

    def __init__(
        self,
        user_id=None,
        name="",
        email="",
        profile_pic="",
        discord_id="",
        google_id="",
        permissions=SERVER_PERMISSION_BASIC,
    ):
        self._name = "Guest-" + str(random.randint(0, 1000))
        self.user_id = USER_ID_ANONYMOUS

    def insert(self):
        pass

    def new_super_secret(self):
        pass

    def update_field(
        self, field, value,
    ):
        pass

    def is_authenticated(self):
        return False

    def is_active(self):
        return False

    # Getters-setters, please, do not set/get any of these variables
    # directly, use appropriate getter-setter.
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        pass

    @property
    def email(self):
        return "guest@guest.guest"

    @email.setter
    def email(self, new_email):
        pass

    @property
    def profile_pic(self):
        return "/static/resources/guest.png"

    @profile_pic.setter
    def profile_pic(self, new_pfp):
        pass

    """
    PLACEHOLDER

    @property
    def discord_id(self):
        return ""

    @discord_id.setter
    def discord_id(self, new_discord_id):
        pass
    """

    @property
    def google_id(self):
        return ""

    @google_id.setter
    def google_id(self, new_google_id):
        pass

    @property
    def permissions(self):
        return SERVER_PERMISSION_NONE

    @permissions.setter
    def permissions(self, new_permissions):
        if new_permissions != self._permissions:
            self._permissions = new_permissions
