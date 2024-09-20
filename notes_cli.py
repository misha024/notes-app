import json
import os
from datetime import datetime

NOTES_FILE = "notes.json"


class NoteManager:
    @staticmethod
    def load_notes():
        if not os.path.exists(NOTES_FILE):
            return []
        try:
            with open(NOTES_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            print("Ошибка чтения файла заметок. Файл может быть поврежден.")
            return []

    @staticmethod
    def save_notes(notes):
        try:
            with open(NOTES_FILE, "w", encoding="utf-8") as file:
                json.dump(notes, file, indent=4, ensure_ascii=False)
        except IOError:
            print("Ошибка записи файла заметок.")

    @staticmethod
    def generate_note_id(notes):
        return max([note['id'] for note in notes], default=0) + 1

    @staticmethod
    def create_note():
        title = input("\nВведите заголовок заметки: ").strip()
        body = input("Введите текст заметки: ").strip()

        if not title or not body:
            print("Заголовок и текст не могут быть пустыми.")
            return

        note = {
            "id": NoteManager.generate_note_id(NoteManager.load_notes()),
            "title": title,
            "body": body,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        notes = NoteManager.load_notes()
        notes.append(note)
        NoteManager.save_notes(notes)
        print("Заметка успешно создана.")

    @staticmethod
    def edit_note():
        notes = NoteManager.load_notes()
        if not notes:
            print("Заметок нет.")
            return

        try:
            note_id = int(input("\nВведите ID заметки для редактирования: ").strip())
        except ValueError:
            print("ID должен быть числом.")
            return

        for note in notes:
            if note["id"] == note_id:
                note["title"] = input(f"Текущий заголовок: {note['title']}. Введите новый заголовок: ").strip()
                note["body"] = input(f"Текущий текст: {note['body']}. Введите новый текст: ").strip()
                note["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                NoteManager.save_notes(notes)
                print("Заметка успешно обновлена.")
                return

        print("Заметка с указанным ID не найдена.")

    @staticmethod
    def delete_note():
        notes = NoteManager.load_notes()
        if not notes:
            print("Заметок нет.")
            return

        try:
            note_id = int(input("\nВведите ID заметки для удаления: ").strip())
        except ValueError:
            print("ID должен быть числом.")
            return

        updated_notes = [note for note in notes if note["id"] != note_id]

        if len(updated_notes) == len(notes):
            print("Заметка с указанным ID не найдена.")
        else:
            NoteManager.save_notes(updated_notes)
            print("Заметка успешно удалена.")

    @staticmethod
    def view_note():
        notes = NoteManager.load_notes()
        if not notes:
            print("Заметок нет.")
            return

        try:
            note_id = int(input("\nВведите ID заметки для просмотра: ").strip())
        except ValueError:
            print("ID должен быть числом.")
            return

        for note in notes:
            if note["id"] == note_id:
                print(f"\nЗаголовок: {note['title']}")
                print(f"Дата: {note['datetime']}")
                print(f"Содержание: {note['body']}")
                return

        print("Заметка с указанным ID не найдена.")

    @staticmethod
    def list_notes():
        notes = NoteManager.load_notes()
        if not notes:
            print("Заметок нет.")
            return

        print("\nСписок заметок:")
        for note in notes:
            print(f"- ID: {note['id']}, Заголовок: {note['title']}, Дата: {note['datetime']}")


class NoteApp:
    @staticmethod
    def display_menu():
        print("\nДоступные команды: ")
        print("1. Создать заметку")
        print("2. Просмотреть заметку")
        print("3. Редактировать заметку")
        print("4. Удалить заметку")
        print("5. Показать все заметки")
        print("6. Выйти")

    @staticmethod
    def run():
        NoteApp.display_menu()
        while True:
            command = input("\nВведите команду (1-6): ").strip()

            if command == "1":
                NoteManager.create_note()
            elif command == "2":
                NoteManager.view_note()
            elif command == "3":
                NoteManager.edit_note()
            elif command == "4":
                NoteManager.delete_note()
            elif command == "5":
                NoteManager.list_notes()
            elif command == "6":
                print("Выход...")
                break
            elif command.lower() == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                NoteApp.display_menu()


if __name__ == "__main__":
    try:
        NoteApp.run()
    except KeyboardInterrupt:
        print("\nПрограмма завершена.")
