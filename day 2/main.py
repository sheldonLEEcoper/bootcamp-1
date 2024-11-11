from flask import Flask , render_template, request , redirect ,url_for
from model import *
import os
from sqlalchemy import and_

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///" + os.path.join(current_dir, 'database.sqlite3') 

db.init_app(app)
app.app_context().push()

@app.route('/', methods=['GET']) # / = http://127.0.0.1:5000/
def home():
    return render_template('home.html')




@app.route('/page1' ,  methods=['GET','POST'])
def page1():
    if request.method=="POST":
         data_username= request.form['Username']
         data_email = request.form['email']
         data_password = request.form['password']
         
         data = users.query.filter_by(email=data_email).first()
        
         if data :
            return "email already exists please use a differen email"
         else:
            new_data=users(name= data_username , email=data_email ,
                            password=data_password , user_type='customer')
            db.session.add(new_data)
            db.session.commit()

            return redirect (url_for('home'))

    return render_template ('page1.html')




@app.route('/page2' ,  methods=['GET'])
def page2():
    return render_template ('page2.html')

@app.route('/page3' ,  methods=['GET'])
def page3():
    return render_template ('page3.html')

@app.route('/demo' ,  methods=['GET'])
def demo():
    # data_1 = users.query.all()
    # data_2 = users.query.first()

    # data_1 = users.query.filter_by(user_type='theater_owner').all()
    # data_1 = users.query.filter(users.name.like('s%')).all()

    # data_1 = users.query.filter(users.name.like('%a%'),users.user_type == 'theater_owner').all()
    # for i in data_1:
    #     print(f"name: {i.name}, email: {i.email}")

    new_data = users(name= 'ravi' , email='rv@email.com', password=1234, user_type='customer')

    data= users.query.filter_by(email='rv@email.com').first()


    if data :
        print("hit")
        return "email already exists please use a differen email"
    else:
        db.session.add(new_data)
        db.session.commit()




    return "look in to the VS code terminal"





if __name__ == '__main__':
    db.create_all()
    app.debug= True
    app.run()


