
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request , redirect , url_for , session ,flash , get_flashed_messages
from database import db, Usuario , Ambiente
from sqlalchemy import or_

app = Flask(__name__)
app.secret_key = 'Ig24032010@'

msg_ant = get_flashed_messages

#PASTA DE UPLOAD

UPLOAD_FOLDER = os.path.join(
    app.root_path,
    'static',
    'imagens',
    'uploads'
)
# CONFIGURAÇÕES DO BANCO DE DADOS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CONECTAR E CRIAR TABELAS
db.init_app(app)




with app.app_context():
    db.create_all()


# TELAS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apresentacao')
def index2():
    return render_template('index2.html')

@app.route('/cadastro')
def index3():
    return render_template('index3.html')

@app.route('/login')
def index4():
    return render_template('index4.html')
@app.route('/feed')
def index5():
    user_name = session.get('user_name' , 'Visitante')
    all_ambientes = Ambiente.query.all()
    return render_template('index5.html' , user_name=user_name , ambientes=all_ambientes )

@app.route('/form_abnd')
def index6():
    user_name = session.get('user_name' , 'Visitante')
    return render_template('index6.html',user_name=user_name )
#  ÁREA DE CADASTRO

@app.route('/enviar', methods=['POST'])
def enviar():

    nome_form = request.form.get('name')
    email_form = request.form.get('email')
    senha_raw = request.form.get('password')
    re_senha_raw = request.form.get('re-password')

    if re_senha_raw == senha_raw:
        senha_form = generate_password_hash(senha_raw)

        print("Senha válida e recebida.")
        novo_usuario = Usuario(
            nome=nome_form,
            email=email_form,
            senha=senha_form
        )

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            return redirect(url_for('index3'))
        except Exception as e:
            db.session.rollback()
            return f'erro ao cadastrar {e}'
        
        
    else:
        print('senhas não conferem.')
        # RETORNO OBRIGATÓRIO
        return 'Erro: As senhas digitadas não conferem!'


# ÁREA DE LOGIN

@app.route('/login', methods=['POST'])
def login():
    user_lg = request.form.get('lg_user')
    try:
        user_bd = Usuario.query.filter(or_(Usuario.nome == user_lg, Usuario.email == user_lg)).first()
        if user_bd:
                print('Usuário encontrado. \n Próxima etapa senha: ')
        
                if check_password_hash(user_bd.senha , request.form.get('lg_password')):
        
                    session['user_id'] = user_bd.id
                    session['user_name'] = user_bd.nome
                    print('Senha Correta!')
                    return redirect(url_for('index5'))
                
                else:
                    db.session.rollback()
                    flash('senha incorreta' , 'erro')
                    return redirect(url_for('index4'))
                    
        else:
            db.session.rollback()
            flash('usuário inexistente' , 'erro')
            return redirect(url_for('index4'))
    except Exception as e:
        
        return f'erro ao fazer o login {e}'
    


# ÁREA DE DESLOGAR

@app.route('/logout' , methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index4'))
# CADASTRO DE LOCAIS

@app.route('/upload' , methods=['POST'] )
def upload():
    nome = request.form.get('name_abnd')
    situacao = request.form.get('situacao')
    pr_name = request.form.get('pr_name')
    desc = request.form.get('desc') 
    user_id = session.get('user_id')
    rg_name = session.get('user_name')
    #ÁREA DA IMAGEM

    arq_img = request.files.get('img')
    arq_nome = ''

    if arq_img  and arq_img.filename != '':
        arq_nome = secure_filename(arq_img.filename)

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        caminho = os.path.join(UPLOAD_FOLDER, arq_nome)
        
        arq_img.save(caminho)
       
    else:
        return 'erro '
    
    novo_ambiente = Ambiente(
                    user_id=user_id,
                    nome=nome,
                    img=arq_nome,
                    situacao=situacao,
                    desc=desc,
                    pr_nome=pr_name,
                    rg_name=rg_name
                )
        
    try:
        db.session.add(novo_ambiente)
        db.session.commit()
        return redirect(url_for('index5'))
    except Exception as e:
        db.session.rollback()
        return f'erro ao registrar  {e}'    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
