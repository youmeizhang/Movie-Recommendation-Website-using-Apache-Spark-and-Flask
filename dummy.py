#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 12:07:50 2018

@author: yumi.zhang
"""

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///tutorial.db', echo = True)

Session = sessionmaker(bind = engine)
session = Session()

#manually add users information into the database
user = User("1", "1")
session.add(user)

user2 = User("2", "2")
session.add(user2)

user3 = User("3", "3")
session.add(user3)

session.commit()
session.commit()