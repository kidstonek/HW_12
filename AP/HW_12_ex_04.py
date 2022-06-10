"""
Разработайте класс Person. Он имеет четыре свойства: имя пользователя name, его email, телефонный номер phone и
свойство favorite — избранный контакт или нет.

Пример создания экземпляра класса:

    Person(
        "Allen Raymond",
        "nulla.ante@vestibul.co.uk",
        "(992) 914-3792",
        False,
    )
Разработайте класс Contacts. Он должен инициализировать через конструктор два свойства: filename —
имя файла для упаковки объекта класса Contacts, contacts — список контактов, экземпляров класса Person.

Пример создания экземпляра класса:

contacts = [
    Person(
        "Allen Raymond",
        "nulla.ante@vestibul.co.uk",
        "(992) 914-3792",
        False,
    ),
    Person(
        "Chaim Lewis",
        "dui.in@egetlacus.ca",
        "(294) 840-6685",
        False,
    ),
]

persons = Contacts("hw_12_04.dat", contacts)
Разработайте два метода для сериализации и десериализации экземпляра класса Contacts с помощью пакета pickle и
хранения полученных данных в бинарном файле.

Первый метод save_to_file сохраняет экземпляр класса Contacts в файл, используя метод dump пакета pickle.
Имя файла хранится в атрибуте filename.

Второй метод read_from_file читает и возвращает экземпляр класса Contacts из файла filename, используя метод
load пакета pickle.

Пример работы:

persons = Contacts("hw_12_04.dat", contacts)
persons.save_to_file()
person_from_file = persons.read_from_file()
print(persons == person_from_file)  # False
print(persons.contacts[0] == person_from_file.contacts[0])  # False
print(persons.contacts[0].name == person_from_file.contacts[0].name)  # True
print(persons.contacts[0].email == person_from_file.contacts[0].email)  # True
print(persons.contacts[0].phone == person_from_file.contacts[0].phone)  # True
"""
import pickle


class Person:
    def __init__(self, name: str, email: str, phone: str, favorite: bool):
        self.name = name
        self.email = email
        self.phone = phone
        self.favorite = favorite


class Contacts:
    def __init__(self, filename: str, contacts: list[Person] = None):
        self.filename = filename
        if contacts is None:
            contacts = []
        self.contacts = contacts

    def save_to_file(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self, f)

    def read_from_file(self):
        with open(self.filename, "rb") as f:
            our_class = pickle.load(f)
        return our_class


def main():
    contacts = [
        Person(
            "Allen Raymond",
            "nulla.ante@vestibul.co.uk",
            "(992) 914-3792",
            False,
        ),
        Person(
            "Chaim Lewis",
            "dui.in@egetlacus.ca",
            "(294) 840-6685",
            False,
        ),
    ]

    persons = Contacts("files/hw_12_04.dat", contacts)
    persons.save_to_file()
    person_from_file = persons.read_from_file()
    print(persons == person_from_file)  # False
    print(persons.contacts[0] == person_from_file.contacts[0])  # False
    print(persons.contacts[0].name == person_from_file.contacts[0].name)  # True
    print(persons.contacts[0].email == person_from_file.contacts[0].email)  # True
    print(persons.contacts[0].phone == person_from_file.contacts[0].phone)  # True


if '__main__' == __name__:
    main()