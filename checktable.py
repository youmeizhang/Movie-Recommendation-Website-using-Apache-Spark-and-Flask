#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 12:22:30 2018

@author: yumi.zhang
"""

#check if a user exists in the database
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

Session = sessionmaker(bind=engine)
s = Session()
POST_USERNAME = "3"
result = s.query(User).filter(User.password.in_([POST_USERNAME])).all()
print(result)