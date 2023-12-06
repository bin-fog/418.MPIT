from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Date, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from _md5 import md5
from datetime import date, datetime
from typing import Optional

class Base(DeclarativeBase):
    pass


class Company(Base):
    __tablename__ = "companies"
    # Login data
    code_title: Mapped[str] = mapped_column(String(16), primary_key=True)  # Код.Название
    password_hash: Mapped[str] = mapped_column(String(32))  # Хэш пароля

    # Information
    title: Mapped[str] = mapped_column(String(64))  # Название компании
    description: Mapped[str] = mapped_column(String(512))  # Описание компании
    logo_url: Mapped[str] = mapped_column(String(64))  # Ссылка на логотип

    # Preview
    def __repr__(self) -> str:
        return (f"Company(code_title={self.code_title!r}, title={self.title!r}, description={self.description!r}, "
                f"logo_url={self.logo_url!r})")


class User(Base):
    __tablename__ = "users"
    # Login data
    username: Mapped[str] = mapped_column(String(16), primary_key=True)  # Уникальное имя
    password_hash: Mapped[str] = mapped_column(String(32))  # Хэш пароля

    # Information
    name: Mapped[str] = mapped_column(String(16), default="")  # Имя
    surname: Mapped[str] = mapped_column(String(20), default="")  # Фамилия
    patronymic: Mapped[str] = mapped_column(String(24), default="")  # Отчество
    birthday: Mapped[str] = mapped_column(Date(), default="")  # Дата рождения
    city: Mapped[str] = mapped_column(String(20), default="")  # Город

    # Reward
    coins: Mapped[int] = mapped_column(Integer(), default=0)  # Монеты
    achievements: Mapped[str] = mapped_column(String(), default="")  # Достижения

    # Administration
    access_level: Mapped[int] = mapped_column(Integer(), default=0)  # Уровень доступа (пользователь, админ)
    company: Mapped[Optional[str]] = mapped_column(ForeignKey(Company.code_title))  # Компания на которую работает админ

    # Preview
    def __repr__(self) -> str:
        return (f"User(username={self.username!r}, name={self.surname + ' ' + self.name + ' ' + self.patronymic!r}, "
                f"birthday={self.birthday!r}, city={self.city!r}, coins={self.coins!r}, "
                f"achievements={self.achievements!r})")


class Achievement(Base):
    __tablename__ = "achievements"
    # ID
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)  # Идентификатор
    # Information
    title: Mapped[str] = mapped_column(String(32))  # Название
    description: Mapped[str] = mapped_column(String(256))  # Описание
    company: Mapped[str] = mapped_column(ForeignKey(Company.code_title))  # Название компании

    # Preview
    def __repr__(self) -> str:
        return (f"Achievement(id={self.id!r}, title={self.title!r}, description={self.description!r}, "
                f"company={self.company!r})")


class Event(Base):
    __tablename__ = "events"
    # ID
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)  # Идентификатор
    # Information
    title: Mapped[str] = mapped_column(String(32))  # Название
    description: Mapped[str] = mapped_column(String(256))  # Описание
    company: Mapped[str] = mapped_column(ForeignKey(Company.code_title))  # Название компании
    address: Mapped[str] = mapped_column(String(64))  # Место проведения
    datetime: Mapped[datetime] = mapped_column(DateTime())  # Дата и время проведения

    # Preview
    def __repr__(self) -> str:
        return (f"Event(id={self.id!r}, title={self.title!r}, description={self.description!r}, "
                f"company={self.company!r}), datetime={self.datetime}, address={self.address}")


class Task(Base):
    __tablename__ = "tasks"
    # ID
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)  # Идентификатор
    # Information
    title: Mapped[str] = mapped_column(String(32))  # Название
    description: Mapped[str] = mapped_column(String(256))  # Описание
    company: Mapped[str] = mapped_column(ForeignKey(Company.code_title))  # Название компании
    reward: Mapped[int] = mapped_column(Integer())  # Награда
    logo_url: Mapped[str] = mapped_column(String(64))  # Ссылка на лого
    completed: Mapped[bool] = mapped_column(Boolean())

    # Preview
    def __repr__(self) -> str:
        return (f"Event(id={self.id!r}, title={self.title!r}, description={self.description!r}, "
                f"company={self.company!r}), datetime={self.datetime}, address={self.address}")


class Product(Base):
    __tablename__ = "products"
    # ID
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)  # Идентификатор
    # Information
    title: Mapped[str] = mapped_column(String(32))  # Название
    description: Mapped[str] = mapped_column(String(256))  # Описание
    company: Mapped[str] = mapped_column(ForeignKey(Company.code_title))  # Название компании
    remained: Mapped[int] = mapped_column(Integer(), default=0)  # Сколько осталось на складе
    # Image
    image_url: Mapped[str] = mapped_column(String(128))  # Ссылка на изображение

    # Preview
    def __repr__(self) -> str:
        return (f"Product(id={self.id!r}, title=\"{self.title!r}\", description=\"{self.description!r}\", "
                f"remained={self.remained!r}, image_url=\"{self.image_url!r}\", company={self.company})")


class AuthKey(Base):
    __tablename__ = "authkeys"
    # Information
    num: Mapped[int] = mapped_column(primary_key=True)  # Идентификатор связи
    ip: Mapped[str] = mapped_column(String())
    username: Mapped[str] = mapped_column(ForeignKey(User.username))  # Имя пользователя
    content: Mapped[str] = mapped_column(String(64))  # Содежимое
    created: Mapped[str] = mapped_column(Date())  # Дата создания

    # Content generator
    def __init__(self, num: int, username: str, ip: str, account_type: int = 0):
        self.content = md5(str(num).encode()).hexdigest() + md5(str(username).encode()).hexdigest()
        super().__init__(num=num, username=username, created=date.today().isoformat(), ip=ip)

    # Preview
    def __repr__(self) -> str:
        return (f"AuthKey(num={self.num!r}, username={self.username!r}, content={self.content!r}, "
                f"ip={self.ip!r})")
