from address_book import main
import pickle
import os


class Field:
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self._value)


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, new_value):
        if not str(new_value).isdigit():
            raise ValueError(
                "Invalid phone number. Phone number must be numeric.")


class Birthday(Field):
    @Field.value.setter
    def value(self, new_value):
        try:
            datetime.strptime(new_value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                "Invalid birthday format. Birthday must be in the format YYYY-MM-DD.")
        self._value = new_value


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if old_phone in str(phone.value):
                self.phones[i] = Phone(new_phone)

    def days_to_birthday(self):
        if self.birthday.value:
            today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            next_birthday = datetime.strptime(
                self.birthday.value, "%Y-%m-%d").replace(year=today.year)
            if today > next_birthday:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_left = (next_birthday - today).days
            return days_left

    def __str__(self):
        result = f"Name: {self.name}\n"
        if self.birthday.value:
            result += f"Birthday: {self.birthday}\n"
        if self.phones:
            result += "Phones:\n"
            for phone in self.phones:
                result += f"- {phone}\n"
        return result


class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        if record.name.value in self.data:
            existing_record = self.data[record.name.value]
            existing_record.phones.extend(record.phones)
        else:
            self.data[record.name.value] = record
        self.save_to_file('address_book.pkl')

    def delete_record(self, name):
        del self.data[name]
        self.save_to_file('address_book.pkl')

    def search_by_name(self, name):
        result = []
        for record in self.data.values():
            if name.lower() in record.name.value.lower():
                result.append(record)
        return result

    def search_by_phone(self, phone):
        result = []
        for record in self.data.values():
            for p in record.phones:
                if phone in str(p):
                    result.append(record)
                    break
        return result

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        if os.path.isfile(filename):
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        else:
            print(f"File '{filename}' does not exist.")

    def __iter__(self):
        self.index = 0
        self._records = list(self.data.values())
        return self

    def __next__(self):
        if self.index >= len(self._records):
            raise StopIteration
        record = self._records[self.index]
        self.index += 1
        return str(record)


main()
