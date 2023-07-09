from collections import UserDict
from datetime import datetime
import json
import os
import random

def magic_8_ball():
    responses = [
        "Безперечно!",
        "Так точно!",
        "Вельми ймовірно",
        "Можливо",
        "Не можу вам сказати зараз",
        "Спробуйте ще раз пізніше",
        "Краще не розраховувати на це",
        "Відповідь невизначена",
        "Це малоймовірно",
        "Ні, це неможливо",
        "Духи говорять так!",
        "Є сумніви",
        "Думаю що ні",
        "Шанси хороші",
        "Духи говорять ні",
        "Без сумнівів",
        "Шансів мало",
        "Звичайно, якщо хочеш стати пінгвіном.",
        "Тільки якщо готовий танцювати під дощем.",
        "Звичайно, але пам'ятай, що це не змінить твій настрій.",
        "Запитай пізніше. Зараз я зайнята готуванням чарівного пирога.",
        "Ймовірно так! Я бачила це в своєму кришталевому шарі. :-)",
        "Ніколи не кажи ніколи. Хіба, що магічна куля принесе тобі піцу.",
        "Чи не краще тобі поговорити з моїм колегою, Магічнимм Барменом? Він спеціаліст з усіх важливих справ.",
        "Спитай у кішки. Вона знає багато секретів всесвіту.",
        "Завжди пам'ятайте: краще питати дурні питання, ніж дурно відповідати на питання. Я готова відповісти на будь-яке!",
        "Відповідь закодована в потоці нейронних синапсів... Але нажаль, у мене не залучення до інтернету.",
        "Впевнена на 99,9%... але є ще цей 0,1%, коли всі правила перестають діяти.",
        "Знаєте, іноді питання без відповідей - найцікавіші. Так, ваше питання може стати наступним кандидатом на цю нагороду!",
        "Це випадково, але відповідь - так!",
        "На жаль, магічна куля відпочиває на Гавайських островах, але я можу залишити тобі свої 27 смішних порад!",
        "Ох, це складне питання. Магічна куля вирішила пожартувати - питай знову!",
        "Не можу відповісти прямо зараз, я ще переглядаю ""Курс магічних відповідей для чайників"".",
        "Погодься на піцу і пиво, і відповідь буде - так!",
        "Запитання надто складне для магічної кулі, спробуй з кришталевим шаром.",
        "Магічна куля бачить велике щастя у твоєму майбутньому - але не знає, чи це через відповідь на це питання.",
        "Питання настільки хороше, що магічна куля вирішила сміятись і не відповідати.",
        "Ні, але якщо принесеш мені каву, то можливо згодом зміню думку.",
        "Зірки кажуть - можливо!",
        "Зроби паузу, випий чашку гарячого шоколаду і подивись комедійний серіал - це теж розвага!",
        "Магічна куля каже, що можливість бути в гарному настрої - це найкращий депозит, який можеш мати!"
    ]
    random.shuffle(responses)
    return random.choice(responses)

class CustomException(Exception):
    pass

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Give me name and phone please or "
        except IndexError:
            return "Enter contact name"
        except CustomException as e:
            return str(e)
    return wrapper

def hello_command(params):
    return "How can I help you?"

def iter_record(params):
    for addres in address_book:
        print(addres)
        print('------------------------------')
    
def find_command(params):
    if not params:
        return "Enter a word to search"
    return "\n".join(f" {result}" for result in address_book.search_by_content(params))        

def note_find(params=''):

    note_book.load_from_file()

    wordfind = ""
    if not params:
        wordfind = input("Введіть слово для пошуку (щоб шукати по тегам додайте # перед словом): ")
    else:
        wordfind = params
    if not wordfind:
        return "Слово для пошуку не введене!"
    
    if wordfind.startswith('#'):
        wordfind = wordfind[1:]
        return "\n".join(f" {result}" for result in note_book.search_by_tag(wordfind))        
    else:
        return "\n".join(f" {result}" for result in note_book.search_by_content(wordfind))        

@input_error
def note_add(params=''):
    #list_param = params.split(' ')
    #if len(list_param) < 3:
    #        raise CustomException("Після команди через пробіл потрібно ввести назву замітки, теги та текст замітки")

    #name = list_param[0]
    #tags = list_param[1:len(list_param)-1]
    #text_note = list_param[len(list_param)-1]

    note_book.load_from_file()

    name = input("Введіть назву нотатки: ")
    tags_text = input("Введіть теги через пробіл: ")
    tags = tags_text.split(' ')
    text_note = input("Введіть текст нотатки: ")
    
    record = note_book.search_record(name)
    for tag in tags:
        record.add_tag(tag)
    if text_note:
        record.add_note(text_note)

    note_book.save_to_file(os.path.join(os.getcwd(), "note_book.json"))
    
    return f"Нотатка '{name}' успішно додана!"

def note_remove():
    name = input("Введіть назву нотатки яку потрібно видалити: ")
    if name == '':
        print('Нічого не введено, видалення відхилено.')
    else:    
        #record = note_book.search_by_name(name)
        #note_delet = str(record)
        note_book.load_from_file()
        note_book.remove_record(name)
        note_book.save_to_file(os.path.join(os.getcwd(), "note_book.json"))
        print(f"Нотатка '{name}' видалена!")

def note_edite():    
    name = input("Введіть назву нотатки яку потрібно відредагувати: ")
    if name == '':
        print('Нічого не введено, редагування відхилено.')
    else:
        note_book.load_from_file()
        note_book.edite_record(name)
        note_book.save_to_file(os.path.join(os.getcwd(), "note_book.json"))
        print(f"Нотатка '{name}' відредагована!")    
    
def note_show_all(params=''):
    note_book.load_from_file()
    return note_book.show_all_records()

@input_error
def add_command(params):
    list_param = params.split(' ')
    name = list_param[0]
    phone = list_param[1]
    birthday = None
    if len(list_param) == 3:
        birthday = list_param[2]
    record = address_book.search_record(name)
    record.add_phone(phone)
    if birthday:
        record.add_birthday(birthday)
    return f"Contact {name} added"

@input_error
def change_command(params):
    name, phone, new_phone = params.split(' ')
    record = address_book.search_record(name)
    record.edit_phone(phone, new_phone)
    return f"Phone number for {name} changed"

@input_error
def phone_command(params):
    name = params.strip()
    return address_book.search_records(name)

@input_error
def birthday_command(params):
    name = params.strip()
    return address_book.search_records(name)
    
def show_all_command(params):
    return address_book.show_all_records()

class NoteBook(UserDict):
    def __init__(self):
        super().__init__()
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, name):
        del self.data[name]

    def edite_record(self, text_name):
        record = ''
        for find_record in self.data.values():
            if text_name.lower() in find_record.name.value.lower():
                record = find_record
                break
        if not record:
            print(f"Немає нотатки з назвою '{text_name}'.")
            return

        print('1 - Змінити назву\n2 - Видалити чи змінити тег\n3 - Замінити текст нотатки\n4 - Додати текст до нотатки')
        commandNote = input('Оберіть команду: ')
        if commandNote == '1':
            NewName = input('Введіть нову назву нотатки: ')
            record.add_name(NewName)
        elif commandNote == '2':
            text_mesage = 'Теги:'
            for tag in record.tags:
                text_mesage += ' ' + tag.value
            print(text_mesage)
            FindTag = input('Введіть назву тега який потрібно видалити чи змінити: ')
            NewTag = input('Введіть нову назву тега щоб змінити або нічого щоб видалити: ')
            if NewTag == '':
                record.remove_tag(FindTag)
            else:
                record.edit_tag(FindTag, NewTag)
        elif commandNote == '3':
            add_text_note = input('Введіть новий текст нотатки: ')
            record.add_note(add_text_note)
        elif commandNote == '4':
            add_text_note = input('Введіть текст який потрібно додати до тексту нотатки: ')
            record.add_text_note(add_text_note)

    def search_record(self, search_criteria):
        for record in self.data.values():
            if search_criteria.lower() in record.name.value.lower():
                return record
        record = RecordNote(search_criteria)
        self.add_record(record)
        return record

    def search_records(self, search_criteria):
        results = []
        for record in self.data.values():
            if search_criteria.lower() in record.name.value.lower():
                results.append(record)
        return results
    
    def show_all_records(self):
        results = ''
        for record in self.data.values():
            results += "\n"+f"{record.name.value}:"+"".join(f" {tag.value}" for tag in record.tags)
            if record.text_note:
                results += ' Текст нотатки: '+ str(record.text_note.value)
        if not results:
            results = "Список нотаток пустий"
        return results

    def __iter__(self):
        self._iter_index = 0
        self._iter_chunk_size = 5
        return self

    def __next__(self):
        if self._iter_index >= len(self.data):
            raise StopIteration

        chunk = list(self.data.values())[self._iter_index:self._iter_index + self._iter_chunk_size]
        self._iter_index += self._iter_chunk_size

        return "\n".join(str(record) for record in chunk)
    
    def save_to_file(self, file_path):
        data = {
            'records': [record.to_dict() for record in self.data.values()]
        }
        with open(file_path, 'w') as file:
            json.dump(data, file, default=str)

    def load_from_file(self):
        file_path = os.path.join(os.getcwd(), "note_book.json")
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
            for record_data in data['records']:
                record = RecordNote.from_dict(record_data)
                self.add_record(record)
    
    def search_by_content(self, search_string):
        results = []
        for record in self.data.values():
            if search_string.lower() in record.name.value.lower():
                results.append(str(record))
            else:
                for tag in record.tags:
                    if search_string.lower() in tag.value.lower():
                        results.append(str(record))
                        break
        return results

    def search_by_tag(self, search_string):
        results = []
        for record in self.data.values():
            for tag in record.tags:
                if search_string.lower() in tag.value.lower():
                    results.append(str(record))
                    break
        return results

    def search_by_name(self, search_string):
        results = []
        for record in self.data.values():
            if search_string.lower() in record.name.value.lower():
                return record


class RecordNote:
    def __init__(self, name, text_note=None):
        self.name = Name(name)
        self.text_note = Name(text_note)
        self.tags = []

    def add_tag(self, tag):
        self.tags.append(Name(tag))

    def add_text_note(self, add_text_note):
        self.text_note = Name(''+str(self.text_note.value)+' '+add_text_note)

    def add_note(self, text_note):
        self.text_note = Name(text_note)
        
    def add_name(self, name):
        self.name = Name(name)
        
    def remove_tag(self, tag):
        self.tags = [p for p in self.tags if p.value != tag]

    def edit_tag(self, old_tag, new_tag):
        for i, tag in enumerate(self.tags):
            if tag.value == old_tag:
                self.tags[i] = Name(new_tag)

    def __str__(self):
        results = f"{self.name.value}: {' '.join(tag.value for tag in self.tags)}"
        if self.text_note:
                results += ' Текст нотатки: '+ str(self.text_note.value)
        return results
    
    def to_dict(self):
        return {
            'name': self.name.value,
            'text_note': str(self.text_note.value) if self.text_note else None,
            'tags': [tag.value for tag in self.tags]
        }

    @classmethod
    def from_dict(cls, data):
        record = cls(data['name'], data['text_note'])
        for tag in data['tags']:
            record.add_tag(tag)
        return record

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, name):
        del self.data[name]

    def search_record(self, search_criteria):
        for record in self.data.values():
            if search_criteria.lower() in record.name.value.lower():
                return record
        record = Record(search_criteria)
        self.add_record(record)
        return record

    def search_records(self, search_criteria):
        results = []
        for record in self.data.values():
            if search_criteria.lower() in record.name.value.lower():
                results.append(record)
        return results
    
    def show_all_records(self):
        results = ''
        for record in self.data.values():
            results += "\n"+f"{record.name.value}:"+"".join(f" {phone.value}" for phone in record.phones)
            if record.birthday:
                results += ' birthday: '+ str(record.birthday.value.date())
        if not results:
            results = "Contact list is empty"
        return results

    def __iter__(self):
        self._iter_index = 0
        self._iter_chunk_size = 5
        return self

    def __next__(self):
        if self._iter_index >= len(self.data):
            raise StopIteration

        chunk = list(self.data.values())[self._iter_index:self._iter_index + self._iter_chunk_size]
        self._iter_index += self._iter_chunk_size

        return "\n".join(str(record) for record in chunk)
    
    def save_to_file(self, file_path):
        data = {
            'records': [record.to_dict() for record in self.data.values()]
        }
        with open(file_path, 'w') as file:
            json.dump(data, file, default=str)

    def load_from_file(self):
        file_path = os.path.join(os.getcwd(), "address_book.json")
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
            for record_data in data['records']:
                record = Record.from_dict(record_data)
                self.add_record(record)
    
    def search_by_content(self, search_string):
        results = []
        for record in self.data.values():
            if search_string.lower() in record.name.value.lower():
                results.append(str(record))
            else:
                for phone in record.phones:
                    if search_string.lower() in phone.value.lower():
                        results.append(str(record))
                        break
        return results        

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = None
        if birthday:
            self.birthday = Birthday(birthday)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            # 1988-08-11 00:00:00
            #birthday = datetime.strptime(self.birthday.value, '%Y-%m-%d')
            birthday = self.birthday.value
            next_birthday = datetime(year=today.year, month=birthday.month, day=birthday.day).date()
            if today > next_birthday:
                next_birthday = datetime(year=today.year+1, month=birthday.month, day=birthday.day).date()
            days_left = (next_birthday - today).days
            return days_left
    
    def __str__(self):
        results = f"{self.name.value}: {' '.join(phone.value for phone in self.phones)}"
        if self.birthday:
                results += ' birthday: '+ str(self.birthday.value.date())
        return results
    
    def to_dict(self):
        return {
            'name': self.name.value,
            'birthday': str(self.birthday.value.date()) if self.birthday else None,
            'phones': [phone.value for phone in self.phones]
        }

    @classmethod
    def from_dict(cls, data):
        record = cls(data['name'], data['birthday'])
        for phone in data['phones']:
            record.add_phone(phone)
        return record

class Field:
    def __init__(self, value):
        self._value = value
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(self._validate_phone(value))
    
    @staticmethod
    def _validate_phone(phone):
        if not len(phone) == 10:
            raise CustomException("Phone number must have 10 digits")
        if not phone.isdigit():
            raise CustomException("Phone number should contain only digits")
        return phone

    @Field.value.setter
    def value(self, new_value):
        self._value = self._validate_phone(new_value)

class Birthday(Field):
    def __init__(self, value):
        super().__init__(self._validate_birthday(value))

    @staticmethod
    def _validate_birthday(value):
        if value == None:
            raise CustomException("Date of birth == None")
        if not len(value) == 10:
            raise CustomException("Date of birth must have 10 characters ""1988-08-11""")
        try:
            value = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise CustomException("Date of birth should be ""1988-08-11""")        
        return value
    
    @Field.value.setter
    def value(self, new_value):
        self._value = self._validate_birthday(new_value)

def main():
    print("Введіть команду")
    commands = {
        'hello': hello_command,
        'add': add_command,
        'change': change_command,
        'phone': phone_command,
        'show all': show_all_command,
        'iter rec': iter_record,
        'find': find_command,
        'note_add': note_add,
        'note_find': note_find,
        'note_show_all': note_show_all
    }

    while True:
        user_input = input("> ").lower()
        if user_input in ["good bye", "close", "exit"]:
            address_book.save_to_file(os.path.join(os.getcwd(), "address_book.json"))
            note_book.save_to_file(os.path.join(os.getcwd(), "note_book.json"))
            print("Good bye!")
            break
        
        for command, handler in commands.items():
            if user_input.startswith(command):
                params = user_input[len(command):].strip()
                result = handler(params)
                print(result)
                break
        else:
            print("Unknown command")

#contacts = {}
address_book = AddressBook()
address_book.load_from_file()

note_book = NoteBook()
note_book.load_from_file()

if __name__ == "__main__":
    main()