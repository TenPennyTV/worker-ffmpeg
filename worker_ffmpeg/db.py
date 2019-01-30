# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://tempuser:temppassword@localhost:5432/tenpenny')

Session = sessionmaker(bind=engine)

# new session.   no connections are in use.
session = Session()
