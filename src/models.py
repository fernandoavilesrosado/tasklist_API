from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    __tablename__ :'person'
    id = db.Column(db.Integer, primary_key=True)
    nickmane = db.Column(db.String, unique=True, nullable=False)
    #this is the relationship with children
    have_task = db.relationship("Task", lazy=True)

    def __repr__(self):
        return f"Person {self.id}, user {self.nickmane}"#this line write the information in the window
    #this is the dictionary
    def serialize(self):
        return {
            "id": self.id,
            "nickname": self.nickmane
            # do not serialize the password, its a security breach
        }
#CREO UN UUARIO METOTH POST

class Task(db.Model):
    __tablename__: 'task'
    id = db.Column(db.Integer, primary_key=True)
    task_txt = db.Column(db.String, unique=False, nullable=False)
    is_active = db.Column(db.Boolean(True), nullable=False)
    #this is the relationship whit parent
    id_person = db.Column(db.Integer, db.ForeignKey("person.id"))

    def __repr__(self):
        return f'Task {self.id}, from user {self.id_person}'

    #this is the dictionary 
    def serialize(self):
        return{
            "id": self.id,
            "task_txt": self.task_txt 
        }