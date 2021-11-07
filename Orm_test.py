from peewee import *

# If The Database Not Exist In This Folder ,,, Automatically Program Will Create Data Base
# Very Important Notice ^_^ :  If You pen Database ,, The Program Will Give Error ,, So You must Cloe The DB To Craete Tables Corectly
# db = SqliteDatabase('people.db')
db = MySQLDatabase('test',user='root', password='',
                         host='localhost')  # Create DB By MySQL
# pg_db = PostgresqlDatabase('my_app', user='localhost', password="root",
                           #host='localhost', port=5432)  # Create DB By MySQL ,, Same The Function [ MySQLDatabase ],,,, Error

class Person(Model):
    name = CharField()  # Because The Name Is String So Use CharField()
    birthday = DateField()  # Because The birthday Is Date So Use DateField()

    class Meta:
        database = db  #This Is Mean :This Class belongs To db # This model uses the "people.db" database

class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')  # That Mean Pet Class Have Relationship With Person Class
    # ForeignKeyField => Use It To Make Relationship between 2 Classes(2 Tables)
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db # this model uses the "people.db" database

'''class Pupils(Model):
    level = DecimalField()
    name = CharField()
    class Meta:
        database = pg_db

class Lesoons(Model):
    math = CharField()
    arabic = CharField()

    class Meta:
        database = pg_db'''


db.connect()
#pg_db.connect()
db.create_tables([Person, Pet])  # Here Put The Names Of Table Which I want To Create In Database,, Every Table Not Exist Here ,,Will Not Create
#Very Important Notice ^_^ : Must Order THe Tables inFunction
#pg_db.create_tables([Pupils, Lesoons])



