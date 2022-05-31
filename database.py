"""
alembic init migrations

change sqlalchemy.url = "" to the url of your database eg. sqlite:///data.sqlite in the alembic.ini file

change target_metadata = None to target_metadata = Base.metadata, also from models import Base before

alembic revision --autogenerate -m "message"

alembic upgrade heads
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import *

class DBManager:

    session = sessionmaker(bind=create_engine('sqlite:///data.sqlite'))
    session = scoped_session(session) #making use of session safe in threading

    """ def __init__(self):

        self.session = sessionmaker(bind=create_engine('sqlite:///data.sqlite'))
        self.session = scoped_session(self.session) #making use of session safe in threading """

    #kwargs --> obj=Table in database, id|email|name=value, attr=column, value=value
    def mod_row( **kwargs):

        with DBManager.session() as s:
            row = None
            for key, value in kwargs.items():
                if key == 'id':
                    s.query(kwargs['obj']).filter(kwargs['obj'].id==kwargs['id']).update({kwargs['attr']: kwargs['value']})
                elif key == 'name':
                    s.query(kwargs['obj']).filter(kwargs['obj'].name==kwargs['name']).update({kwargs['attr']: kwargs['value']})
            s.commit()

    def add_row(obj):
        print("trying to commit")
        with DBManager.session() as s:
            s.add(obj)
            s.commit()
            print('committed')

    def del_row(obj, id):
        with DBManager.session() as s:
            row = s.query(obj).filter_by(id=id).first()
            s.delete(row)
            s.commit()

    #kwargs --> obj=table from database, id|email|name=..., all=True
    def get_row(**kwargs):

        def patientmapper(obj):
            if obj == None:
                return None
            x = {
                'id': obj.id,
                'hid': obj.hid,
                'name': obj.name,
                'age': obj.age,
                'gender': obj.gender,
                'weight': obj.weight,
                'height': obj.height,
                'notes': obj.notes,
                'datetime': obj.datetime,
                'pe': obj.pe,
            }

            return x

        def scanmapper(obj):
            if obj == None:
                return None
            x = {
                'id': obj.id,
                'name': obj.name,
                'pid': obj.pid,
                'pname': obj.pname,
                'data': obj.data,
                'v3d': obj.v3d,
                'datetime': obj.datetime,

            }

            return x

        def settingsmapper(obj):
            if obj == None:
                return None
            x = {
                'localizer' : obj.localizer,
                'pdf' : obj.pdf,
                'csv' : obj.csv,
                'pic_format' : obj.pic_format,
                'v3d' : obj.v3d,
                'results' : obj.results,
                'probability': obj.probability
            }

            return x

        records = None
        with DBManager.session() as s:

            for key, value in kwargs.items():
                if key == 'all':
                    records = s.query(kwargs['obj']).all()
                elif key == 'id':
                    print('id')
                    records = [s.query(kwargs['obj']).filter_by(id=kwargs['id']).first()]
                elif key == 'name':
                    records = [s.query(kwargs['obj']).filter_by(id=kwargs['name']).first()]

        if kwargs['obj'] == Patient:
            records = list(map(patientmapper, records))
        elif kwargs['obj'] == Scan:
            records = list(map(scanmapper, records))
        elif kwargs['obj'] == Settings:
            print('setting mapper')
            records = list(map(settingsmapper, records))

        return records
        
#service = [Service(name='Customer Care', sector='C', )]
#user = [User(email='jermainedavis@gmail.com', fname='jermaine', lname='davis', alias='jay', password='xyz123', counter=7, service1=1)]

#add_row(user[0])
#update_row(obj=User, id=2, attr='service1', value=None)
#del_row(User, 3)
#a = get_row(obj=User, id=2)
#print(a)