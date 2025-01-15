from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from flask_bcrypt import Bcrypt
#from flask_session import Session
#from flask import redirect, url_for
from openai import OpenAI
from dotenv import load_dotenv
from db import db, db_config
from models import User, Message, Session
from functions import Preferences, getTools, FindURLs
#from forms import ProfileForm, SignUpForm, LoginForm
#from flask_wtf.csrf import CSRFProtect
from os import getenv
import json
from bot import build_prompt, search_movie_or_tv_show, where_to_watch
from sqlalchemy import desc
from datetime import datetime
import pytz
from markupsafe import Markup

# Carga variables de entorno desde .env
load_dotenv()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Inicia sesión para continuar'

client = OpenAI()

app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY')

bootstrap = Bootstrap5(app)
#csrf = CSRFProtect(app)
login_manager.init_app(app)
bcrypt = Bcrypt(app)
db_config(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:    
        user = db.session.query(User).get(current_user.id)
    else:
        user = None

    return render_template('landing.html', usr=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    email = ''
    if request.method == 'GET':
        return render_template('login.html', email=email)

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
    
        user = db.session.query(User).filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                session['first'] = '1'
                session['newpreferences'] = '0'
                login_user(user)
                return redirect('chat')
            else:
                flash("Contraseña incorrecta!", "error")
        else:
            email = ''
            flash("Email no está registrado!", "error")

    return render_template('login.html', email=email)


@app.get('/logout')
def logout():
# ---------------------------------------------------------------------------------------------------------------
# Cierra sesión del usuario, libera variables de sesión y vuelve a página de inicio.
# ---------------------------------------------------------------------------------------------------------------
    session.pop('first', None)
    session.pop('newpreferences', None)

    logout_user()
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
# ---------------------------------------------------------------------------------------------------------------
# Registro de un nuevo usuario
# ---------------------------------------------------------------------------------------------------------------
    if current_user.is_authenticated:    
        return redirect('/')
    else:
        name = ''
        fav_movies = ''
        fav_series = ''
        kind_movies = ''

    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('nombre')
        fav_movies = request.form.get('fav_movies')
        fav_series = request.form.get('fav_series')
        kind_movies = request.form.get('kind_movies')

        usrval = db.session.query(User).filter_by(email=email).first()
        if usrval:
            flash("Email ya se encuentra registrado!", "error")
            return render_template('signup.html', 
                                   name=name, 
                                   fav_movies=fav_movies, 
                                   fav_series=fav_series, 
                                   kind_movies=kind_movies)
        else:
            user = User(email=email, 
                        password=bcrypt.generate_password_hash(request.form.get('password1')).decode('utf-8'), 
                        name=name, 
                        fav_movies=fav_movies, 
                        fav_series=fav_series, 
                        kind_movies=kind_movies)
            db.session.add(user)
            db.session.commit()
            session['first'] = '1'
            session['newpreferences'] = '0'
            login_user(user)
            return redirect('chat')

    return render_template('signup.html',
                           name=name, 
                           fav_movies=fav_movies, 
                           fav_series=fav_series, 
                           kind_movies=kind_movies)


@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
# ---------------------------------------------------------------------------------------------------------------
# Interacción con Chatbot
# ---------------------------------------------------------------------------------------------------------------
    user = db.session.query(User).get(current_user.id)

    sChkF = 'checked'
    sChkQ = ''
    sChk1 = 'checked'
    sChk2 = ''

    if request.method == 'GET':
        if session['first'] == '1':
            # Guarda nueva sesión en la BD
            sesion = Session(user_id=user.id, 
                              created_at=datetime.now(pytz.timezone('America/Santiago')))
            db.session.add(sesion)
            db.session.commit()

            sPreferences = Preferences(user.fav_movies,user.fav_series,user.kind_movies)

            # Guarda el primer mensaje de la sesión en la BD
            sMsg = f"Hola {user.name}! Soy Verflix, y mi rol es recomendar películas ó series."

            if len(sPreferences) > 0:
                if session['newpreferences'] == '0':
                    sMsg += f' Se que tus preferencias son las siguientes: {sPreferences}.'
                else:
                    sMsg += f' Se que tus nuevas preferencias son las siguientes: {sPreferences}.'
            
            sMsg += ' ¿En qué te puedo ayudar?.'

            db.session.add(Message(content=sMsg, 
                                   author="assistant", 
                                   created_at=datetime.now(pytz.timezone('America/Santiago')), 
                                   user=user, 
                                   session=sesion))
            db.session.commit()

            session['first'] = '0'
            session['newpreferences'] = '0'
        else:
            sesion = db.session.query(Session).filter(Session.user_id == user.id).order_by(desc(Session.created_at)).first()

        Checks = [sChkF,sChkQ,sChk1,sChk2]

        return render_template('chat.html', messages=user.messages, usr=user, chks=Checks)
    
    if request.method == 'POST':
        intent = request.form.get('intent')

        sMsgType =  request.form.get('MsgType')
        if sMsgType == 'QuickMsg':
            sChkF = ''
            sChkQ = 'checked'

        sType =  request.form.get('inlineRadioOptions')
        if sType == 'Serie':
            sChk1 = ''
            sChk2 = 'checked'

        Checks = [sChkF,sChkQ,sChk1,sChk2]

        intents = {
            'CF': f'Recomiéndame una {sType} del género ciencia ficción',
            'S': f'Recomiéndame una {sType} del género suspenso',
            'C': f'Recomiéndame una {sType} del género comedia',
            'Enviar': request.form.get('message')
        }

        if intent in intents:
            sesion = db.session.query(Session).filter(Session.user_id == user.id).order_by(desc(Session.created_at)).first()
            user_message = intents[intent]

            # Guardar nuevo mensaje en la BD
            db.session.add(Message(content=user_message, 
                                   author="user",
                                   created_at=datetime.now(pytz.timezone('America/Santiago')), 
                                   user=user, 
                                   session=sesion))
            db.session.commit()

            messages_for_llm = [{
                "role": "system",
                "content": build_prompt(user, ''),
            }]

            for message in user.messages:
                messages_for_llm.append({
                    "role": message.author,
                    "content": message.content,
                })

            chat_completion = client.chat.completions.create(
                messages=messages_for_llm,
                model="gpt-4o",
                temperature=1,
                tools = getTools()
            )

            model_recommendation = ''

            if chat_completion.choices[0].message.tool_calls:
                tool_call = chat_completion.choices[0].message.tool_calls[0]

                if tool_call.function.name == 'where_to_watch':
                    arguments = json.loads(tool_call.function.arguments)
                    name = arguments['name']
                    model_recommendation = where_to_watch(client, name, user)
                elif tool_call.function.name == 'search_movie_or_tv_show':
                    arguments = json.loads(tool_call.function.arguments)
                    name = arguments['name']
                    model_recommendation = search_movie_or_tv_show(client, name, user)

                model_recommendation = model_recommendation.replace('- **','<br/><b>')
                model_recommendation = model_recommendation.replace('**','</b>')

                urls = FindURLs(model_recommendation)
                for url in urls:
                    model_recommendation = Markup(model_recommendation.replace(url,f'<a href="{url}" target="_blank">click aquí</a>'))

            else:
                model_recommendation = chat_completion.choices[0].message.content

            db.session.add(Message(content=model_recommendation, 
                                   author="assistant",
                                   created_at=datetime.now(pytz.timezone('America/Santiago')), 
                                   user=user, 
                                   session=sesion))
            db.session.commit()

            return render_template('chat.html', messages=user.messages, usr=user, chks=Checks)

@app.route('/profile', methods=['POST'])
@login_required
def profile():
# ---------------------------------------------------------------------------------------------------------------
# Guarda en BD las preferencias del usuario  
# ---------------------------------------------------------------------------------------------------------------
    user = db.session.query(User).get(current_user.id)

    name = user.name
    fav_movies = user.fav_movies
    fav_series = user.fav_series
    kind_movies = user.kind_movies

    user.name = request.form.get('nombre')
    user.fav_movies = request.form.get('fav_movies')
    user.fav_series = request.form.get('fav_series')
    user.kind_movies = request.form.get('kind_movies')
    db.session.commit()
    db.session.refresh(user)

    if fav_movies != user.fav_movies or fav_series != user.fav_series or kind_movies != user.kind_movies:
        session['first'] = '1'
        session['newpreferences'] = '1'
    elif name != user.name:
        session['first'] = '1'
        session['newpreferences'] = '0'

    return render_template('landing.html', usr=user)


