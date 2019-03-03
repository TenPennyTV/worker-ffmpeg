# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import config

engine = create_engine('postgresql://%s:%s@%s:%s/tenpenny?sslmode=require' % (config.DB_USER, config.DB_PW, config.DB_HOST, config.DB_PORT))

Session = sessionmaker(bind=engine)

# new session.   no connections are in use.
session = Session()
