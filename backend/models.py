from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Date, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from _md5 import md5
from datetime import date, datetime


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
    logo_url: Mapped[str] = mapped_column()  # Ссылка на логотип

    # Preview
    def __repr__(self) -> str:
        return (f"Company(code_title={self.code_title!r}, title={self.title!r}, description={self.description!r}, "
                f"logo_url={self.logo_url!r})")


class User(Base):
    __tablename__ = "users"
    # Login data
    username: Mapped[str] = mapped_column(String(16), primary_key=True)    # Уникальное имя
    password_hash: Mapped[str] = mapped_column(String(32))    # Хэш пароля

    # Information
    name: Mapped[str] = mapped_column(String(16))    # Имя
    surname: Mapped[str] = mapped_column(String(20))    # Фамилия
    patronymic: Mapped[str] = mapped_column(String(24))    # Отчество
    birthday: Mapped[str] = mapped_column(Date())    # Дата рождения
    city: Mapped[str] = mapped_column(String(20))    # Город

    # Reward
    coins: Mapped[int] = mapped_column(Integer(), default=0)    # Монеты
    achievements: Mapped[str] = mapped_column(String(), default="")    # Достижения

    # Preview
    def __repr__(self) -> str:
        return (f"User(username={self.username!r}, name={self.surname+' '+self.name+' '+self.patronymic!r}, "
                f"birthday={self.birthday!r}, city={self.city!r}, coins={self.coins!r}, "
                f"achievements={self.achievements!r})")


class Admin(Base):
    __tablename__ = "admins"
    # Login data
    username: Mapped[str] = mapped_column(String(16), primary_key=True)    # Уникальное имя
    password_hash: Mapped[str] = mapped_column(String(32))    # Хэш пароля

    # Information
    name: Mapped[str] = mapped_column(String(16))    # Имя
    surname: Mapped[str] = mapped_column(String(20))    # Фамилия
    access_level: Mapped[int] = mapped_column()    # Уровень доступа
    company: Mapped[str] = mapped_column(ForeignKey(Company.code_title))    # Название компании

    # Preview
    def __repr__(self) -> str:
        return (f"User(username={self.username!r}, name={self.surname+' '+self.name!r}, "
                f"access_level={self.access_level!r})")


class Achievement(Base):
    __tablename__ = "achievements"
    # ID
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)    # Идентификатор
    # Information
    title: Mapped[str] = mapped_column(String(32))    # Название
    description: Mapped[str] = mapped_column(String(256))    # Описание
    company: Mapped[str] = mapped_column(ForeignKey(Company.code_title))    # Название компании

    # Preview
    def __repr__(self) -> str:
        return (f"Achievement(id={self.id!r}, title={self.title!r}, description={self.description!r}, "
                f"company={self.company!r})")


class Event(Base):
    __tablename__ = "events"
    # ID
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)    # Идентификатор
    # Information
    title: Mapped[str] = mapped_column(String(32))    # Название
    description: Mapped[str] = mapped_column(String(256))    # Описание
    company: Mapped[str] = mapped_column(ForeignKey(Company.code_title))    # Название компании
    address: Mapped[str] = mapped_column(String(64))    # Место проведения
    datetime: Mapped[datetime] = mapped_column(DateTime())  # Дата и время проведения

    # Preview
    def __repr__(self) -> str:
        return (f"Event(id={self.id!r}, title={self.title!r}, description={self.description!r}, "
                f"company={self.company!r})")


class Product(Base):
    __tablename__ = "products"
    # ID
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)    # Идентификатор
    # Information
    title: Mapped[str] = mapped_column(String(32))    # Название
    description: Mapped[str] = mapped_column(String(256))    # Описание
    company: Mapped[str] = mapped_column(ForeignKey(Company.code_title))    # Название компании
    remained: Mapped[int] = mapped_column(Integer(), default=0)    # Сколько осталось на складе
    # Image
    image_url: Mapped[str] = mapped_column(String(128))    # Ссылка на изображение

    # Preview
    def __repr__(self) -> str:
        return (f"Product(id={self.id!r}, title=\"{self.title!r}\", description=\"{self.description!r}\", "
                f"remained={self.remained!r}, image_url=\"{self.image_url!r}\", company={self.company})")


class AuthKey(Base):
    __tablename__ = "authkeys"
    # Information
    num: Mapped[int] = mapped_column(Integer(), autoincrement=True)    # Идентификатор связи
    ip: Mapped[str] = mapped_column(String())
    username: Mapped[str] = mapped_column(ForeignKey(User.username))    # Имя пользователя
    content: Mapped[str] = mapped_column(String(64), primary_key=True)    # Содежимое
    created: Mapped[str] = mapped_column(Date())    # Дата создания
    account_type: Mapped[int] = mapped_column(Integer(), default=0)    # Тип аккаунта (пользователь, админ, компания)

    # Content generator
    def __init__(self, username: str, ip: str, account_type: int = 0):
        self.content = md5(str(self.num).encode()).hexdigest() + md5(str(self.username).encode()).hexdigest()
        super().__init__(username=username, account_type=account_type, created=date.today().isoformat(), ip=ip)

    # Preview
    def __repr__(self) -> str:
        return (f"AuthKey(num={self.num!r}, username={self.username!r}, content={self.content!r}, "
                f"account_type={self.account_type!r}, ip={self.ip!r})")
