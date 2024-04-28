from requests import get, post

print(post('http://127.0.0.1:5000/api/jobs/1', json={'team_leader': 1, "job": "НЕругаться за списывание",
                                                   "work_size": 10 ** 10, "content": "НЕнужно НИКОГДА ругаться",
                                                   "collaborators": "", "is_finished": True, "categories": 2}))

print(post('http://127.0.0.1:5000/api/jobs/1000', json={}).json())
# пустой запрос + работы с таким id нет

print(post('http://127.0.0.1:5000/api/jobs/1', json={'team_leader': "1", "job": "Ругаться за списывание",
                                                   "work_size": 10 ** 10, "content": "Нужно иногда ругаться чтоб не втыкали",
                                                   "collaborators": None, "is_finished": "False", "categories": 1}).json())
# некорректные данные

print(get('http://127.0.0.1:5000/api/jobs').json())



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
