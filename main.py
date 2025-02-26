from abc import ABC, abstractmethod

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

    def add_employee(self, full_name, position, phone_number, email):
        if full_name not in self.employees.keys():
            self.employees[full_name] = Employee(full_name, position, phone_number, email)
            return
        print("This employee already exists.")

    def remove_employee(self, full_name):
        if full_name in self.employees.keys():
            del self.employees[full_name]
            return
        print("This employee doesn't exist.")

class BooksManager:
    def __init__(self):
        self.books = {}

class SalesManager:
    def __init__(self):
        self.sales = {}

    def add_sale(self, employee, book, date, real_price):
        pass

    def remove_sale(self, employee, book, date, real_price):
        pass

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

class Book(IObject):
    def __init__(self, title: str, year: int, author: str, genre: str, cost: float, potential_price: float):
        self.title = title
        self.year = year
        self.author = author
        self.genre = genre
        self.cost = cost
        self.potential_price = potential_price

    def get_data(self):
        return f"title : {self.title}\nyear : {self.year}\nauthor : {self.author}\ngenre : {self.genre}\ncost : {self.cost}\npotencial price : {self.potential_price}".title()

class Sale(IObject):
    def __init__(self, employee, book, sale_date, real_price):
        self.employee = employee
        self.book = book
        self.sale_date = sale_date
        self.real_price = real_price

    def get_data(self):
        return f"employee : {self.employee}\nbook : {self.book}\nsale date : {self.sale_date}\nreal price : {self.real_price}".title()
