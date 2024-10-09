from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String,  nullable=False,unique= True)
    phone_number = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @db.validates('name')
    def validates_name(self, key, name):
        if not name:
            raise ValueError (f"Name must be present")
        if Author.query.filter_by(name=name).first():
            raise ValueError("Name must be unique")
        

        return name
    
    @db.validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number is not None and (len(phone_number) != 10 or not phone_number.isdigit()):
            raise ValueError("requires each phone number to be exactly ten digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @db.validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return content
    
    @db.validates('summary')
    def validates_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("category must be in fiction or non fiction")
        return summary
    
    @db.validates('category')
    def validates_category(self, key, category):
        if category not in  ['Fiction','Non-Fiction']:
            raise ValueError("category must be in fiction or non fiction")
        return category
    
    @db.validates('title')
    def validate_title(self, key, title):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Post title must contain one of the following: 'Won't Believe', 'Secret', 'Top', 'Guess'.")
        return title
        


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
