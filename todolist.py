# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
import calendar
import sys

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column('id', Integer, primary_key=True)
    string_field = Column('task', String, default='default_value')
    date_field = Column('deadline', Date, default=datetime.today().date())

    def __repr__(self):
        return self.string_field

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def get_day(day):
    return calendar.day_name[day]

while True:
    print('''1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit''')
    choice = int(input())

    if choice == 0:
        break
    elif choice == 1:
        today = datetime.today().date()
        rows = session.query(Table).filter(Table.date_field == today).all()
        if len(rows) == 0:
            print(f'\nToday {today.strftime("%d %b")}:\nNothing to do!\n')
        else:
            print(f'\nToday {today.strftime("%d %b")}:')

            for i, v in enumerate(rows):
                print(f'{i + 1}. {v.string_field}')
            print()
    elif choice == 2:
        deadline = datetime.today().date()
        for i in range(7):
            rows = session.query(Table).filter(Table.date_field == deadline).all()
            if len(rows) == 0:
                print(f'\n{get_day(deadline.weekday())} {deadline.strftime("%d %b")}:\nNothing to do!')
            else:
                print(f'\n{get_day(deadline.weekday())} {deadline.strftime("%d %b")}:')

                for i, v in enumerate(rows):
                    print(f'{i + 1}. {v.string_field}')
            deadline += timedelta(days=1)
        print()
    elif choice == 3:
        rows = session.query(Table).order_by(Table.date_field).all()
        print('\nAll tasks:')
        if len(rows) == 0:
            print('Nothing to do!')
        else:
            for i, v in enumerate(rows):
                print(f'{i + 1}. {v.string_field}. {v.date_field.strftime("%d %b")}')
        print()
    elif choice == 4:
        rows = session.query(Table).filter(Table.date_field < datetime.today()).order_by(Table.date_field).all()
        print('Missed tasks:')
        if len(rows) == 0:
            print('Nothing is missed!')
        else:
            for i, v in enumerate(rows):
                print(f'{i + 1}. {v.string_field}. {v.date_field.strftime("%d %b")}')
        print()
    elif choice == 5:
        task = input('Enter task\n')
        deadline = input('Enter deadline\n')
        try:
            deadline = datetime.strptime(deadline, '%Y-%m-%d')
        except:
            print('error: invalid date format')
            sys.exit()

        table = Table()
        table.string_field = task
        table.date_field = deadline

        session.add(table)
        session.commit()

        print('The task has been added!\n')
    elif choice == 6:
        rows = session.query(Table).all()
        if len(rows) == 0:
            print('Nothing to delete\n')
        else:
            print('Chose the number of the task you want to delete:\n')
            for i, v in enumerate(rows):
                print(f'{i + 1}. {v.string_field}. {v.date_field.strftime("%d %b")}')

            delete_task = int(input())
            session.delete(rows[delete_task - 1])
            session.commit()
            print('The task has been deleted!\n')
    else:
        continue

print('Bye!')
session.close()
