from abc import ABC, abstractmethod

class IObject(ABC):
    @abstractmethod
    def get_data(self):
        pass

class Employee(IObject):
    def __init__(self, full_name, position, phone_number, email):
        self.full_name = full_name
        self.position = position
        self.phone_number = phone_number
        self.email = email

    def get_data(self):
        return f"full name : {self.full_name}\nwork position : {self.position}\nphone number : {self.phone_number}\nemail : {self.email}".title()

class BookShop:
    def __init__(self):
        self.employees_manager = EmployeesManager()
        self.books_manager = BooksManager()
        self.sales_manager = SalesManager()

    def get_employees_manager(self):
        return self.employees_manager

    def get_books_manager(self):
        return self.books_manager

    def get_sales_manager(self):
        return self.sales_manager


class EmployeesManager:
    def __init__(self):
        self.employees = {}

class Book:
    """
    Класс, который хранит информацию об одной книге.
    """
    def __init__(self, title: str, year: int, author: str, genre: str, cost: float, potential_price: float):
        self.title = title
        self.year = year
        self.author = author
        self.genre = genre
        self.cost = cost
        self.potential_price = potential_price

    def to_dict(self) -> dict:
        """
        Возвращает словарь с данными книги для сериализации в JSON.
        """
        return {
            "title": self.title,
            "year": self.year,
            "author": self.author,
            "genre": self.genre,
            "cost": self.cost,
            "potential_price": self.potential_price
        }

    @staticmethod
    def from_dict(data: dict):
        """
        Создаёт Book-объект из словаря (например, после чтения из JSON-файла).
        """
        return Book(
            title=data["title"],
            year=data["year"],
            author=data["author"],
            genre=data["genre"],
            cost=data["cost"],
            potential_price=data["potential_price"]
        )



