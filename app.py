from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'asdfaslkdjfladlfjk1lk23jlk12'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __repr__(self):
        return f'add success <{self.name}>'

# session


def session_fun():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

# home


@app.route('/')
def home():
    return redirect(url_for('login'))

# login page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form.get('password')

        users = User.query.all()
        login_value = []
        for user in users:
            if user.name == name and user.password == password:
                result = 'success'
                login_value.append(result)
            else:
                result = 'failed'
                login_value.append(result)

        if 'success' in login_value:
            session['username'] = name
            session.permanent = True
            if name == 'admin':
                return redirect(url_for('index'))
            else:
                message = User.query.filter_by(name=name).first()
                return render_template('detail.html', message=message)
        else:
            return render_template('login.html', error='⚠Username or Passowrd is Error!')

    return render_template('login.html')

# all users info


@app.route('/index')
def index():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    students = User.query.all()
    return render_template('index.html', students=students)


@app.route('/create', methods=['GET', 'POST'])
def create():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        users = User.query.all()
        user_li = []
        email_li = []
        for user in users:
            user_li.append(user.name)
            email_li.append(user.email)

        if name in user_li or email in email_li:
            return render_template('create.html', error='⚠Username or Email is Exist.')

        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/detail/<int:id>')
def detail(id):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    message = User.query.get_or_404(id)
    return render_template('detail.html', message=message)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    user = User.query.get_or_404(id)
    if request.method == "POST":
        user.name = request.form.get('name')
        user.email = request.form.get('email')
        user.password = request.form.get('password')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', user=user)


@app.route('/delete/<int:id>')
def delete(id):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/del_session')
def del_session():
    session.pop('username')
    return 'del_session'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, ssl_context=(
        'ssl/server.crt', 'ssl/server.key'))
