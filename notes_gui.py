import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

NOTES_FILE = "notes.json"


def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as file:
            return json.load(file)
    return []


def save_notes(notes):
    with open(NOTES_FILE, "w") as file:
        json.dump(notes, file, indent=4)


def create_note():
    title = simpledialog.askstring("Создать заметку", "Введите заголовок:")
    if title:
        body = simpledialog.askstring("Создать заметку", "Введите текст:")
        if body:
            note = {
                "id": len(load_notes()) + 1,
                "title": title,
                "body": body,
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            notes = load_notes()
            notes.append(note)
            save_notes(notes)
            messagebox.showinfo("Успех", "Заметка создана.")
        else:
            messagebox.showwarning("Ошибка", "Текст заметки не может быть пустым.")
    else:
        messagebox.showwarning("Ошибка", "Заголовок не может быть пустым.")


def edit_note():
    notes = load_notes()
    note_id = simpledialog.askinteger("Редактировать заметку", "Введите ID заметки:")
    if note_id:
        for note in notes:
            if note["id"] == note_id:
                new_title = simpledialog.askstring("Редактировать заметку", f"Текущий заголовок: {note['title']}. Введите новый заголовок:")
                new_body = simpledialog.askstring("Редактировать заметку", f"Текущий текст: {note['body']}. Введите новый текст:")
                if new_title and new_body:
                    note["title"] = new_title
                    note["body"] = new_body
                    note["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_notes(notes)
                    messagebox.showinfo("Успех", "Заметка обновлена.")
                else:
                    messagebox.showwarning("Ошибка", "Заголовок и текст не могут быть пустыми.")
                return
        messagebox.showwarning("Ошибка", "Заметка с таким ID не найдена.")
    else:
        messagebox.showwarning("Ошибка", "Введите корректный ID.")


def delete_note():
    notes = load_notes()
    note_id = simpledialog.askinteger("Удалить заметку", "Введите ID заметки:")
    if note_id:
        notes = [note for note in notes if note["id"] != note_id]
        save_notes(notes)
        messagebox.showinfo("Успех", "Заметка удалена.")
    else:
        messagebox.showwarning("Ошибка", "Введите корректный ID.")


def list_notes():
    notes = load_notes()
    if notes:
        notes_str = "\n".join([f"ID: {note['id']}, Заголовок: {note['title']}, Дата: {note['datetime']}" for note in notes])
        messagebox.showinfo("Список заметок", notes_str)
    else:
        messagebox.showinfo("Список заметок", "Заметок пока нет.")


def main():
    root = tk.Tk()
    root.title("Приложение для заметок")

    tk.Label(root, text="Меню").pack(pady=10)

    tk.Button(root, text="Создать заметку", command=create_note).pack(fill="x", padx=10, pady=5)
    tk.Button(root, text="Редактировать заметку", command=edit_note).pack(fill="x", padx=10, pady=5)
    tk.Button(root, text="Удалить заметку", command=delete_note).pack(fill="x", padx=10, pady=5)
    tk.Button(root, text="Показать все заметки", command=list_notes).pack(fill="x", padx=10, pady=5)

    tk.Button(root, text="Выход", command=root.quit).pack(fill="x", padx=10, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
