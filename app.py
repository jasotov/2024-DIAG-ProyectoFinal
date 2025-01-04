from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from openai import OpenAI
from dotenv import load_dotenv
from db import db, db_config
from models import User, Message, Session
from sqlalchemy import desc

# Carga variables de entorno desde .env
load_dotenv()

client = OpenAI()
app = Flask(__name__)
bootstrap = Bootstrap5(app)
db_config(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    user = db.session.query(User).first()

    if request.method == 'GET':
        return render_template('landing.html', usr=user)
    else:
        user.name = request.form.get('nombre')
        user.fav_movies = request.form.get('fav_movies')
        user.fav_series = request.form.get('fav_series')
        user.kind_movies = request.form.get('kind_movies')
        db.session.commit()
        db.session.refresh(user)

        return render_template('landing.html', usr=user)


@app.route('/chat', defaults={'user_id': 1, 'case': ''})
@app.route('/chat/<int:user_id>/<string:case>', methods=['GET', 'POST'])
def chat(user_id, case):
    user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one()
    # user = db.session.query(User).filter(User.id == user_id).first()
    sChk1 = 'checked'
    sChk2 = ''

    if request.method == 'GET':
        if case == 'first':
            # Guarda nueva sesión en la BD
            session = Session(user_id=user.id)
            db.session.add(session)

            # Guarda el primer mensaje de la sesión en la BD
            sMsg = f"Hola {user.name}! Soy Verflix, un recomendador de películas. ¿En qué te puedo ayudar?"
            db.session.add(Message(content=sMsg, author="assistant", user=user, session=session))
            db.session.commit()
        else:
            # session = db.session.execute(db.select(Session).filter_by(user_id=user_id).order_by(Session.created_at.desc)).first()
            session = db.session.query(Session).filter(Session.user_id == user_id).order_by(desc(Session.created_at)).first()
        
        return render_template('chat.html', messages=user.messages, usr=user, chk1=sChk1, chk2=sChk2)

    intent = request.form.get('intent')
    sType =  request.form.get('inlineRadioOptions')
    if sType == 'Serie':
        sChk1 = ''
        sChk2 = 'checked'

    intents = {
        'CF': f'Recomiéndame una {sType} de ciencia ficción',
        'S': f'Recomiéndame una {sType} de acción',
        'C': f'Recomiéndame una {sType} de comedia',
        'Enviar': request.form.get('message')
    }

    if intent in intents:
        session = db.session.query(Session).filter(Session.user_id == user_id).order_by(desc(Session.created_at)).first()
        user_message = intents[intent]

        # Guardar nuevo mensaje en la BD
        db.session.add(Message(content=user_message, author="user", user=user, session=session))
        db.session.commit()

        sMsg = "Eres un chatbot que recomienda películas y series, te llamas 'Verflix'. Tu rol es responder recomendaciones de manera breve y concisa. No repitas recomendaciones."

        messages_for_llm = [{
            "role": "system",
            "content": sMsg,
        }]

        for message in user.messages:
            messages_for_llm.append({
                "role": message.author,
                "content": message.content,
            })

        chat_completion = client.chat.completions.create(
            messages=messages_for_llm,
            model="gpt-4o",
            temperature=1
        )

        model_recommendation = chat_completion.choices[0].message.content
        db.session.add(Message(content=model_recommendation, author="assistant", user=user, session=session))
        db.session.commit()

        return render_template('chat.html', messages=user.messages, usr=user, chk1=sChk1, chk2=sChk2)


@app.route('/user/<username>')
def user(username):
    favorite_movies = [
        'The Shawshank Redemption',
        'The Godfather',
        'The Dark Knight',
    ]
    return render_template('user.html', username=username, favorite_movies=favorite_movies)


@app.post('/recommend')
def recommend():
    user = db.session.query(User).first()
    data = request.get_json()
    user_message = data['message']
    new_message = Message(content=user_message, author="user", user=user)
    db.session.add(new_message)
    db.session.commit()

    messages_for_llm = [{
        "role": "system",
        "content": "Eres un chatbot que recomienda películas, te llamas 'Next Moby'. Tu rol es responder recomendaciones de manera breve y concisa. No repitas recomendaciones.",
    }]

    for message in user.messages:
        messages_for_llm.append({
            "role": message.author,
            "content": message.content,
        })

    chat_completion = client.chat.completions.create(
        messages=messages_for_llm,
        model="gpt-4o",
    )

    message = chat_completion.choices[0].message.content

    return {
        'recommendation': message,
        'tokens': chat_completion.usage.total_tokens,
    }
