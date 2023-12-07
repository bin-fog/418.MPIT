import uvicorn
from db import database
from models import User, AuthKey, Task, Product
from fastapi import FastAPI, Response, Cookie, Request
from config import DB_TOKEN
from sqlalchemy import Sequence
from _md5 import md5
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
db = database(DB_TOKEN)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# db.create_db()


# TODO: company management
# TODO: task doing (Main)


# Account manager
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


@app.get("/verify")
async def verify(auth_key: str | None = Cookie(default=None), username: str | None = Cookie(default=None)):
    if auth_key is None or username is None:
        return "You are not logged in"
    key = db.get_auth(auth_key)
    user = db.session.get(User, key.username)
    if key is None:
        return "Invalid cookie"
    if key.username == username:
        return user


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


# Profile manager
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


# User task management
@app.get("/add-to-tasks")
async def add_to_tasks(task_id: int, auth_key: str | None = Cookie(default=None),
                       username: str | None = Cookie(default=None)):
    user = await verify(auth_key, username)
    if type(user) is str:
        return user
    print(user.tasks.split("\t"))
    todo, completed = user.tasks.split("\t")
    user.tasks = " ".join(todo.split() + [str(task_id)]) + "\t" + completed
    db.session.commit()
    return "Successful"


@app.get("/get-my-tasks")
async def get_my_tasks(auth_key: str | None = Cookie(default=None), username: str | None = Cookie(default=None)):
    user = await verify(auth_key, username)
    if type(user) is str:
        return user
    print(user.tasks.split("\t"))
    todo, completed = user.tasks.split("\t")
    todo, completed = list(map(int, todo.split())), list(map(int, completed.split()))
    return {"todo": todo, "completed": completed}


# Money manager
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


# Task manager
@app.get("/tasks")
async def events():
    return db.get_tasks()


@app.get("/add-task")
async def add_task(title: str, description: str, reward: str, logo_url: str,
                   auth_key: str | None = Cookie(default=None),
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


@app.get("/finish-task")
async def finish_task(task_id: int, auth_key: str | None = Cookie(default=None),
                      username: str | None = Cookie(default=None)):
    user = await verify(auth_key, username)
    if type(user) is str:
        return user
    if user.access_level == 0:
        return "You don't have rights to manage tasks"
    task = db.session.get(Task, task_id)
    if task.company != user.company:
        return "You can't modify tasks from other companies"
    task.is_completed = True
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


# найти пользователей, подписавшихся на задание
@app.get("/users-on-task")
async def users_on_task(task_id: int, auth_key: str | None = Cookie(default=None),
                        username: str | None = Cookie(default=None)):
    user = await verify(auth_key, username)
    if type(user) is str:
        return user
    if user.access_level == 0:
        return "You don't have rights to manage tasks"
    print(db.get_users_on_task(task_id))
    return "Successful"


# отметить, что посетил
@app.get("/mark-user")
async def mark_user(task_id: int, user_name: str, auth_key: str | None = Cookie(default=None),
                    username: str | None = Cookie(default=None)):
    user = await verify(auth_key, username)
    if type(user) is str:
        return user
    if user.access_level == 0:
        return "You don't have rights to manage tasks"
    muser = db.session.get(User, user_name)
    todo, completed = muser.tasks.split("\t")
    todo = todo.split()
    if str(task_id) in todo:
        todo.remove(str(task_id))
    todo = " ".join(todo)
    completed += " " + str(task_id)
    muser.tasks = todo + "\t" + completed
    db.session.commit()
    return "Successful"


# Products
@app.get("/products")
async def products():
    return db.get_products()


@app.get("/add-product")
async def add_product(title: str, description: str, price: int, remained: int, image_url: int,
                      auth_key: str | None = Cookie(default=None), username: str | None = Cookie(default=None)):
    user = await verify(auth_key, username)
    if type(user) is str:
        return user
    if user.access_level == 0:
        return "You don't have rights to manage products"
    company = user.company
    db.session.add(Product(title=title, description=description, company=company,
                           price=price, remained=remained, image_url=image_url))
    db.session.commit()
    return "Successful"


@app.get("/remove-product")
async def remove_product(product_id: int, auth_key: str | None = Cookie(default=None),
                         username: str | None = Cookie(default=None)):
    user = await verify(auth_key, username)
    if type(user) is str:
        return user
    if user.access_level == 0:
        return "You don't have rights to manage products"
    product = db.session.get(Product, product_id)
    if product.company != user.company:
        return "You can't modify tasks from other companies"
    db.session.delete(product)
    db.session.commit()
    return "Successful"


# Run manager
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
