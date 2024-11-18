from flask import Flask , render_template, request , redirect ,url_for
from model import *
import os
from sqlalchemy import and_

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///" + os.path.join(current_dir, 'database.sqlite3') 

db.init_app(app)
app.app_context().push()

@app.route('/', methods=['GET','POST']) # / = http://127.0.0.1:5000/
def home():
    if request.method=="POST":
        data_email = request.form['email']
        data_password = request.form['password']

        user= users.query.filter_by(email = data_email).first()
        print(user)

        if user:
            
            if data_password == user.password:
                print("LLL")
                if user.user_type == 'admin':
                    return redirect(url_for('admin'))
                elif user.user_type == 'customer':
                    return render_template('user_adshbord.html')
                elif user.user_type == 'theater_owner':
                    query = theaters_users_relationship.query.filter_by(user_id =user.id).first()
                    theater_data= theaters.query.filter_by(id=query.theater_id).first()
                    print(theater_data.approval_status)
                    if theater_data.approval_status == False:
                        return 'approval pending '
                    else:
                        return redirect(url_for('theater_dashbord', id=user.id))
                 
        else: 
            return 'user dosn\'t exists'
         



    return render_template('home.html')




@app.route('/user_signup' ,  methods=['GET','POST'])
def user_signup():
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




@app.route('/theater_signup' ,  methods=['GET', 'POST'])
def page2():
    if request.method=="POST":
        data_username= request.form['Username']
        data_email = request.form['email']
        data_password = request.form['password']
        data_theater_name = request.form['theater name']
        data_location = request.form['location']

        data = users.query.filter_by(email=data_email).first()

        if data :
            return "email already exists please use a differen email"
        else:
            new_user=users(name= data_username , email=data_email ,
                            password=data_password , user_type='theater_owner')
            
           
            new_theater = theaters(theater_name = data_theater_name, theater_location = data_location )

           

            db.session.add(new_theater)
            db.session.add(new_user)
            db.session.commit()
            
            new_relationship = theaters_users_relationship(theater_id=new_theater.id , user_id= new_user.id )

            db.session.add(new_relationship)
            db.session.commit()

            return redirect (url_for('home'))




    return render_template ('page2.html')

@app.route('/page3' ,  methods=['GET'])
def page3():
    return render_template ('page3.html')




@app.route('/admin' ,  methods=['GET',"POST"])
def admin():

    if request.method=="POST":
        data_id= request.form['id']
        data_status = request.form['status']
        
        theater = theaters.query.filter_by(id = data_id).first()

        if data_status == "T":
            theater.approval_status= True
        else:
            theater.approval_status= False
        
        db.session.commit()



    approval_list= theaters.query.filter_by(approval_status = False).all()
    
    return render_template('admin_adshbord.html' , data=approval_list)




@app.route('/theater_dashbord/<id>' ,  methods=['GET',"POST"])
def theater_dashbord(id):

    if request.method=="POST":
        title = request.form['title']
        genre = request.form['genre']
        date = request.form['date']
        time = request.form['time']
        price_of_ticket = request.form.get('price_of_ticket')
        seats = request.form['seats']
        poster = request.form['poster']
        host_id = request.form['host_id']

        new_movie = movies(
            title=title,
            genre=genre,
            date=date,
            time=time,
            price_of_ticket=price_of_ticket,
            seats=seats,
            poster=poster
        )
        
        db.session.add(new_movie)
        db.session.commit()

        new_relation = theaters_movie_relationship(theater_id = host_id , movie_id =new_movie.id)

        db.session.add(new_relation)
        db.session.commit()



        

    

    user=users.query.filter_by(id = id).first()
    query= theaters_users_relationship.query.filter_by(user_id =user.id).first()
    theater_data= theaters.query.filter_by(id=query.theater_id).first()
    print(theater_data.hosted_movies)
   

    return render_template('theater_owner_dashbord.html', theater_owner=user ,theater=theater_data) 
   

@app.route('/update_data/<id>' ,  methods=['GET',"POST"])
def update_data(id):
    if request.method=="POST":
        theater_Id = request.form['t_id']
        movie_Id = request.form['m_id']

        entry = theaters_movie_relationship.query.filter_by( theater_id =   theater_Id , movie_id= movie_Id ).first()

        db.session.delete(entry)
        db.session.commit()

        movie = movies.query.filter_by(id=movie_Id).first()

        db.session.delete(movie)
        db.session.commit()

    return redirect(url_for( 'theater_dashbord', id = id ))


@app.route('/search' ,  methods=["POST"])
def search():
    filter_value = request.form['filter']  
    query = request.form['query']

    if filter_value == 'Title':
        movie_list= movies.query.filter_by(title = query ).all()
    elif filter_value == 'Genre':
        movie_list= movies.query.filter_by(genre= query ).all()   
    elif filter_value == 'Price':
        movie_list= movies.query.filter(movies.price_of_ticket <= int(query) ).all()

    return render_template('search_results.html' , data= movie_list)

    












@app.route('/demo' ,  methods=['GET'])
def demo():
    # data_1 = users.query.all()
    # data_2 = users.query.first()

    # data_1 = users.query.filter_by(user_type='theater_owner').all()
    # data_1 = users.query.filter(users.name.like('s%')).all()

    # data_1 = users.query.filter(users.name.like('%a%'),users.user_type == 'theater_owner').all()
    # for i in data_1:
    #     print(f"name: {i.name}, email: {i.email}")

    # new_data = users(name= 'ravi' , email='rv@email.com', password=1234, user_type='customer')

    # data= users.query.filter_by(email='rv@email.com').first()


    # if data :
    #     print("hit")
    #     return "email already exists please use a differen email"
    # else:
    #     db.session.add(new_data)
    #     db.session.commit()
    new_theater = theaters.query.filter_by(theater_name = 'Inox ' ).first()
    for i in new_theater.user_id:
        print(i.name)




    return "look in to the VS code terminal"





if __name__ == '__main__':
    db.create_all()
    app.debug= True
    app.run()


