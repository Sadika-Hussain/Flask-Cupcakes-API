"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

default_image = 'https://tinyurl.com/demo-cupcake'


class Cupcake(db.Model):
    """
    Model representing a cupcake with attributes such as flavor, size, rating, and image.
    """
    __tablename__ = "cupcakes"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    flavor = db.Column(db.Text,
                     nullable=False)
    
    size = db.Column(db.Text,
                     nullable=False)
    
    rating = db.Column(db.Float, nullable = False)
    
    image = db.Column(db.Text, nullable = False)

    def serialize(self):
        """Serialize the Cupcake object into a dictionary format.
        
        Returns:
            A dictionary with the cupcake's ID, flavor, size, rating, and image URL.
            If no image is provided, a default image URL is used.
        """
        return {
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating': self.rating,
            'image': self.image or default_image
        }


