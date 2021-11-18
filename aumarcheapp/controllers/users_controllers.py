from flask import render_template,redirect,session,request, flash
from aumarcheapp import app
from aumarcheapp.models.user import User
from aumarcheapp.models.product import Product
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "company":request.form['company'],
        "jobtitle": request.form['jobtitle'],
        "email": request.form['email'],
        "phonenumber": request.form['phonenumber'],
        "website": request.form['website'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/home')

@app.route('/login',methods=['POST'])
def login():
    if not User.validate_login_email(request.form):
        return redirect('/')
    user = User.get_by_email(request.form)
    session['user_id'] = user.id
    return redirect('/home')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("home.html",user=User.get_by_id(data))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html",user=User.get_by_id(data),products=Product.get_all_products())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/update',methods=['POST'])
def update_user():
    if 'user_id' not in session:
        return redirect('/logout')
    if not User.validate_edit(request.form):
        return redirect('/user/account')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "company":request.form['company'],
        "jobtitle": request.form['jobtitle'],
        "email": request.form['email'],
        "phonenumber": request.form['phonenumber'],
        "website": request.form['website'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    Product.update(data)
    return redirect('/')

#password not working