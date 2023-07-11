from datetime import datetime, timedelta
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
                "Недійсний номер телефону. Номер телефону має бути цифровим.")


class Email(Field):
    @Field.value.setter
    def value(self, new_value):
        if "@" not in new_value:
            raise ValueError("Невірна адреса електронної пошти.")


class Address(Field):
    pass


class Birthday(Field):
    @Field.value.setter
    def value(self, new_value):
        try:
            datetime.strptime(new_value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                "Неправильний формат дня народження. Дата народження має бути у форматі YYYY-MM-DD.")
        self._value = new_value


class Record:
    def __init__(self, name, address=None, birthday=None, email=None):
        self.name = Name(name)
        self.address = Address(address)
        self.birthday = Birthday(birthday)
        self.email = Email(email)
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
        if self.birthday:
            dt_birthday = datetime.strptime(self.birthday.value, "%Y-%m-%d")
            dt_birthday_in_this_year = datetime(
                year=datetime.now().year, month=dt_birthday.month, day=dt_birthday.day)
            if dt_birthday_in_this_year.month < datetime.now().month:
                dt_birthday_in_this_year += timedelta(weeks=52)
                days_before_birthday = dt_birthday_in_this_year - datetime.now()
                return f"{days_before_birthday.days} днів до дня народження!"
            elif dt_birthday_in_this_year.month == datetime.now().month and dt_birthday_in_this_year.day == datetime.now().day:
                return f"День народження сьогодні! З Днем Народження!!!!"
            elif dt_birthday_in_this_year.month == datetime.now().month and dt_birthday_in_this_year.day < datetime.now().day:
                dt_birthday_in_this_year += timedelta(weeks=52)
                days_before_birthday = dt_birthday_in_this_year - datetime.now()
                return f"{days_before_birthday.days} днів до дня народження!"
            else:
                days_before_birthday = dt_birthday_in_this_year - datetime.now()
                return f"{days_before_birthday.days} днів до дня народження!"

    def __str__(self):
        result = f"Ім'я: {self.name}\n"
        if self.address.value:
            result += f"Адреса: {self.address}\n"
        if self.birthday.value:
            result += f"День народження: {self.birthday}\n"
        if self.email.value:
            result += f"Електронна адреса: {self.email}\n"
        if self.phones:
            result += "Номери телефону:\n"
            for phone in self.phones:
                result += f"- {phone}\n"
        return result


class CustomerBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        if record.name.value in self.data:
            existing_record = self.data[record.name.value]
            existing_record.phones.extend(record.phones)
        else:
            self.data[record.name.value] = record
        self.save_to_file('customer_book.pkl')

    def delete_record(self, name):
        del self.data[name]
        self.save_to_file('customer_book.pkl')

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

    def search_by_address(self, address):
        result = []
        for record in self.data.values():
            if address.lower() in record.address.value.lower():
                result.append(record)
        return result

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        if os.path.isfile(filename):
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        else:
            print(f"Файл '{filename}' не існує.")

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


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return str(e)

    return wrapper


customer_book = CustomerBook()


@input_error
def add_contact(name, phone, birthday=None, address=None, email=None):
    record = Record(name, address, birthday, email)
    correct_phone = phone.replace(
        "-", "").replace(" ", "").replace("(", "").replace(")", "")
    if len(correct_phone) == 10 and correct_phone.startswith("0") and (all(not char. isalpha() for char in correct_phone)):
        new_correct_phone = f"+38{correct_phone}"
        record.add_phone(new_correct_phone)
    elif len(correct_phone) == 11 and correct_phone.startswith("80") and (all(not char. isalpha() for char in correct_phone)):
        new_correct_phone = f"+3{correct_phone}"
        record.add_phone(new_correct_phone)
    elif len(correct_phone) == 12 and correct_phone.startswith("380") and (all(not char. isalpha() for char in correct_phone)):
        new_correct_phone = f"+{correct_phone}"
        record.add_phone(new_correct_phone)
    elif len(correct_phone) == 13 and correct_phone.startswith("+380") and (all(not char. isalpha() for char in correct_phone[1:])):
        new_correct_phone = correct_phone[::]
        record.add_phone(correct_phone)
    else:
        return "Ви ввели неправильний номер! Номер повинен містити всі цифри та не менше 10 символів!"
    if birthday:
        try:
            record.birthday.value = birthday
        except ValueError as e:
            return str(e)
    customer_book.add_record(record)
    return f"Додано контакт '{name}' з номером телефону '{new_correct_phone}', днем народження '{birthday}', адресою '{address}', і  електронною адресою '{email}'!."


@input_error
def change_phone(name, old_phone, new_phone):
    correct__old_phone = old_phone.replace("-", "").replace(" ", "")
    correct_new_phone = new_phone.replace("-", "").replace(" ", "")
    if name not in customer_book.data:
        return f"!!! Контакт'{name}' не існує !!!"
    if len(correct_new_phone) == 13 and correct_new_phone.startswith("+380") and (all(not char. isalpha() for char in correct_new_phone[1:])):
        record = customer_book.data[name]
        record.edit_phone(correct__old_phone, correct_new_phone)
        return f"Номер телефону для контакту '{name}' змінено на '{correct_new_phone}'."
    else:
        return "Ви ввели неправильний номер! Номер повинен містити всі цифри і мати не менше 10 символів!"


@input_error
def remove_contact(name):
    if name not in customer_book.data:
        return f"!!! Контакт '{name}' не існує !!!"
    customer_book.delete_record(name)
    return f"Контакт '{name}' видалено."


@input_error
def get_phone(name):
    if name not in customer_book.data:
        return f"Контакт '{name}' не існує."
    record = customer_book.data[name]
    phones = ", ".join([str(phone) for phone in record.phones])
    return f"Номер(и) телефону для контакту '{name}': {phones}"


@input_error
def get_days_to_birthday(name):
    if name not in customer_book.data:
        return f"Контакт '{name}' не існує."
    record = customer_book.data[name]
    days_left = record.days_to_birthday()
    if days_left:
        return f"Кількість днів до наступного дня народження {name}: {days_left}"
    else:
        return f"У {name} сьогодні день народження! З Днем Народження!"


def next_birthday(days):
    result = []
    if days >= 1:
        for k, v in customer_book.data.items():
            _ = datetime.strptime(
                customer_book.data[k].birthday.value, "%Y-%m-%d")
            dt = datetime(year=datetime.now().year, month=_.month, day=_.day)
            td = datetime.now() + timedelta(days=days)
            if _.month < datetime.now().month:
                dt += timedelta(weeks=52)
                if (dt - datetime.now()).days <= days:
                    result.append(
                        f"{k}:{customer_book.data[k].birthday.value}, {k}'s день народження через {(dt - datetime.now()).days} днів!")
            elif _.month == datetime.now().month and _.day < datetime.now().day:
                dt += timedelta(weeks=52)
                if (dt - datetime.now()).days <= days:
                    result.append(
                        f"{k}:{customer_book.data[k].birthday.value}, {k}'s день народження через {(dt - datetime.now()).days} днів!")
            elif _.month == datetime.now().month and _.day == datetime.now().day:
                result.append(
                    f"{k}:{customer_book.data[k].birthday.value}, {k}'s день народження сьогодні!")
            else:
                if (dt - datetime.now()).days <= days:
                    result.append(
                        f"{k}:{customer_book.data[k].birthday.value}, {k}'s день народження через {(dt - datetime.now()).days} днів!")
        return result
    else:
        return "Кількість днів має бути більша за 0!"


def show_all_contacts():
    if not customer_book.data:
        return "Список контактів порожній!"
    result = "Контакти:\n"
    for record in customer_book.data.values():
        result += str(record) + "\n"
    return result


command_text = 'Hello, Add, Change, Remove, Phone, Next birthday, Birthday list, Search, Show all, Close or Exit or Good bye'


def main_customer_book():
    customer_book.load_from_file('customer_book.pkl')
    print(f"Доступні команди: {command_text}")
    while True:
        command = input("Введіть команду  > ").lower()
        if command == "hello":
            print(f"Чим я можу допомогти?")
        elif command == "add":
            while True:
                try:
                    name = str(input("Введіть ім'я > "))
                    if name == ("close" or "exit" or "good bye"):
                        break
                    phone = input("Введіть номер телефону > ")
                    if phone == ("close" or "exit" or "good bye"):
                        break
                    birthday = input(
                        "Введіть день народження у форматі YYYY-MM-DD (необов'язково) > ")
                    if birthday == ("close" or "exit" or "good bye"):
                        break
                    address = input("Введіть адресу (необов'язково) > ")
                    if address == ("close" or "exit" or "good bye"):
                        break
                    email = input(
                        "Введіть електронну пошту (необов'язково) > ")
                    if email == ("close" or "exit" or "good bye"):
                        break
                    res = add_contact(name, phone, birthday, address, email)
                    if res.startswith("Додано"):
                        print(res)
                        break
                    print(res)

                except ValueError:
                    print("Непрвильні дані.")
        elif command == "change":
            while True:
                try:
                    name, old_phone = input(
                        "Введіть ім'я та старий номер телефону > ").lower().split()
                    new_phone = input("Введіть новий номер телефону > ")
                    if (name or old_phone or new_phone) == ("close" or "exit" or "good bye"):
                        break
                    res = change_phone(name, old_phone, new_phone)
                    if not res.startswith("Номер"):
                        print(res)
                    else:
                        print(res)
                        break
                except ValueError:
                    print("Неправильні дані.")
        elif command == "remove":
            while True:
                name = input("Введіть ім'я > ")
                if name == ("close" or "exit" or "good bye"):
                    break
                res = remove_contact(name)
                if not res.endswith("видалено."):
                    print(res)
                else:
                    print(res)
                    break
        elif command == "phone":
            while True:
                name = input("Введіть ім'я > ")
                if name == ("close" or "exit" or "good bye"):
                    break
                res = get_phone(name)
                if not res.startswith("Номер"):
                    print(res)
                else:
                    print(res)
                    break
        elif command == "next birthday":
            while True:
                name = input("Введіть ім'я > ")
                if name == ("close" or "exit" or "good bye"):
                    break
                print(get_days_to_birthday(name))
        elif command == "birthday list":
            num = input("Введіть кількість днів: ")
            try:
                days = int(num)
                print(next_birthday(days))
            except ValueError:
                print("Кількість днів має бути цілим числом!")
        elif command == "search":
            inp = input(
                "Введіть ім'я,номер телефону або адресу > ")
            contacts = []
            if inp.isdigit():
                contacts = customer_book.search_by_phone(inp)
            else:
                contacts = customer_book.search_by_name(
                    inp) + customer_book.search_by_address(inp)
            if contacts:
                result = "Результат:\n"
                for record in contacts:
                    result += str(record) + "\n"
                print(result)
            else:
                print("Контакти не знайдено")
        elif command == "show all":
            print(show_all_contacts())
        elif command == "good bye" or command == "close" or command == "exit":
            print("До зустрічі!")
            break
        else:
            print(f"Невідома команда. Доступні команди: {command_text}")
    customer_book.save_to_file('customer_book.pkl')


if __name__ == "__main__":
    main_customer_book()
