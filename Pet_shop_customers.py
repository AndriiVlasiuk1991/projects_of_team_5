import sys
import os
from sorter import sort_file
from note_book import magic_8_ball, note_add, note_find, note_show_all, note_remove, note_edite

def main():
    print('Вітаю!\n') #ToDo Потрібно дати коротенький опис програми, зробим в самому кінці
    print('1 - Книга клієнтів\n2 - Нотатки\n3 - Сортувати файли\n') #ToDo Підправити текст
    command = input('Оберіть команду: ')

    if command == '1':
        pass
    elif command == '2':
        print('1 - Для створення нової нотатки\n2 - Для пошуку по нотаткам\n3 - Вивести всі нотатки\n4 - Видалити нотатку по назві\n5 - Редагувати нотату')
        commandNote = input('Оберіть команду: ')
        if commandNote == '1':
            note_add()
        elif commandNote == '2':
            result = note_find()
            if result == '':
                print('Нічого не знайдено.')
            else:
                print(result)  
        elif commandNote == '3':
            print(note_show_all())
        elif commandNote == '4':
            note_remove()
        elif commandNote == '5':
            note_edite()
        else:
            print('Команда невідома')
              
    elif command == '3':
        list_error_files = []
        while True:
            try:
                folder_name = r"C:\Users\andrey.vlasiuk\Desktop"
                sort_file(folder_name=folder_name)
            except OSError as error:
                error_file = os.path.basename(error.filename)
                if error_file not in list_error_files:
                    list_error_files.append(error_file)
                    if error.errno == 22:
                        print(f"Файл {error_file} не відсортовано. Неприпустима назва файлу")
                        continue
                    elif error.errno in [17, 183]:
                        print(f"Файл {error_file} не відсортовано. Цей файл вже існує в папці призначення")
                        continue
                else:
                    print(error)
                    continue
            else:
                break



    else:
        pass



if __name__ == '__main__':
    if len(sys.argv) > 1:
        folder_name = sys.argv[1]
        sort_file(folder_name)
    else:
        main()