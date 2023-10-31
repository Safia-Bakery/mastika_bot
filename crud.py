from sqlalchemy.orm import Session
import models
import pytz
from typing import Optional
import requests
from sqlalchemy import or_,and_,Date,cast
from datetime import datetime 
timezonetash = pytz.timezone("Asia/Tashkent")



def get_user(db:Session,tel_id):
    query = db.query(models.Users).filter(models.Users.tel_id==tel_id).first()
    return query



def create_user(db:Session,tel_id,phone_number,full_name,user_name):
    query = models.Users(tel_id=tel_id,phone_number=phone_number,full_name=full_name,username=user_name,is_client=1,status=1)
    db.add(query)
    db.commit()
    return query

def updateuser(db:Session,tel_id,phone_number,full_name):
    query = db.query(models.Users).filter(models.Users.tel_id==tel_id).first()
    if query:
        if phone_number is not None:
            query.phone_number==phone_number
        if full_name is not None:
            query.full_name==full_name
        db.commit()
    return True