from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# class demo_table(db.Model):
#     __tablename__ ='demo_table'
#     id =db.Column(db.Integer, primary_key = True, autoincrement = True)
#     name= db.Column(db.String)
#     phoneNo= db.Column(db.Integer)



# types of users :

# admin - menatains and manages the app
# theater_owner - contentcreaters of the app
# customers - the end users 


class users(db.Model):
    __tablename__ ='users'
    id =db.Column(db.Integer, primary_key = True, autoincrement = True)
    name= db.Column(db.String)
    email= db.Column(db.String , unique = True)
    password= db.Column(db.String)
    user_type= db.Column(db.String)
    