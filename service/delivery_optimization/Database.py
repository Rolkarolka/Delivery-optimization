import csv

class Database:
    def __init__(self, path="service/database/"):
        self.path = path
        self.__users = {}
        self.__load_from_file("users.csv")

    def get_path(self, filename):
        return self.path + filename

    def __load_from_file(self, filename):
        with open(self.get_path(filename), mode='r', encoding='UTF-8') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                self.__users[row[0]] = row[1]

    def __save_to_file(self, filename, key, value):
        with open(self.get_path(filename), mode='a', newline='', encoding='UTF-8') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([key, value])

    def create_new_user(self, username):
        if username not in self.__users:
            group = self.__get_new_user_group(username)
            self.__save_to_file("users.csv", username, group)
            self.__users[username] = group
            return group
        else:
            raise ValueError("User with that username exists.")

    def __get_new_user_group(self, username):
        # TODO rozklad normalny?
        h = sum([ord(char) for char in username])
        if h % 2:
            return "A"
        else:
            return "B"

    def get_user_group(self, username: str):
        if username in self.__users:
            return self.__users[username]
        return self.create_new_user(username)

    def save_prediction(self, group, predictions, week_number):
        with open(self.get_path("predictions.csv"), mode='a', newline='', encoding='UTF-8') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for product_id, prediction in predictions.items():
                writer.writerow([group, week_number, product_id, prediction])
