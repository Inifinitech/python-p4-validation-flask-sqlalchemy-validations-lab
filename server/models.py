from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def check_author(self, key, name):
        if not name:
            raise ValueError('All authors must have a name')
        
        author_inlist = Author.query.filter(Author.name == name).first()
        if author_inlist:
            raise ValueError(f'The author name {name} is taken')
        return name
    
    @validates('phone_number')
    def digits(self, key, number):
        if number is not None and len(number) != 10 or not number.isdigit():
            raise ValueError('Author phone numbers should be exactly ten digits')
        return number
        

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('content')
    def validate_content(self,key,content):
        if content is None or len(content) < 250:
            raise ValueError('Post content should be at least 250 characters')
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if summary is None or len(summary) > 250:
            raise ValueError('Post summary should be a maximum of 250 characters')
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError('Post category should be either Fiction or Non-Fiction')
        return category
    
    @validates('title')
    def validates_title(self, key, title):
        if not title:
            raise ValueError('A post must have a title')
        
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if any(phrase in title for phrase in clickbait_phrases):
            raise ValueError('Post title cannot be a Clickbait')
        return title


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
