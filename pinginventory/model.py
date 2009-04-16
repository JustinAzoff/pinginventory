"""The application's model objects"""
import datetime

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.databases.postgres import PGInet

# SQLAlchemy database engine. Updated by model.init_model()
engine = None

# SQLAlchemy session manager. Updated by model.init_model()
Session = scoped_session(sessionmaker(autoflush=True))

# Global metadata. If you have multiple databases with overlapping table
# names, you'll need a metadata for each database
metadata = MetaData()

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)
    metadata.bind = engine

Base = declarative_base(metadata=metadata)

class Inventory(Base):
    __tablename__ = 'inventory'

    id          = sa.Column(sa.types.Integer,       primary_key=True)
    starttime   = sa.Column(sa.types.DateTime,      nullable=False)
    endtime     = sa.Column(sa.types.DateTime,      nullable=False)
    numup       = sa.Column(sa.types.Integer,       nullable=False)

    def __repr__(self):
        return "Inventory(id=%d, starttime=%s, endtime=%s, numup=%d" % (
            self.id, self.starttime, self.endtime, self.numup)

    @classmethod
    def list(self):
        return Session.query(Inventory).order_by(sa.desc(self.starttime))
    
    @classmethod
    def most(self):
        return Session.query(Inventory).order_by(sa.desc(self.numup)).first()

    @classmethod
    def latest(self):
        return Session.query(Inventory).order_by(sa.desc(self.starttime)).first()

    @classmethod
    def count(self):
        return Session.query(Inventory).count()

    nodes       = orm.relation('Node', backref='inventory', lazy='dynamic',order_by='Node.ip')


class Node(Base):
    __tablename__ = 'node'
    inventory_id= sa.Column(sa.types.Integer,       sa.ForeignKey('inventory.id'), primary_key=True)
    ip          = sa.Column(PGInet,                 nullable=False, primary_key=True)

    def __repr__(self):
        return "Node(inventory_id=%d, ip=%s)" % (self.inventory_id, self.ip)

def get_ip_history(ip):
    return Session.query(Inventory.starttime, sa.exists(
            [1], sa.and_(Node.inventory_id==Inventory.id,Node.ip==ip)
    )).order_by(Inventory.starttime).all()
