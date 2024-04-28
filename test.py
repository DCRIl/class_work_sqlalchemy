from requests import get, post, delete

print(get('http://127.0.0.1:5000/api/v2/users'))
print(get('http://127.0.0.1:5000/api/v2/user')) # ошибка, нет такой страницы
print(get('http://127.0.0.1:5000/api/v2/user/1'))
print(get('http://127.0.0.1:5000/api/v2/user/-1')) # ошибка, нет такого id
print(get('http://127.0.0.1:5000/api/v2/user/ф')) # ошибка, не корректный id
a = {"surname": "ABA",
     "name": "CABA",
     "age": 15,
     "position": "В активном поиске",
     "speciality": "Боб строитель",
     "address": "Улица Ежёва, дом Пиражёва",
     "email": "abacaba@gmail.com",
     "city_from": "Владикавказ"}
print(post("http://127.0.0.1:5000/api/v2/users", json=a))
print(post("http://127.0.0.1:5000/api/v2/users", json={})) # ошибка, пустой запрос
print(delete("http://127.0.0.1:5000/api/v2/users/2"))
print(delete("http://127.0.0.1:5000/api/v2/users/2"))  # ошибка, пользователь уже удалён
print(delete("http://127.0.0.1:5000/api/v2/users/100"))  # ошибка, пользователя с таким id нет




# from data.db_session import create_session, global_init
# from data.category import Category
# from data.jobs import Jobs
#
# global_init("db/colonists.db")
# db_sess = create_session()
# job1 = Jobs()
# job1.team_leader = 1
# job1.job = 'deployment of residential modules 1 and 2'
# job1.work_size = 15
# job1.collaborators = '2, 3'
# job1.categories.append(db_sess.query(Category).filter(Category.id == 1).first())
# job1.is_finished = False
# db_sess.add(job1)
# db_sess.commit()
