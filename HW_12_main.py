import os
import pathlib
import shelve
from collections import UserDict
from datetime import date, datetime
from os import path


def input_error(in_func):
    def wrapper(*args):
        try:
            check = in_func(*args)
            return check
        except KeyError:
            return 'There is no such a contact. Please try again'
        except IndexError:
            return 'Give me name and phone please'
        except ValueError:
            return 'ValueError'
        except TypeError:
            return 'TypeError'

    return wrapper


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value


class Phone(Field):
    def __init__(self, phone_list):
        self.__phone_list = None
        self.phone_list = phone_list

    @property
    def phone_list(self):
        return self.__phone_list

    @phone_list.setter
    def phone_list(self, phone_list):
        if phone_list.isdigit():
            self.__phone_list = phone_list

    def __repr__(self) -> str:
        return str(self.__phone_list)


class Name(Field):
    pass


class Birthday(Field):
    def __init__(self, b_date):
        self.__b_date = None
        self.b_date = b_date

    @property
    def b_date(self):
        return self.__b_date

    @b_date.setter
    def b_date(self, b_date):
        try:
            self.__b_date = datetime.strptime(b_date, '%Y-%m-%d').date()
        except ValueError as e:
            return "Birthdate must be in 'dd.mm.yy' format"

    def __repr__(self) -> str:
        return self.b_date.strftime('%Y-%m-%d')


# Record реализует методы для добавления/удаления/редактирования объектов Phone.


class Record:
    def __init__(self, name: Name, phone: Phone = None, b_date: Birthday = None):
        self.name = name
        self.phones = []  # коллекции называем во множественном числе
        if phone:
            self.phones.append(phone)
        self.b_date = b_date

    def add_number_to_record(self, phone: Phone):
        self.phones.append(phone)

    def del_number_from_record(self, phone: Phone):
        for i in self.phones:
            if i.phone_list == phone.phone_list:
                self.phones.remove(i)

    def change_number_in_record(self, phone: Phone, phone_new: Phone):
        for i in self.phones:
            if i.phone_list == phone.phone_list:
                self.phones[self.phones.index(i)] = phone_new

    def add_b_day(self, b_date: Birthday):
        self.b_date = b_date
        return f'Birthdate for {self.name.value} was set to {self.b_date}'

    def days_to_birthday(self):
        if self.b_date:
            b_d = self.b_date.b_date
            result = datetime(datetime.now().year, b_d.month, b_d.day) - datetime.now()
            if result.days > 0:
                return result.days
            return "The birthday is over"
        return "Birthdate not set"

    def __repr__(self):
        if self.b_date is None:
            return f'{self.name.value}, {self.phones}'
        else:
            return f'{self.name.value}, {self.phones}, {self.b_date}'


class AddressBook(UserDict):
    counter = 0

    def set_pages(self, page):
        self.counter = page

    def add_to_addressbook(self, record: Record):
        self.data[record.name.value] = record

    def iterator_addressbook(self, *args):
        self.counter = int(args[0])
        number_of_iterations = int(args[1])
        b = list(dict.keys(self.data))
        while int(self.counter) < number_of_iterations:
            yield self[b[self.counter]]
            self.counter += 1
            if self.counter == number_of_iterations:
                input("press Enter to continue...")
                number_of_iterations += int(args[1])
                if number_of_iterations > len(b):
                    number_of_iterations = len(b)


def ex(*args):
    save_phonebook(args[0])
    return "Good bye!"


@input_error
def add_to_addressbook(addressbook: AddressBook, *args):
    if args[0].isdigit():
        return "The contact name should be in letters"
    tmp_name = Name(args[0])
    tmp_phone1 = Phone(args[1])
    tmp_rec = Record(tmp_name, tmp_phone1)
    addressbook.add_to_addressbook(tmp_rec)
    save_phonebook(addressbook)
    return f'Contact {tmp_rec.name.value} with phones {tmp_phone1} added successfully'


def show_addressbook(addressbook: AddressBook, *args):
    if args[0] == '':
        for k, v in addressbook.data.items():
            print(f"Name for the contact {k}, phone\\s {v.phones}, birthday is {v.b_date}" if v.b_date else
                  f"Name for the contact {k}, phone\\s {v.phones}, birthday is not defined")
        return 'End of the PhoneBook'
    if args[0].isdigit():
        if int(args[0]) > len(addressbook.data.values()):
            print('Now you will get a whole book')
            for k, v in addressbook.data.items():
                print(f"Name for the contact {k}, phone\\s {v.phones}, birthday is {v.b_date}" if v.b_date else
                      f"Name for the contact {k}, phone\\s {v.phones}, birthday is not defined")
            return 'End of the PhoneBook'
        if int(args[0]) <= len(addressbook.data.values()):
            by_steps = addressbook.iterator_addressbook(addressbook.counter, args[0])
            for rec in by_steps:
                print(rec)
            addressbook.counter = 0
        return "End of the Addressbook"


@input_error
def find_contact(addressbook: AddressBook, *args):
    for k, v in addressbook.data.items():
        if k == args[0]:
            return k, v.phones


@input_error
def add_phone_to_contact(addressbook: AddressBook, *args):
    for k, v in addressbook.data.items():
        if k == args[0]:
            add_num = Phone(args[1])
            Record.add_number_to_record(v, add_num)
            return f'Number {add_num.phone_list} was added'


@input_error
def erase_phone(addressbook: AddressBook, *args):
    for k, v in addressbook.data.items():
        if k == args[0]:
            del_num = Phone(args[1])
            Record.del_number_from_record(v, del_num)
            return f'Number {del_num.phone_list} was deleted'


def change_phone(addressbook: AddressBook, *args):
    for k, v in addressbook.data.items():
        if k == args[0]:
            ch_num_in = Phone(args[1])
            ch_num_for = Phone(args[2])
            Record.change_number_in_record(v, ch_num_in, ch_num_for)
            return f'Number {ch_num_in.phone_list} was changed to {ch_num_for.phone_list}'


def check_contact_b_day(addressbook: AddressBook, *args):
    rec = addressbook.data.get(args[0])
    if rec:
        return rec.days_to_birthday()


def save_phonebook(addressbook: AddressBook):
    with shelve.open(db_file) as db:
        db['phone_book'] = addressbook
    print('changes to PhoneBook are saved')


def find_all_staff(addressbook: AddressBook, *args):
    contact_found = False
    print('--------------------')
    for k, v in addressbook.items():
        if args[0].lower() in k.lower():
            print(f'Contact found --> Name: {k}, phone\\s: {v.phones}')
            contact_found = True
        else:
            for phone in v.phones:
                if args[0].lower() in phone.phone_list:
                    print(f'Contact found --> Name: {k}, phone\\s: {v.phones}')
                    contact_found = True
    if not contact_found:
        return 'No contact found'
    return '--------------------'


def add_b_day(addressbook: AddressBook, *args):
    for k, v in addressbook.data.items():
        if k == args[0]:
            b_day_to_set = Birthday(args[1])
            return Record.add_b_day(v, b_day_to_set)


def show_db(addressbook, *args):
    with shelve.open(db_file) as states:
        for key in states.values():
            print(key)
    return 'There was your PhoneBook'


def helps(*args):
    print('You can use following commands:')
    print('"show", "s" - to show the whole PhoneBook')
    print('"s and number" - to show the whole PhoneBook by pages \\ example: s [number]')
    print('"add" - to add the contact to the Phone book \\ example: add ContactName Phone \\+ Phone....')
    print('"ap" - add phone for existing contact \\ example: ap NameOfExistingContact Phone \\+ Phone....')
    print('"change", "ch" - to update existing phone number for contact \\ example: change '
          'NameOfExistingContact Phone \\+ Phone....')
    print('"erase" - to erase existing phone for the contact \\ example: erase NameOfExistingContact '
          'Phone \\+ Phone....')
    print('"birthday", "bdate", "bd" - to check how many days till next birthday for the contact '
          '\\ example: ch NameOfExistingContact')
    print('"ff" - to find something in the phonebook \\ example: ff YourText')
    print('"exit", ".", "bye" - for exit')
    return 'make your choice'


COMMANDS = {ex: ["exit", ".", "bye"], show_addressbook: ["show", "s"], add_to_addressbook: ["add"],
            find_contact: ["find"], add_phone_to_contact: ["ap"], erase_phone: ["erase"],
            change_phone: ["change", "ch"], check_contact_b_day: ["birthday", "bdate", "bd"], helps: ["help", "h"],
            show_db: ["asd"], find_all_staff: ["ff"], add_b_day: ["abd"]}


@input_error
def parse_command(user_input: str):
    for k, v in COMMANDS.items():
        for i in v:
            if user_input.lower().startswith(i.lower()):
                return k, user_input[len(i):].strip().split(" ")


def db_checker():
    if os.path.exists(db_file + '.dat'):
        print('contact book exist\n')
        with shelve.open(db_file) as states:
            for key in states.values():
                phone_book = key
        return phone_book
    else:
        print('Blank PhoneBook was created')
        phone_book = AddressBook()
        return phone_book


def main():
    print('Welcome to the worst PhoneBook EVER')
    print('type "help" or "h" to receive a help')
    phone_book = db_checker()
    print(phone_book)
    while True:
        tmp = input('Please input command: ')
        result, data = parse_command(tmp)
        print(result(phone_book, *data))
        if result is ex:
            break


if '__main__' == __name__:
    db_file = os.getcwd() + "\\db\\db"
    main()
