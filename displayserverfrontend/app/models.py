#  Created by Marcello Monachesi at 9/6/19, 5:30 PM

from app import db


class IPCamera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(64))
    port = db.Column(db.Integer)
    name = db.Column(db.String(64), index=True, unique=True)
    ftp = db.Column(db.Boolean)

    def __repr__(self):
        return '<IPCamera {}>'.format(self.id)
