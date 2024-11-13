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

class theaters_users_relationship(db.Model):
    __tablename__ ='theaters_users_relationship'
    theater_id = db.Column(db.Integer, db.ForeignKey('theaters.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)



class theaters(db.Model):
    __tablename__ ='theaters'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    theater_name = db.Column(db.String, unique=True)
    theater_location = db.Column(db.String)
    approval_status = db.Column(db.Boolean, default=False)
    user_id = db.relationship('users', secondary= 'theaters_users_relationship')
   
   