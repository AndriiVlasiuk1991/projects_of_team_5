import sys
from sorter import sort_file
from note_book import main_note_book
from customer_book import main_customer_book


def main():
    print('Вітаю!')
    while True:
        print("\n--------------- Menu ---------------\n")
        print('Ви у головному меню!\nДоступні команди:')
        print('1 - Книга клієнтів\n2 - Нотатки\n3 - Сортувати файли\n4 - Вихід')
        command = input('Оберіть команду: ')

        if command == '1':
            print("\nВи обрали команду під номером 1. Отже, вітаємо в книзі клієнтів!")
            main_customer_book()
            print("Ви завершили роботу в книзі клієнтів!")
        elif command == '2':
            print("\nВи обрали команду під номером 2. Отже, вітаємо в нотатках!")
            main_note_book()
            print("Ви завершили роботу в нотатках!")
        elif command == '3':
            print("\nВи обрали команду під номером 3 - 'Сортування файлів'!")
            sort_file()
            print("Сортування папки завершено!")
        elif command == '4':
            print("\nДо зустрічі!")
            break
        else:
            print("Такої команди не існує! Оберіть команду з вище перелічених!")
            print("------------ Команди не існує ------------\n")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        folder_name = sys.argv[1]
        main()
    else:
        main()
