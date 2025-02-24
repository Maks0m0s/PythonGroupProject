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


