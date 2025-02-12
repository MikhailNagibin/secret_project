from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, firstname, surname, email, password, role_id):
        self.id = id
        self.firstname = firstname
        self.surname = surname
        self.email = email
        self.password = password
        self.role = role_id
        self.for_db = (firstname, surname, email, self.password, role_id)

    def __repr__(self):
        return " ".join([str(el) for el in self.for_db])