#Icluded Patterns Composite, Factory

from abc import ABC, abstractmethod

#Main Object
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

#-- R E P O R T S --
#Main Report Object
#Factory
class Reporter:
    def __init__(self, book_shop):
        self.book_shop = book_shop

    def get_reporter(self, destination):
        if destination == "file":
            return FileReporter(self.book_shop)
        elif destination == "console":
            return ConsoleReporter(self.book_shop)
        else:
            print("You can write only file/console")

class IReport(ABC):
    def __init__(self, book_shop):
        self.book_shop = book_shop

    @abstractmethod
    def employees_report(self):
        pass

    @abstractmethod
    def books_report(self):
        pass

    @abstractmethod
    def sales_report(self):
        pass

class ConsoleReporter(IReport):
    def employees_report(self):
        print("Employees :")
        for employee in self.book_shop.employees_manager.employees:
            print(employee.get_data())
            print("---")

    def books_report(self):
        print("Books :")
        for book in self.book_shop.books_manager.books:
            print(book.get_data())
            print("---")

    def sales_report(self):
        print("Sales :")
        for sale in self.book_shop.sales_manager.sales:
            print(sale.get_data())
            print("---")

class FileReporter(IReport):
    def employees_report(self):
        with open("employees.txt", "w+") as my_file:
            my_file.write("Employees :\n")
            for employee in self.book_shop.employees_manager.employees:
                my_file.write("---\n")
                my_file.write(employee.get_data() + "\n")
            my_file.close()

    def books_report(self):
        with open("books.txt", "w+") as my_file:
            my_file.write("Books :\n")
            for book in self.book_shop.books_manager.books:
                my_file.write("---\n")
                my_file.write(book.get_data() + "\n")
            my_file.close()

    def sales_report(self):
        with open("sales.txt", "w+") as my_file:
            my_file.write("Sales :\n")
            for sale in self.book_shop.sales_manager.sales:
                my_file.write("---\n")
                my_file.write(sale.get_data() + "\n")
            my_file.close()

#-- M A N A G E R S --
#Composite
class EmployeesManager:
    def __init__(self):
        self.employees = []

    def add_employee(self, employee):
        if employee not in self.employees:
            self.employees.append(employee)
            return
        print("This employee already exists.")

    def remove_employee(self, employee):
        if employee in self.employees:
            self.employees.remove(employee)
            return
        print("This employee doesn't exist.")

#Composite
class BooksManager:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)
            return
        print("This book doesn't exist.")

#Composite
class SalesManager:
    def __init__(self):
        self.sales = []

    def add_sale(self, sale):
        self.sales.append(sale)

    def remove_sale(self, sale):
        if sale in self.sales:
            self.sales.remove(sale)
            return
        print("This sale doesn't exist.")

#-- O B J E C T S --

#Interface
class IObject(ABC):
    @abstractmethod
    def get_data(self):
        pass

#Leaf
class Employee(IObject):
    def __init__(self, full_name, position, phone_number, email):
        self.full_name = full_name
        self.position = position
        self.phone_number = phone_number
        self.email = email

    def get_data(self):
        return f"full name : {self.full_name}\nwork position : {self.position}\nphone number : {self.phone_number}\nemail : {self.email}".title()

#Leaf
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

#Leaf
class Sale(IObject):
    def __init__(self, employee, book, sale_date, real_price):
        self.employee = employee
        self.book = book
        self.sale_date = sale_date
        self.real_price = real_price

    def get_data(self):
        return f"employee : {self.employee}\nbook : {self.book}\nsale date : {self.sale_date}\nreal price : {self.real_price}".title()


shop = BookShop()
book_manager = shop.get_books_manager()
reporter = Reporter(shop)
file_reporter = reporter.get_reporter("file")

book = Book("Python", 2025, "Maksym K", "Educative", 10, 20)

book_manager.add_book(book)

book1 = Book("C#", 2024, "Maksym K", "Educative", 10, 20)

book_manager.add_book(book1)


file_reporter.books_report()
