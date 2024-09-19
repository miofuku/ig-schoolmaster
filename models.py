from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(200), nullable=True)  # Stored as comma-separated values

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'summary': self.summary,
            'tags': self.tags.split(',') if self.tags else []
        }
