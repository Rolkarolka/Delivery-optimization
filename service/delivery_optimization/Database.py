import json

class Database:
    def __init__(self, path):
        self.__users = self.__load_from_file(path + "/users.json")

    def __load_from_file(self, path):
        with open(path, mode='r') as file:
            text = file.read().replace("\n", "")
            return json.loads(text)

    def create_new_user(self, username):
        if username not in self.__users:
            group = self.__get_new_user_group()
            self.__users[username] = group
            return group
        else:
            raise ValueError("User with that username exists.")

    def __get_new_user_group(self):
        # TODO
        return "B"

    def get_user_group(self, username: str):
        return self.__users[username]

    def save_prediction(self, group, prediction):
        # TODO
        pass
