from movies import search, search_platforms, search_youtube
from openai import OpenAI
from models import User
from functions import Preferences


def build_prompt(user: User, context: str):
    system_prompt = "Eres un chatbot que recomienda películas y series, te llamas 'Verflix'. Tu rol es responder recomendaciones de manera breve y concisa. No repitas recomendaciones."
    system_prompt += 'Si te preguntan por trailer o video prefiere utilizar tool_calls para obtener la información'

    sPreferences = Preferences(user.fav_movies,user.fav_series,user.kind_movies)
    if len(sPreferences) > 0:
        system_prompt += f'Para recomendar, considera los gustos del usuario que te está preguntando, que son los siguientes: {sPreferences}'

    if context:
        system_prompt += f'Además considera el siguiente contenido: {context}\n'

    return system_prompt


def where_to_watch(client: OpenAI, search_term: str, user: User):
    movie_or_tv_show = search_platforms(search_term)

    if not movie_or_tv_show:
        return f'No estoy seguro de dónde puedes ver esta película o serie, pero quizas puedes revisar en JustWatch: https://www.justwatch.com/cl/buscar?q={search_term}'

    system_prompt = build_prompt(user, str(movie_or_tv_show))

    messages_for_llm = [{"role": "system", "content": system_prompt}]

    for message in user.messages:
        messages_for_llm.append({
            "role": message.author,
            "content": message.content,
        })

    chat_completion = client.chat.completions.create(
        messages=messages_for_llm,
        model="gpt-4o",
        temperature=1,
    )

    return chat_completion.choices[0].message.content


def search_movie_or_tv_show(client: OpenAI, search_term: str, user: User):
    movie_or_tv_show = search(search_term)

    if movie_or_tv_show:
        system_prompt = build_prompt(user, str(movie_or_tv_show))
    else:
        system_prompt = build_prompt(user, '')

    messages_for_llm = [{"role": "system", "content": system_prompt}]

    for message in user.messages:
        messages_for_llm.append({
            "role": message.author,
            "content": message.content,
        })

    chat_completion = client.chat.completions.create(
        messages=messages_for_llm,
        model="gpt-4o",
        temperature=1,
    )

    return chat_completion.choices[0].message.content

def search_trailer(client: OpenAI, search_term: str, user: User):
    trailer = search_youtube(search_term)

    # if trailer:
    #     return trailer

    if trailer:
        system_prompt = build_prompt(user, str(trailer))
    else:
        system_prompt = build_prompt(user, '')

    messages_for_llm = [{"role": "system", "content": system_prompt}]

    for message in user.messages:
        messages_for_llm.append({
            "role": message.author,
            "content": message.content,
        })

    chat_completion = client.chat.completions.create(
        messages=messages_for_llm,
        model="gpt-4o",
        temperature=1,
    )

    return chat_completion.choices[0].message.content
