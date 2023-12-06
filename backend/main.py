import uvicorn
from db import database
from models import User, AuthKey, Task
from fastapi import FastAPI, Response, Cookie, Request
from config import DB_TOKEN
from sqlalchemy import Sequence
from _md5 import md5

app = FastAPI()
db = database(DB_TOKEN)


# db.create_db()


@app.get("/auth")
async def auth(username: str, password: str, response: Response, request: Request):
    user = db.session.get(User, username)
    if user is None:
        return "Does not exist"
    if user.password_hash == md5(password.encode()).hexdigest():
        auth_key = AuthKey(username=user.username, ip=request.client.host,
                           num=db.session.execute(Sequence("authkeys_num_seq")))
        response.set_cookie(key="auth_key", value=auth_key.content, max_age=604800)
        response.set_cookie(key="username", value=f"{username}", max_age=604800)
        db.session.add(auth_key)
        db.session.commit()
        return "Successful"
    else:
        return "Invalid password"


@app.get("/permissions")
async def verify(auth_key: str | None = Cookie(default=None), username: str | None = Cookie(default=None)):
    if auth_key is None or username is None:
        return "You are not logged in"
    key = db.get_auth(auth_key)
    user = db.session.get(User, key.username)
    if key is None:
        return "Invalid cookie"
    if key.username == username:
        return user


@app.get("/events")
async def events():
    return db.get_events()


@app.get("/register")
async def register(username: str, password: str, name: str, surname: str, birthday: str, city: str,
                   response: Response, request: Request, patronymic: str = ""):
    if db.session.get(User, username) is not None:
        return "Already exists"
    db.session.add(User(username=username, password_hash=md5(password.encode()).hexdigest(), name=name, surname=surname,
                        patronymic=patronymic,
                        birthday=birthday, city=city))
    db.session.commit()
    auth_key = AuthKey(username=username, ip=request.client.host, num=db.session.scalar(Sequence("authkeys_num_seq")))
    response.set_cookie(key="auth_key", value=auth_key.content, max_age=604800)
    response.set_cookie(key="username", value=f"{username}", max_age=604800)
    db.session.add(auth_key)
    db.session.commit()
    return "Successful"


@app.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="auth_key")
    response.delete_cookie(key="username")
    return "Successful"


@app.get("/profile")
async def profile(auth_key: str | None = Cookie(default=None),
                  username: str | None = Cookie(default=None)):
    user = await verify(auth_key, username)
    if type(user) is str:
        return user
    return {"username": user.username, "name": user.name, "surname": user.surname, "patronymic": user.patronymic,
            "city": user.city, "coins": user.coins, "birthday": user.birthday}


@app.get("/change-my-profile")
async def change_my_profile(name: str | None = None, surname: str | None = None, patronymic: str | None = None,
                            city: str | None = None, birthday: str | None = None,
                            auth_key: str | None = Cookie(default=None), username: str | None = Cookie(default=None)):
    user = await verify(auth_key, username)
    if type(user) is str:
        return user
    if name is not None:
        user.name = name
    if surname is not None:
        user.surname = surname
    if patronymic is not None:
        user.patronymic = patronymic
    if city is not None:
        user.city = city
    if birthday is not None:
        user.birthday = birthday
    db.session.commit()
    return "Successful"


@app.get("/add-money")
async def add_money(count: int, recipient_username: str, auth_key: str | None = Cookie(default=None),
                    username: str | None = Cookie(default=None)):
    user = await verify(auth_key, username)
    if type(user) is str:
        return user
    if user.access_level == 0:
        return "You don't have rights to manage coins"
    user = db.session.get(User, recipient_username)
    user.coins += count
    db.session.commit()
    return "Successful"


@app.get("/add-task")
async def add_task(title: str, description: str, reward: str, logo_url: str, auth_key: str | None = Cookie(default=None),
                   username: str | None = Cookie(default=None)):
    user = await verify(auth_key, username)
    if type(user) is str:
        return user
    if user.access_level == 0:
        return "You don't have rights to manage tasks"
    company = user.company
    db.session.add(Task(title=title, description=description, reward=reward, logo_url=logo_url, company=company,
                        completed=0))
    db.session.commit()
    return "Successful"


@app.get("/remove-task")
async def remove_task(task_id: int, auth_key: str | None = Cookie(default=None),
                      username: str | None = Cookie(default=None)):
    user = await verify(auth_key, username)
    if type(user) is str:
        return user
    if user.access_level == 0:
        return "You don't have rights to manage tasks"
    task = db.session.get(Task, task_id)
    if task.company != user.company:
        return "You can't modify tasks from other companies"
    db.session.delete(task)
    db.session.commit()
    return "Successful"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
