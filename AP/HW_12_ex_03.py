import csv


def write_contacts_to_file(filename, contacts):
    with open(filename, "w", newline='') as f:
        # field_names = ["name", "email", "phone", "favorite"]
        field_names = contacts[0].keys()
        print(type(field_names))
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for row in contacts:
            writer.writerow(row)


def read_contacts_from_file(filename):
    result = []
    with open(filename, "r") as f:
        gen = csv.DictReader(f)
    for row in gen:
        if row['favorite'] == 'True':
            row['favorite'] = True
        if row['favorite'] == 'False':
            row['favorite'] = False
        result.append(row)
        print(row)
    return result


def main():
    users = {
        "name": "Allen Raymond",
        "email": "nulla.ante@vestibul.co.uk",
        "phone": "(992) 914-3792",
        "favorite": False,
    }
    asd = {
        "name": "Allen Raymond",
        "email": "nulla.ante@vestibul.co.uk",
        "phone": "(992) 914-3792",
        "favorite": False,
    }

    filename = 'files/hw_12_03.csv'
    write_contacts_to_file(filename, asd)
    print(read_contacts_from_file(filename))


if '__main__' == __name__:
    main()
