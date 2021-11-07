from peewee import *
import datetime

db = MySQLDatabase('library_', user='root', password='', host='localhost', port=3306)  # Create DB By MySQL


# -------- Rules ^_^ ----------
# If Field is Mandatory ==> Set Default Value [ as Title in Books Table ]
# Make Choices : variable_Choices = ((Value Which Store In Database... Will Number, Value Which Appear To User))
# In Data Base THe Value Which Store In Database ==> Will Number ==> To Make The Database Smaller, To Make Handle With It Easy

class Publisher(Model):
    name = CharField(unique=True)  # Because We Will Handle Justtt With Name So We prevent its value
    location = CharField(null=True)

    class Meta:
        database = db


class Author(Model):
    name = CharField(unique=True)
    location = CharField(null=True)

    class Meta:
        database = db


class Category(Model):
    category_name = CharField(unique=True)
    parent_category = IntegerField(null=True)  # Recursive Relationship: It Make Relationship With Itself

    class Meta:
        database = db


class Branch(Model):
    name = CharField()
    code = CharField(null=True, unique=True)
    location = CharField(null=True)

    class Meta:
        database = db


BOOKS_STATUS = (
    (0, 'New'),
    (1, 'Used'),
    (2, 'Damaged')
)


class Books(Model):
    # CharField(null=False) = CharField()  ^_*
    title = CharField(null=False, unique=True)
    # CharField:Because The title is Short Text null=False Because This Field is {Mandatory: Mean Not Accept Null Value}
    # unique=True :  To prevent its value from being repeated ^_*

    description = TextField(null=True)
    # Because The description is Long Text,, null=True Because This Field is {Optional: Mean Accept Null Value}

    category = ForeignKeyField(Category, backref='category', null=True)
    # That Mean : This Field Have Relationship With Category Table,, and The The Name This Field Which Appear Be(backref Parameter) is 'category'

    code = CharField(null=True)  # This Field Will Specific it Value Automatically [ By Code ],, (Not By User)
    barcode = CharField(null=True)
    # parts =

    part_order = IntegerField(null=True)
    price = DecimalField(null=True)
    publisher = ForeignKeyField(Publisher, backref='publisher', null=True)
    author = ForeignKeyField(Author, backref='author', null=True)

    image = CharField(null=True)
    # Maybe Will Be Link # Very Important Notice ^_* : If Want To Put The Image Itself (Not Link Image)in DB => DB Will Be Very Big & Heavy & Slow,,,So The images Will Exist In Folder.. To Copy it Link In DB When I Rent it
    status = CharField(choices=BOOKS_STATUS)  # Choices
    date = DateTimeField(
        default=datetime.datetime.now)  # To Contain The Date With Time (Not Only Date) To Can Do Sort It

    class Meta:
        database = db


class Clients(Model):
    name = CharField()
    email = CharField(null=True, unique=True)
    # No Specific Field For Email So You Can Make sure From Text If Email Or Not By Code ^_^
    # unique=True : To prevent its value from being repeated Justtt If Was To Same User^_*

    phone = CharField(null=True)
    # Not IntegerField() Because If User Append "+" => Tht Make Error Soooo Even Make sure From Text If phone Or Not By Code ^_^

    date = DateTimeField(default=datetime.datetime.now)  # it Value Automatically From DateTime From System
    national_id = IntegerField(null=True, unique=True)

    class Meta:
        database = db


class Employee(Model):
    name = CharField()
    email = CharField(null=True, unique=True)
    phone = CharField(null=True)
    date = DateTimeField(default=datetime.datetime.now)
    national_id = IntegerField(null=True, unique=True)
    periority = IntegerField(null=True)
    # password = CharField()
    # branch = CharField()

    class Meta:
        database = db


PROCESS_TYPE = (
    (1, 'Rent'),
    (2, 'Retrieve')
)


class Daily_movements(Model):
    book = ForeignKeyField(Books, backref='daily_book')
    client = ForeignKeyField(Clients, backref='book_client')
    type = CharField(choices=PROCESS_TYPE)  # rent or retrieve
    date = DateTimeField(default=datetime.datetime.now)
    branch = ForeignKeyField(Branch, backref='daily_branch', null=True)  # Will Make It Automatically,,
    book_from = DateField(null=True)  # It Optional Because In Retrieve Case ,,Not Need To TO Specific from ___ To ____
    book_to = DateField(null=True)
    employee = ForeignKeyField(Employee, backref='daily_employee', null=True)

    class Meta:
        database = db


ACTIONS_TYPE = (
    (1, 'Login'),
    (2, 'Update'),
    (3, 'Create'),
    (4, 'Delete')
)
TABLE_CHOICES = (
    (1, 'Books'),
    (2, 'Clients'),
    (3, 'Employee'),
    (4, 'Category'),
    (5, 'Branch'),
    (6, 'Daily Movements'),
    (7, 'History'),
    (8, 'Publisher')
)


class History(
    Model):  # This Table Will Mandatory ==> Will Performed Automatically By Code ,,[ Store Actions Automatically ]
    employee = ForeignKeyField(Employee, backref='history_employee')
    action = CharField(choices=ACTIONS_TYPE)  # Choices
    table = CharField(choices=TABLE_CHOICES)  # Choices
    date = DateField(default=datetime.datetime.now)
    branch = ForeignKeyField(Branch, backref='history_branch')

    class Meta:
        database = db


db.connect()
db.create_tables([Category, Branch, Publisher, Author, Books, Clients, Employee, Daily_movements, History])
db.close()
