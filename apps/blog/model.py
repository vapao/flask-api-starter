from public import db
from libs import ModelMixin


class Blog(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    count = db.Column(db.Integer)
