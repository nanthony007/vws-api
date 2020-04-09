from app import db

class Wrestler(db.Model):
    __tablename__ = 'wrestlers'

    name = db.Column(db.String(), primary_key=True)
    team = db.Column(db.String())
    rating = db.Column(db.Integer())

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'name': self.name,
            'team': self.team,
            'rating':self.rating
        }

