from abc import ABC, abstractmethod
                            "Співробітник"
class IEmployee(ABC):
    @abstractmethod
    def get_employee_data(self):
        pass

class Employee(IEmployee):
    def __init__(self, full_name, position, phone_number, email):
        self.full_name = full_name
        self.position = position
        self.phone_number = phone_number
        self.email = email

    def get_employee_data(self):
        return f"full name : {self.full_name}\nwork position : {self.position}\nphone number : {self.phone_number}\nemail : {self.email}".title()

                                    "книга"
        
    def add_book(self, title: str, year: int, author: str, genre: str, cost: float, potential_price: float):
        """Додає нову книгу."""
    for b in self.books:
        if b.title == title:
            print(f"Книга з назвою '{title}' вже існує.")
            return
    self.books.append(Book(title, year, author, genre, cost, potential_price))


def remove_book(self, title: str):
    """Видаляє книгу за назвою."""
    before_count = len(self.books)
    self.books = [b for b in self.books if b.title != title]
    after_count = len(self.books)
    if before_count == after_count:
        print(f"Книгу з назвою '{title}' не знайдено.")
    else:
        print(f"Книгу '{title}' успішно видалено.")

                "Продажі"

