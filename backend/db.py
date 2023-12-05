from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Base, Event


class database:
    def __init__(self, connection: str):
        self.engine = create_engine(connection, echo=True)
        self.session = Session(self.engine)

    def create_db(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def get_events(self):
        result = self.session.execute(select(Event)).fetchall()
        print(result)
        for i in range(len(result)):
            if i is not None:
                print(i)
                result[i] = {"title": result[i].title, "description": result[i].description,
                             "company": result[i].company, "address": result[i].address, "datetime": result[i].datetime}
        return result
