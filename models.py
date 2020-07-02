from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from re import sub

# SQLAlchemy Setup
Base = declarative_base()
engine = create_engine('sqlite:///methods.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Method(Base):
    __tablename__ = 'methods'
    id = Column(Integer, primary_key=True)               # method['id'] (formatted)

    stage = Column(Integer)                              # mset.properties.stage
    classification = Column(String(32))                  # mset.properties.classification.string
    plain = Column(Boolean, default=False)               # mset.properties.classification['plain']
    trebledodging = Column(Boolean, default=False)       # mset.properties.classification['trebledodging']
    little = Column(Boolean, default=False)              # mset.properties.classification['little']
    differential = Column(Boolean, default=False)        # mset.properties.classification['differential']
    lengthoflead = Column(Integer)                       # mset.properties.lengthoflead
    numberofhunts = Column(Integer)                      # mset.properties.numberofhunts
    huntbellpath = Column(String(32))                    # mset.properties.huntbellpath
    methodset_notes = Column(String(128))                # mset.properties.notes

    title = Column(String(128), index=True, unique=True) # method.title
    name = Column(String(128), index=True)               # method.name
    leadhead = Column(String(32))                        # method.leadhead
    leadheadcode = Column(String(32))                    # method.leadheadcode
    symmetry = Column(String(32))                        # method.symmetry
    notation = Column(String(128))                       # method.notation
    falseness = Column(String(32))                       # method.falseness.fchgroups
    extensionconstruction = Column(String(32))           # method.extensionconstruction
    notes = Column(String(128))                          # method.notes


    pmmref = Column(String(32))                          # method.references.pmmref
    bnref = Column(String(32))                           # method.references.bnref
    cbref = Column(String(32))                           # method.references.cbref
    rwref = Column(String(32))                           # method.references.rwref
    tdmmref = Column(String(32))                         # method.references.tdmmref


    performances = relationship("Performance", back_populates="method")


    @property
    def full_notation(self):
        if not ',' in self.notation: return self.notation
        symmetric, division = self.notation.split(',')
        symmetric = sub('-','.-.',symmetric).strip('.').split('.')
        return ''.join(symmetric + symmetric[:-1][::-1]) + division

    @property
    def full_notation_list(self):
        return sub('-','.-.', self.full_notation).strip('.').split('.')

    def __repr__(self):
        return '<Method {}>'.format(self.title)

    def __iter__(self):
        for key, val in self.__dict__.items():
            if key == '_sa_instance_state': continue
            yield (key, val)


class Performance(Base):
    __tablename__ = 'performances'
    id = Column(Integer, primary_key=True, autoincrement=True) # id
    kind = Column(String(32))                                  # method.performances.KIND
    date = Column(Date)                                        # PERF.date
    society = Column(String(32))                               # PERF.society
    town = Column(String(32))                                  # PERF.location.town
    county = Column(String(32))                                # PERF.location.county
    building = Column(String(32))                              # PERF.location.building
    address = Column(String(32))                               # PERF.location.address
    country = Column(String(32))                               # PERF.location.country
    room = Column(String(32))                                  # PERF.location.room
    region = Column(String(32))                                # PERF.location.region
    method_id_fk = Column(Integer, ForeignKey('methods.id'))
    method = relationship("Method", back_populates="performances")

    def __repr__(self):
        return '<Performance {}: {}>'.format(self.kind, self.method.title)

    def __iter__(self):
        for key, val in self.__dict__.items():
            if key == '_sa_instance_state': continue
            if key == 'method': continue
            yield (key, val)
