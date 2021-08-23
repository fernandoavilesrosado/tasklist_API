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
#
    def create(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        personList = cls.query.all()
        return [usr.to_dict() for user in user_list]
    
    @classmethod
    def get_by_id(cls, id):
        account = cls.query.get(id)
        return account
    
    def update(slef, nick):
        self.nickmane = nickmane
        db.session.commit()
    
    @classmethod
    def get_by_nickmane(cls,nickmane):
        account = cls.query.filter_by(nickmane = nickmane).one_or_none()
        return person

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Task(db.Model):
    __tablename__: 'task'
    id = db.Column(db.Integer, primary_key=True)
    task_txt = db.Column(db.String, unique=False, nullable=False)
    is_active = db.Column(db.Boolean(True), nullable=False)
    #this is the relationship whit parent
    id_person = db.Column(db.Integer, db.ForeignKey("person.id"))

    def __repr__(self):
        return f'Task {self.id}, task_txt:{self.task_txt} from user {self.id_person}'

    #this is the dictionary 
    def serialize(self):
        person = Person.get_by_id(self.person_id)
        return{
            "id": self.id,
            "task_txt": self.task_txt 
        }

    def add_new(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_task(cls):
        tasks 0 cls.query.all()
        return [task.serialize() for task in task]

    @classmethod
    def get_task_by_person(cls, id):
        specific_task_list = cls.query.filter_by(person.id = id, status = False)
        return [element.serialize() for element in specific_task_list]
    
    @classmethod
    def get_one_task(cls, position):
        one_task = cls.query.get(position)
        return one_task-serialize()

    def delete(self):
        db.session.delete(self)
        db.session.commit()