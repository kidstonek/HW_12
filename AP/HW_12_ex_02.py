"""
Есть список, каждый элемент которого — это словарь с контактами пользователя следующего вида:

{
    "name": "Allen Raymond",
    "email": "nulla.ante@vestibul.co.uk",
    "phone": "(992) 914-3792",
    "favorite": False,
}
Словарь содержит имя пользователя name, его email, телефонный номер phone и свойство favorite — избранный контакт
или нет.

Разработайте две функции для сериализации и десериализации списка контактов с помощью пакета json и
хранения полученных данных в текстовом файле.

Первая функция write_contacts_to_file принимает два параметра: filename — имя файла, contacts — список контактов.
Она сохраняет указанный список в файл, используя метод dump пакета json.

Структура json файла должна быть следующей:

{
  "contacts": [
    {
      "name": "Allen Raymond",
      "email": "nulla.ante@vestibul.co.uk",
      "phone": "(992) 914-3792",
      "favorite": false
    },
    ...
  ]
}
Т.е. список контактов должен храниться по ключу "contacts", а не просто сохранить его в файл.

Вторая функция read_contacts_from_file читает и возвращает указанный список contacts из файла filename,
сохраненного ранее функцией write_contacts_to_file, используя метод load пакета json.
"""


import json


def write_contacts_to_file(filename, contacts):
    with open(filename, "w") as f:
        bb = {'contacts': contacts}
        json.dump(bb, f)


def read_contacts_from_file(filename):
    with open(filename, "r") as f:
        unpack = json.load(f)
    return unpack['contacts']


def main():
    asd = {
        "name": "Allen Raymond",
        "email": "nulla.ante@vestibul.co.uk",
        "phone": "(992) 914-3792",
        "favorite": False,
    }

    filename = 'files/hw_12_02.json'
    write_contacts_to_file(filename, asd)
    print(read_contacts_from_file(filename))


if '__main__' == __name__:
    main()