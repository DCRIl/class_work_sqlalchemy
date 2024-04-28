from flask import Flask, render_template, redirect, request, abort
from data import db_session, jobs_api,user_api, user_resources, jobs_resources
from data.users import User
from data.jobs import Jobs
from data.department import Departments
from data.category import Category
from forms.user import RegisterForm, LoginForm
from forms.jobs import JobsForm
from forms.departments import DepartmentsForm
from forms.category import CategoryForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    print(jobs)
    return render_template("index.html", jobs=jobs)


@app.route("/users_show/<int:id>")
def show_user(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    if user:
        return render_template("user_city.html", user=user, title="Ностальгия")
    else:
        return "Пользователь не найден"


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    db_sess = db_session.create_session()
    options = db_sess.query(Category).all()
    if form.validate_on_submit():
        jobs = Jobs()
        jobs.job = form.title.data
        jobs.content = form.content.data
        jobs.collaborators = form.collaborators.data
        jobs.categories.append(db_sess.query(Category).filter(Category.name == request.form["category"]).first().id)
        jobs.is_finished = form.is_finished.data
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', title='Добавление новости',
                           form=form, option=options)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user or current_user.id == 1
                                          ).first()
        if jobs:
            form.title.data = jobs.title
            form.content.data = jobs.content
            request.form["category"] = jobs.category
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user or current_user.id == 1
                                          ).first()
        if jobs:
            jobs.title = form.title.data
            jobs.content = form.content.data
            jobs.categories = request.form["category"]
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      Jobs.user == current_user or current_user.id == 1
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/departments', methods=['GET', 'POST'])
@login_required
def departments():
    db_sess = db_session.create_session()
    deps = db_sess.query(Departments).all()
    return render_template("list_department.html", deps=deps)


@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = Departments()
        dep.title = form.title.data
        dep.chief = form.chief.data
        dep.members = form.members.data
        dep.email = form.email
        db_sess.add(dep)
        db_sess.commit()
        return redirect('/departments')
    return render_template('deps.html', title='Добавление департамента',
                           form=form)


@app.route('/department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        dep = db_sess.query(Departments).filter(Departments.id == id,
                                                Departments.user == current_user or current_user.id == 1
                                                ).first()
        if dep:
            form.title.data = dep.title
            form.chief.data = dep.chief
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = db_sess.query(Departments).filter(Departments.id == id,
                                         Departments.user == current_user or current_user.id == 1
                                         ).first()
        if dep:
            dep.title = form.title.data
            dep.chief = form.chief.data
            dep.members = form.members.data
            dep.email = form.email.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('deps.html',
                           title='Редактирование департамента',
                           form=form
                           )


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    db_sess = db_session.create_session()
    dep = db_sess.query(Departments).filter(Departments.id == id,
                                            Departments.user == current_user or current_user.id == 1
                                            ).first()
    if dep:
        db_sess.delete(dep)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        category = Category()
        category.name = form.name.data
        db_sess.add(category)
        db_sess.commit()
        return redirect('/')
    return render_template('category.html', title='Добавление категории',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")



if __name__ == '__main__':
    db_session.global_init("db/colonists.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(user_api.blueprint)
    api.add_resource(user_resources.UserListResource, '/api/v2/users')
    api.add_resource(user_resources.UserResource, '/api/v2/user/<int:id>')
    api.add_resource(jobs_resources.JobsListResource, '/api/v2/jobs')
    api.add_resource(jobs_resources.JobsResource, '/api/v2/job/<int:id>')
    app.run()
