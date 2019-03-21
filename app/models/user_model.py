user_list = []

class User:
    def __init__(self, **kwargs):
        self.user_id = len(user_list) + 1
        self.email_add = kwargs.get("email_add")
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.password = kwargs.get("password")

    def user_struct(self):
        return {
            "user_id": self.user_id,
            "email_add": self.email_add,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password
        }