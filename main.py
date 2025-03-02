#Icluded Patterns Composite, Factory

from abc import ABC, abstractmethod
import json 


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

    def save_data(self, filename):
        """
        Сохраняет сотрудников, книги и продажи в один JSON-файл.
        """
        data = {
            "employees": [
                {
                    "full_name": e.full_name,
                    "position": e.position,
                    "phone_number": e.phone_number,
                    "email": e.email
                }
                for e in self.employees_manager.employees
            ],
            "books": [
                {
                    "title": b.title,
                    "year": b.year,
                    "author": b.author,
                    "genre": b.genre,
                    "cost": b.cost,
                    "potential_price": b.potential_price
                }
                for b in self.books_manager.books
            ],
            "sales": [
                {
                    "employee_full_name": s.employee.full_name,  
                    "book_title": s.book.title,                  
                    "sale_date": s.sale_date,
                    "real_price": s.real_price
                }
                for s in self.sales_manager.sales
            ]
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_data(self, filename):
        """
        Загружает сотрудников, книги и продажи из JSON-файла,
        предварительно очищая все списки в менеджерах.
        """
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

       
        self.employees_manager.employees.clear()
        self.books_manager.books.clear()
        self.sales_manager.sales.clear()

    
        employees_map = {}
        for e_data in data.get("employees", []):
            emp = Employee(
                e_data["full_name"],
                e_data["position"],
                e_data["phone_number"],
                e_data["email"]
            )
            self.employees_manager.add_employee(emp)
            employees_map[emp.full_name] = emp

      
        books_map = {}
        for b_data in data.get("books", []):
            book = Book(
                b_data["title"],
                b_data["year"],
                b_data["author"],
                b_data["genre"],
                b_data["cost"],
                b_data["potential_price"]
            )
            self.books_manager.add_book(book)
            books_map[book.title] = book

       
        for s_data in data.get("sales", []):
            emp = employees_map.get(s_data["employee_full_name"])
            bk = books_map.get(s_data["book_title"])
            sale = Sale(emp, bk, s_data["sale_date"], s_data["real_price"])
            self.sales_manager.add_sale(sale)


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

    @abstractmethod
    def best_selling_book_for_period(self, start_date, finish_date):
        pass

    @abstractmethod
    def most_successful_employee_for_period(self, start_date, finish_date):
        pass

    @abstractmethod
    def total_money_for_period(self, start_date, finish_date):
        pass

    @abstractmethod
    def most_selling_author_for_period(self, start_date, finish_date):
        pass

    @abstractmethod
    def most_selling_genre_for_period(self, start_date, finish_date):
        """
        Метод для определения наиболее продаваемого жанра за указанный период.
        """
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

    def best_selling_book_for_period(self, start_date, finish_date):
        print(f"The best selling book for period: {start_date} - {finish_date} :".title())
        found_books = False
        books_in_period = []
        for sale in self.book_shop.sales_manager.sales:
            if start_date <= sale.sale_date <= finish_date:
                books_in_period.append(sale.book.title)
                found_books = True
        if not found_books:
            print("No books in period.")
            return
        books_sale_number = [books_in_period.count(b) for b in books_in_period]
        max_sale_number = max(books_sale_number)
        index = books_sale_number.index(max_sale_number)
        print(books_in_period[index])

    def most_successful_employee_for_period(self, start_date, finish_date):
        print(f"The most successful employee for period {start_date} - {finish_date} :".title())
        found_employees = False
        employees_in_period = []
        for sale in self.book_shop.sales_manager.sales:
            if start_date <= sale.sale_date <= finish_date:
                employees_in_period.append(sale.employee)
                found_employees = True
        if not found_employees:
            print("No employees in period.")
            return
        employees_sale_number = [employees_in_period.count(e) for e in employees_in_period]
        max_sale_number = max(employees_sale_number)
        index = employees_sale_number.index(max_sale_number)
        print(employees_in_period[index].get_data())

    def total_money_for_period(self, start_date, finish_date):
        print(f"Total earned money for period {start_date} - {finish_date} :".title())
        found_sales = False
        sales_in_period = []
        for sale in self.book_shop.sales_manager.sales:
            if start_date <= sale.sale_date <= finish_date:
                sales_in_period.append(sale.real_price)
                found_sales = True
        if not found_sales:
            print("No sales in period.")
            return
        total_money = sum(sales_in_period)
        print(f"{total_money}$")

    def most_selling_author_for_period(self, start_date, finish_date):
        print(f"The most selling book-author for period {start_date} - {finish_date} :".title())
        found_book = False
        authors_in_period = []
        for sale in self.book_shop.sales_manager.sales:
            if start_date <= sale.sale_date <= finish_date:
                authors_in_period.append(sale.book.author)
                found_book = True
        if not found_book:
            print("No books in period.")
            return
        authors_sale_number = [authors_in_period.count(a) for a in authors_in_period]
        max_sale_number = max(authors_sale_number)
        index = authors_sale_number.index(max_sale_number)
        print(authors_in_period[index])

    def most_selling_genre_for_period(self, start_date, finish_date):
        print(f"The most selling genre for period {start_date} - {finish_date}:")
        found_books = False
        genres_in_period = []
        for sale in self.book_shop.sales_manager.sales:
            if start_date <= sale.sale_date <= finish_date:
                genres_in_period.append(sale.book.genre)
                found_books = True
        if not found_books:
            print("No books in this period.")
            return
        genres_sale_number = [genres_in_period.count(g) for g in genres_in_period]
        max_sale_number = max(genres_sale_number)
        index = genres_sale_number.index(max_sale_number)
        print(genres_in_period[index])


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

    def best_selling_book_for_period(self, start_date, finish_date):
        with open(f"best selling book in period : {start_date} - {finish_date}", "w+") as f:
            f.write(f"Best selling book for period: {start_date} - {finish_date} :\n".title())
            found_books = False
            books_in_period = []
            for sale in self.book_shop.sales_manager.sales:
                if start_date <= sale.sale_date <= finish_date:
                    books_in_period.append(sale.book.title)
                    found_books = True
            if not found_books:
                f.write("No books in period.")
                return
            books_sale_number = [books_in_period.count(b) for b in books_in_period]
            max_sale_number = max(books_sale_number)
            index = books_sale_number.index(max_sale_number)
            f.write(books_in_period[index])

    def most_successful_employee_for_period(self, start_date, finish_date):
        with open(f"most successful employee for period {start_date} - {finish_date}", "w+") as f:
            f.write(f"The most successful employee for period {start_date} - {finish_date} :\n".title())
            found_employees = False
            employees_in_period = []
            for sale in self.book_shop.sales_manager.sales:
                if start_date <= sale.sale_date <= finish_date:
                    employees_in_period.append(sale.employee)
                    found_employees = True
            if not found_employees:
                f.write("No employees in period.")
                return
            employees_sale_number = [employees_in_period.count(e) for e in employees_in_period]
            max_sale_number = max(employees_sale_number)
            index = employees_sale_number.index(max_sale_number)
            f.write(employees_in_period[index].get_data())

    def total_money_for_period(self, start_date, finish_date):
        with open(f"total money for period {start_date} - {finish_date}", "w+") as f:
            f.write(f"Total earned money for period {start_date} - {finish_date} :\n".title())
            found_sales = False
            sales_in_period = []
            for sale in self.book_shop.sales_manager.sales:
                if start_date <= sale.sale_date <= finish_date:
                    sales_in_period.append(sale.real_price)
                    found_sales = True
            if not found_sales:
                f.write("No sales in period.")
                return
            total_money = sum(sales_in_period)
            f.write(f"{total_money}$")

    def most_selling_author_for_period(self, start_date, finish_date):
        with open(f"most selling author for period {start_date} - {finish_date}", "w+") as f:
            f.write(f"The most selling book-author for period {start_date} - {finish_date} :\n".title())
            found_book = False
            authors_in_period = []
            for sale in self.book_shop.sales_manager.sales:
                if start_date <= sale.sale_date <= finish_date:
                    authors_in_period.append(sale.book.author)
                    found_book = True
            if not found_book:
                f.write("No books in period.")
                return
            authors_sale_number = [authors_in_period.count(a) for a in authors_in_period]
            max_sale_number = max(authors_sale_number)
            index = authors_sale_number.index(max_sale_number)
            f.write(authors_in_period[index])

    def most_selling_genre_for_period(self, start_date, finish_date):
        filename = f"most_selling_genre_{start_date}_{finish_date}.txt"
        with open(filename, "w+", encoding="utf-8") as f:
            f.write(f"The most selling genre for period {start_date} - {finish_date}:\n".title())
            found_books = False
            genres_in_period = []
            for sale in self.book_shop.sales_manager.sales:
                if start_date <= sale.sale_date <= finish_date:
                    genres_in_period.append(sale.book.genre)
                    found_books = True
            if not found_books:
                f.write("No books in this period.\n")
                return
            genres_sale_number = [genres_in_period.count(g) for g in genres_in_period]
            max_sale_number = max(genres_sale_number)
            index = genres_sale_number.index(max_sale_number)
            f.write(genres_in_period[index])


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

    book = Book("Python Basics", 2025, "Maksym K", "Educative", 10, 20)
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
    sale3 = Sale(emp1, book, "2025-02-03", 20.0)
    sales_manager.add_sale(sale1)
    sales_manager.add_sale(sale2)
    sales_manager.add_sale(sale3)

    reporter = Reporter(shop)
    file_reporter = reporter.get_reporter("file")
    console_reporter = reporter.get_reporter("console")
    
    console_reporter.most_selling_genre_for_period("2025-02-01", "2025-02-05")
    file_reporter.most_selling_genre_for_period("2025-02-01", "2025-02-05")
