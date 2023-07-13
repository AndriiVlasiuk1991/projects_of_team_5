from pathlib import Path
import sys
import shutil

def normalize(name):
    map = {
        ord("а"): "a",
        ord("б"): "b",
        ord("в"): "v",
        ord("г"): "h",
        ord("ґ"): "g",
        ord("д"): "d",
        ord("е"): "e",
        ord("є"): "ie",
        ord("ж"): "zh",
        ord("з"): "z",
        ord("и"): "y",
        ord("і"): "i",
        ord("ї"): "i",
        ord("й"): "i",
        ord("к"): "k",
        ord("л"): "l",
        ord("м"): "m",
        ord("н"): "n",
        ord("о"): "o",
        ord("п"): "p",
        ord("р"): "r",
        ord("с"): "s",
        ord("т"): "t",
        ord("у"): "u",
        ord("ф"): "f",
        ord("х"): "kh",
        ord("ц"): "ts",
        ord("ч"): "ch",
        ord("ш"): "sh",
        ord("щ"): "shch",
        ord("ь"): "",
        ord("ю"): "iu",
        ord("я"): "ia",
        ord("А"): "A",
        ord("Б"): "B",
        ord("В"): "V",
        ord("Г"): "H",
        ord("Ґ"): "G",
        ord("Д"): "D",
        ord("Е"): "E",
        ord("Є"): "Ye",
        ord("Ж"): "Zh",
        ord("З"): "Z",
        ord("И"): "Y",
        ord("І"): "I",
        ord("Ї"): "Yi",
        ord("Й"): "Y",
        ord("К"): "K",
        ord("Л"): "L",
        ord("М"): "M",
        ord("Н"): "N",
        ord("О"): "O",
        ord("П"): "P",
        ord("Р"): "R",
        ord("С"): "S",
        ord("Т"): "T",
        ord("У"): "U",
        ord("Ф"): "F",
        ord("Х"): "Kh",
        ord("Ц"): "Ts",
        ord("Ч"): "Ch",
        ord("Ш"): "Sh",
        ord("Щ"): "Shch",
        ord("Ю"): "Yu",
        ord("Я"): "Ya",
        ord("Ё"): "Yo",
        ord("ё"): "yo",
        ord("Ъ"): "",
        ord("ъ"): "",
        ord("Ь"): "",
    }
    normalize_name = name.translate(map)
    finally_name = "".join(ch if ch.isalnum() else "_" for ch in normalize_name)

    return finally_name


def sort_file():
    count_list = []
    ignored_folders = ["video", "audio", "images", "documents", "archives"]

    while True:
        folder_name = input('Введіть шлях до папки, в якій потрібно відсортувати файли або exit для виходу: ')
        if folder_name == "exit":
            break
        path = Path(folder_name)
        if path.exists():
            if path.is_dir():
                items = path.glob("**/*")
                for item in items:
                    if any(part in str(item) for part in ignored_folders):
                        continue
                    try:
                        if item.suffix in [".mp4", ".avi", ".mov", ".mkv"]:
                            dir = path / "video"
                            count_list.append(item.suffix)
                        elif item.suffix in [".mp3", ".ogg", ".wav", ".amr"]:
                            dir = path / "audio"
                            count_list.append(item.suffix)
                        elif item.suffix in [
                            ".jpg",
                            ".jpeg",
                            ".png",
                            ".svg",
                            ".snagx",
                            ".gif",
                        ]:
                            dir = path / "images"
                            count_list.append(item.suffix)
                        elif item.suffix in [
                            ".txt",
                            ".doc",
                            ".docx",
                            ".pdf",
                            ".xlsx",
                            ".pptx",
                        ]:
                            dir = path / "documents"
                            count_list.append(item.suffix)
                        elif item.suffix in [".zip", ".gz", ".tar"]:
                            dir = path / "archives" / item.stem
                            count_list.append(item.suffix)
                            dir.mkdir(parents=True, exist_ok=True)
                            shutil.unpack_archive(item, dir)
                            continue
                        elif item.is_dir():
                            if not any(item.iterdir()):
                                item.rmdir()
                            else:
                                try:
                                    item.rename(
                                        item.resolve().parent / Path(normalize(item.name))
                                    )
                                except FileExistsError:
                                    item.rename(
                                        item.resolve().parent
                                        / Path(normalize(item.name) + "1")
                                    )
                            continue

                        else:
                            continue

                        dir.mkdir(parents=True, exist_ok=True)
                        item.rename(dir / (normalize(item.stem) + item.suffix))

                    except PermissionError:
                        print(f"Файл {item.name} зайнятий програмою або процесом")

            else:
                print(f"{path} це файл")

            count_files(count_list)
            input("Натисніть клавішу Enter для повернення в головне меню...")
            break
        else:
            print(f"{path.absolute()} не існує")





def count_files(count_list):
    index_count = {}
    count_video = ""
    count_audio = ""
    count_images = ""
    count_documents = ""
    count_archives = ""

    for index in count_list:
        if index in index_count:
            index_count[index] += 1
        else:
            index_count[index] = 1

    print(f"\nСортування файлів успішно завершено: \n")

    for index, count in index_count.items():
        if index in [".mp4", ".avi", ".mov", ".mkv"]:
            count_video += f'\t - {count} файлів {index}\n'
        elif index in [".mp3", ".ogg", ".wav", ".amr"]:
            count_audio += f'\t - {count} файлів {index}\n'
        elif index in [".jpg", ".jpeg", ".png", ".svg", ".snagx", ".gif"]:
            count_images += f'\t - {count} файлів {index}\n'
        elif index in [".txt", ".doc", ".docx", ".pdf", ".xlsx", ".pptx"]:
            count_documents += f'\t - {count} файлів {index}\n'
        elif index in [".zip", ".gz", ".tar"]:
            count_archives += f'\t - {count} архівів {index}\n'

    if len(count_archives):
        print(f'В папку "archives" розархівовано: \n{count_archives}')
    if len(count_images):
        print(f'В папку "images" переміщено: \n{count_images}')
    if len(count_audio):
        print(f'В папку "audio" переміщено: \n{count_audio}')
    if len(count_video):
        print(f'В папку "video" переміщено: \n{count_video}')
    if len(count_documents):
        print(f'В папку "documents" переміщено: \n{count_documents}')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        folder_name = sys.argv[1]
        sort_file(folder_name)
    else:
        sort_file()