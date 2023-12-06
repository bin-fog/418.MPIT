from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Base, Event, AuthKey, Task


class database:
    def __init__(self, connection: str):
        self.engine = create_engine(connection)
        self.session = Session(self.engine)

    def create_db(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def get_events(self):
        result = list(map(lambda x: x[0], self.session.execute(select(Event)).fetchall()))
        for i in range(len(result)):
            result[i] = {"title": result[i].title, "description": result[i].description,
                         "company": result[i].company, "address": result[i].address, "datetime": result[i].datetime}
        return result

    def get_tasks(self):
        result = list(map(lambda x: x[0], self.session.execute(select(Task)).fetchall()))
        for i in range(len(result)):
            result[i] = {"id": result[i].id, "title": result[i].title, "description": result[i].description,
                         "company": result[i].company, "reward": result[i].reward,
                         "is_completed": result[i].is_completed}
        return result

    def get_auth(self, key):
        result = self.session.execute(select(AuthKey).where(AuthKey.content == key)).fetchone()
        if result is None:
            return None
        return result[0]
