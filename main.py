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

class Reporter:
    def __init__(self, book_shop):
        self.book_shop = book_shop

    def get_reporter(self, destination):
        if destination == "file":
            return FileReporter(self.book_shop)
        elif destination == "console":
            return ConsoleReporter(self.book_shop)

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

    @abstractmethod
    def sales_for_date(self, date_str):
        pass

    @abstractmethod
    def sales_for_period(self, start_date_str, end_date_str):
        pass

    @abstractmethod
    def sales_by_employee(self, employee):
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

    def sales_for_date(self, date_str):
        print(f"Sales for date: {date_str}")
        found_sales = False
        for sale in self.book_shop.sales_manager.sales:
            if sale.sale_date == date_str:
                print(sale.get_data())
                print("---")
                found_sales = True
        if not found_sales:
            print("No sales for this date.")

    def sales_for_period(self, start_date_str, end_date_str):
        print(f"Sales for period: {start_date_str} - {end_date_str}")
        found_sales = False
        for sale in self.book_shop.sales_manager.sales:
            if start_date_str <= sale.sale_date <= end_date_str:
                print(sale.get_data())
                print("---")
                found_sales = True
        if not found_sales:
            print("No sales in this period.")

    def sales_by_employee(self, employee):
        print(f"Sales by employee: {employee.full_name}")
        found_sales = False
        for sale in self.book_shop.sales_manager.sales:
            if sale.employee == employee:
                print(sale.get_data())
                print("---")
                found_sales = True
        if not found_sales:
            print("No sales by this employee.")

class FileReporter(IReport):
    def employees_report(self):
        with open("employees.txt", "w+", encoding="utf-8") as my_file:
            my_file.write("Employees :\n")
            for employee in self.book_shop.employees_manager.employees:
                my_file.write("---\n")
                my_file.write(employee.get_data() + "\n")

    def books_report(self):
        with open("books.txt", "w+", encoding="utf-8") as my_file:
            my_file.write("Books :\n")
            for book in self.book_shop.books_manager.books:
                my_file.write("---\n")
                my_file.write(book.get_data() + "\n")

    def sales_report(self):
        with open("sales.txt", "w+", encoding="utf-8") as my_file:
            my_file.write("Sales :\n")
            for sale in self.book_shop.sales_manager.sales:
                my_file.write("---\n")
                my_file.write(sale.get_data() + "\n")

    def sales_for_date(self, date_str):
        filename = f"sales_for_date_{date_str}.txt"
        with open(filename, "w+", encoding="utf-8") as f:
            f.write(f"Sales for date: {date_str}\n")
            found_sales = False
            for sale in self.book_shop.sales_manager.sales:
                if sale.sale_date == date_str:
                    f.write("---\n")
                    f.write(sale.get_data() + "\n")
                    found_sales = True
            if not found_sales:
                f.write("No sales for this date.\n")

    def sales_for_period(self, start_date_str, end_date_str):
        filename = f"sales_for_period_{start_date_str}_{end_date_str}.txt"
        with open(filename, "w+", encoding="utf-8") as f:
            f.write(f"Sales for period: {start_date_str} - {end_date_str}\n")
            found_sales = False
            for sale in self.book_shop.sales_manager.sales:
                if start_date_str <= sale.sale_date <= end_date_str:
                    f.write("---\n")
                    f.write(sale.get_data() + "\n")
                    found_sales = True
            if not found_sales:
                f.write("No sales in this period.\n")

    def sales_by_employee(self, employee):
        safe_employee_name = employee.full_name.replace(" ", "_")
        filename = f"sales_by_employee_{safe_employee_name}.txt"
        with open(filename, "w+", encoding="utf-8") as f:
            f.write(f"Sales by employee: {employee.full_name}\n")
            found_sales = False
            for sale in self.book_shop.sales_manager.sales:
                if sale.employee == employee:
                    f.write("---\n")
                    f.write(sale.get_data() + "\n")
                    found_sales = True
            if not found_sales:
                f.write("No sales by this employee.\n")

class EmployeesManager:
    def __init__(self):
        self.employees = []

    def add_employee(self, employee):
        if employee not in self.employees:
            self.employees.append(employee)
        else:
            print("This employee already exists.")

    def remove_employee(self, employee):
        if employee in self.employees:
            self.employees.remove(employee)
        else:
            print("This employee doesn't exist.")

class BooksManager:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)
        else:
            print("This book doesn't exist.")

class SalesManager:
    def __init__(self):
        self.sales = []

    def add_sale(self, sale):
        self.sales.append(sale)

    def remove_sale(self, sale):
        if sale in self.sales:
            self.sales.remove(sale)
        else:
            print("This sale doesn't exist.")

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
        return (
            f"full name : {self.full_name}\n"
            f"work position : {self.position}\n"
            f"phone number : {self.phone_number}\n"
            f"email : {self.email}"
        ).title()

    def __eq__(self, other):
        if not isinstance(other, Employee):
            return False
        return (
            self.full_name == other.full_name
            and self.position == other.position
            and self.phone_number == other.phone_number
            and self.email == other.email
        )

class Book(IObject):
    def __init__(self, title, year, author, genre, cost, potential_price):
        self.title = title
        self.year = year
        self.author = author
        self.genre = genre
        self.cost = cost
        self.potential_price = potential_price

    def get_data(self):
        return (
            f"title : {self.title}\n"
            f"year : {self.year}\n"
            f"author : {self.author}\n"
            f"genre : {self.genre}\n"
            f"cost : {self.cost}\n"
            f"potencial price : {self.potential_price}"
        ).title()

class Sale(IObject):
    def __init__(self, employee, book, sale_date, real_price):
        self.employee = employee
        self.book = book
        self.sale_date = sale_date
        self.real_price = real_price

    def get_data(self):
        return (
            f"employee : {self.employee.full_name}\n"
            f"book : {self.book.title}\n"
            f"sale date : {self.sale_date}\n"
            f"real price : {self.real_price}"
        ).title()

if __name__ == "__main__":
    shop = BookShop()
    book_manager = shop.get_books_manager()
    book = Book("Python", 2025, "Maksym K", "Educative", 10, 20)
    book_manager.add_book(book)
    book1 = Book("C#", 2024, "Maksym K", "Educative", 10, 20)
    book_manager.add_book(book1)
    emp_manager = shop.get_employees_manager()
    emp1 = Employee("John Doe", "Sales Manager", "+123456789", "john@example.com")
    emp_manager.add_employee(emp1)
    emp2 = Employee("Jane Smith", "Cashier", "+987654321", "jane@example.com")
    emp_manager.add_employee(emp2)
    sales_manager = shop.get_sales_manager()
    sale1 = Sale(emp1, book, "2025-02-01", 18.0)
    sale2 = Sale(emp2, book1, "2025-02-02", 19.5)
    sale3 = Sale(emp1, book1, "2025-02-03", 20.0)
    sales_manager.add_sale(sale1)
    sales_manager.add_sale(sale2)
    sales_manager.add_sale(sale3)
    reporter = Reporter(shop)
    file_reporter = reporter.get_reporter("file")
    file_reporter.books_report()
    console_reporter = reporter.get_reporter("console")
    console_reporter.sales_by_employee(emp1)
    file_reporter.sales_for_date("2025-02-02")
    console_reporter.sales_for_period("2025-02-01", "2025-02-03")
