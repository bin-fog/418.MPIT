# Для любого пользователя
## /auth
Вход в аккаунт

    INPUT: username: str, password: str
    OUTPUT: Successful


## /register
Регистрация пользователя

    INPUT: username: str, password: str, name: str, surname: str, birthday: str, city: str
    OUTPUT: Successful

## /tasks
Отображение списка всех задач

    OUTPUT: [{id, title, description, company, reward, is_completed}]

# Для авторизированного пользователя
## /logout
Выход пользователя из аккаунта

    OUTPUT: Successful


## /profile
Просмотр данных своего профиля

    OUTPUT: {username, name, surname, patronymic, city, coins, birthday}


## /change-my-profile
Изменение одного или нескольких параметров своего профиля

    INPUT: name: str | None, surname: str | None, patronymic: str | None, city: str | None, birthday: str | None
    OUTPUT: Successful


## /add-to-tasks
Добавление задачи в свой список выполнения (то, над чем пользователь работает)

    INPUT: task_id: int
    OUTPUT: Successful


## /get-my-tasks
Получение списка задач пользователя (завершённые и незавершённые)    

    INPUT: get_my_tasks
    OUTPUT: {"todo","completed"}


# Для админа
## /add-money
Добавляет (или убавляет) деньги определённому пользователю

    INPUT: count: int, recipient_username: str
    OUTPUT: Successful


## /add-task
Добавляет новую задачу

    INPUT: title: str, description: str, reward: str, logo_url: str
    OUTPUT: Successful


## /finish-task
Помечает задачу как "неактивная" (прошедшая)

    INPUT: task_id: int
    OUTPUT: Successful


## /remove-task
Удаляет задачу полностью (в случае, если задачу не нужно хранить в архиве)

    INPUT: task_id: int
    OUTPUT: Successful

## /add-product
Добавляет товар

    INPUT: title: str, description: str, price: int, remained: int, image_url: int,
    OUTPUT: Sucessful

## /remove-product
Удаляет товар

    INPUT: product_id: int
    OUTPUT: Successful