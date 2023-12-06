import uvicorn
from db import database
from models import User, AuthKey, Admin
from fastapi import FastAPI, Response, Cookie, Request
from config import DB_TOKEN
from sqlalchemy import Sequence
from _md5 import md5

app = FastAPI()
db = database(DB_TOKEN)


db.create_db()


@app.get("/auth")
async def auth(username: str, password: str, response: Response, request: Request):
    user = db.session.get(User, username)
    admin = db.session.get(Admin, username)
    if user is None and admin is None:
        return "Does not exist"
    elif user is not None:
        if user.password_hash == md5(password.encode()).hexdigest():
            auth_key = AuthKey(username=user.username, ip=request.client.host,
                               num=db.session.execute(Sequence("authkeys_num_seq")))
            print(auth_key)
            response.set_cookie(key="auth_key", value=auth_key.content, max_age=604800)
            response.set_cookie(key="username", value=f"{username}", max_age=604800)
            db.session.add(auth_key)
            db.session.commit()
            return "Successful"
        else:
            return "Invalid password"
    elif admin is not None:
        if admin.password_hash == md5(password.encode()).hexdigest():
            auth_key = AuthKey(username=admin.username, ip=request.client.host,
                               num=db.session.execute(Sequence("authkeys_num_seq")))
            response.set_cookie(key="auth_key", value=auth_key.content, max_age=604800)
            response.set_cookie(key="username", value=f"{username}", max_age=604800)
            db.session.add(auth_key)
            db.session.commit()
            return "Successful"
        else:
            return "Invalid password"


@app.get("/permissions")
async def permissions(auth_key: str | None = Cookie(default=None), username: str | None = Cookie(default=None)):
    if auth_key is None or username is None:
        return "You are not logged in"
    key = db.get_auth(auth_key)
    if key is None:
        return "Invalid cookie"
    if key.username == username:
        return key.username, key.account_type


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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
