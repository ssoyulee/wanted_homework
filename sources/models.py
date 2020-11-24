# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Company(db.Model):
    __tablename__ = 'company'

    company_id = db.Column(db.Integer, primary_key=True)
    company_rep_name = db.Column(db.Text)



class CompanyLang(db.Model):
    __tablename__ = 'company_lang'

    company_id = db.Column(db.Integer, primary_key=True, nullable=False)
    company_lang_type = db.Column(db.Text, primary_key=True, nullable=False)
    company_lang_name = db.Column(db.Text, nullable=False)
    company_lang_tag = db.Column(db.Text, nullable=False)
