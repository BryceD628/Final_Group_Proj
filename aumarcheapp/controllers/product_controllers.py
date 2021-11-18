from flask import render_template,redirect,session,request, flash
from aumarcheapp import app
from aumarcheapp.models.product import Product
from aumarcheapp.models.user import User


@app.route('/new/product')
def new_product():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_product.html',user=User.get_by_id(data))


@app.route('/create/product',methods=['POST'])
def create_product():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Product.validate_product(request.form):
        return redirect('/home')
    data = {
        "product_title" : request.form['product_title'],
        "description" : request.form['description'],
        "category" : request.form['category'],
        "size" : request.form['size'],
        "materials" : request.form['materials'],
        "price" : request.form['price'],
        "images" : request.form['images'],
        "video" : request.form['video'],
        "quantity" : request.form['quantity'],
        "notes" : request.form['notes'],
        "user_id" : session["user_id"],
    }
    Product.save(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit_product(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit.html",product=Product.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/product',methods=['POST'])
def update_product():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Product.validate_product(request.form):
        return redirect('/edit/<int:id>')
    data = {
        "product_title" : request.form['product_title'],
        "description" : request.form['description'],
        "category" : request.form['category'],
        "size" : request.form['size'],
        "materials" : request.form['materials'],
        "price" : request.form['price'],
        "images" : request.form['images'],
        "video" : request.form['video'],
        "quantity" : request.form['quantity'],
        "notes" : request.form['notes'],
        "user_id" : session["user_id"],
        "id": request.form['id'],
    }
    Product.update(data)
    return redirect('/dashboard')


@app.route('/show/<int:id>')
def show(id):
    from datetime import datetime 
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }  
    return render_template('show.html', user=User.get_by_id(user_data), product = Product.get_one_complete(data))

@app.route('/user/account')
def myaccount():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id":session['user_id']
    }  
    return render_template('myaccount.html', user=User.get_by_id(user_data), allproducts = Product.get_all_complete(user_data))


@app.route('/destroy/product/<int:id>')
def destroy_product(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Product.destroy(data)
    return redirect('/user/account')