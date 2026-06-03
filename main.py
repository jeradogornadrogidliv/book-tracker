import json
import os
from datetime import datetime

DATA_FILE = "books.json"

def load_books():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_books(books):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

def add_book(books):
    print("\n--- Добавление книги ---")
    author = input("Введите автора: ").strip()
    title = input("Введите название: ").strip()
    
    for book in books:
        if book["author"].lower() == author.lower() and book["title"].lower() == title.lower():
            print("Ошибка: Такая книга уже существует!")
            return books
    
    try:
        rating = int(input("Введите оценку (от 1 до 5): "))
        if rating < 1 or rating > 5:
            print("Ошибка: Оценка должна быть от 1 до 5")
            return books
    except ValueError:
        print("Ошибка: Введите целое число")
        return books
    
    date = input("Введите дату прочтения (ГГГГ-ММ-ДД) или Enter для текущей даты: ").strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Неверный формат, используется сегодняшняя дата")
            date = datetime.now().strftime("%Y-%m-%d")
    
    books.append({
        "author": author,
        "title": title,
        "rating": rating,
        "date": date
    })
    save_books(books)
    print(f"✅ Книга '{title}' добавлена!")
    return books

def show_books(books):
    """Показать все книги"""
    print("\n--- Список книг ---")
    if not books:
        print("Нет добавленных книг")
        return
    
    for i, book in enumerate(books, 1):
        print(f"{i}. {book['author']} - «{book['title']}» | Оценка: {book['rating']}/5 | Дата: {book['date']}")

def show_average_rating(books):
    """Показать среднюю оценку"""
    if not books:
        print("\nНет книг для расчёта")
        return
    
    avg = sum(book["rating"] for book in books) / len(books)
    print(f"\nСредняя оценка всех книг: {avg:.2f} / 5")

def show_author_stats(books):
    """Статистика по авторам"""
    print("\n--- Статистика по авторам ---")
    if not books:
        print("Нет книг")
        return
    
    author_counts = {}
    for book in books:
        author_counts[book["author"]] = author_counts.get(book["author"], 0) + 1
    
    for author, count in sorted(author_counts.items()):
        print(f"{author}: {count} книг(и)")

def delete_book(books):
    """Удаление книги"""
    print("\n--- Удаление книги ---")
    if not books:
        print("Нет книг для удаления")
        return books
    
    show_books(books)
    try:
        choice = int(input("\nВведите номер книги для удаления: "))
        if 1 <= choice <= len(books):
            removed = books.pop(choice - 1)
            save_books(books)
            print(f"Книга '{removed['title']}' удалена")
        else:
            print("Неверный номер")
    except ValueError:
        print("Введите число")
    return books

def main():
    books = load_books()
    
    while True:
        print("\n" + "="*40)
        print("ТРЕКЕР ПРОЧИТАННЫХ КНИГ")
        print("="*40)
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Показать среднюю оценку")
        print("4. Статистика по авторам")
        print("5. Удалить книгу")
        print("6. Выход")
        
        choice = input("\nВыберите действие (1-6): ").strip()
        
        if choice == "1":
            books = add_book(books)
        elif choice == "2":
            show_books(books)
        elif choice == "3":
            show_average_rating(books)
        elif choice == "4":
            show_author_stats(books)
        elif choice == "5":
            books = delete_book(books)
        elif choice == "6":
            print("До свидания!")
            break
        else:
            print("Неверный выбор, попробуйте снова")

if __name__ == "__main__":
    main()
