from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CRIAR BANCO DE DADOS

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()


# MODELO DE TABELA - USUÁRIO

class Usuario(db.Model):
    id = db.Column(db.Integer , primary_key =True)
    nome = db.Column(db.String(100) , nullable =False)
    email = db.Column(db.String(100) , nullable =False , unique =True)
    senha = db.Column(db.String(225) , nullable =False)

# MODELO DE TABELA - AMBIENTE

class Ambiente(db.Model):
    am_id = db.Column(db.Integer , primary_key = True)
    user_id = db.Column(db.String(100) , nullable=False )
    nome = db.Column(db.String(100) , nullable =False)
    img = db.Column(db.String(100) , nullable=False)
    pr_nome =  db.Column(db.String(100) , nullable =False)
    situacao = db.Column(db.String(50) , nullable =False)
    desc = db.Column(db.Text , nullable=False)
    rg_name = db.Column(db.String(20), nullable=False)