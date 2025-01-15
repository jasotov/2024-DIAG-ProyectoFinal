from simplejustwatchapi.justwatch import search as justwatch_search
import tmdbsimple as tmdb
from dotenv import load_dotenv
from os import getenv

load_dotenv()
tmdb.API_KEY = getenv('TMDB_API_KEY')


def search(movie_name):
    search = tmdb.Search()
    response = search.multi(query=movie_name, language='es-CL')

    if not search.results:
        return None

    return search.results[0]


def search_platforms(movie_name):
    results = justwatch_search(movie_name, "CL", "es")
    platforms = []

    if not results:
        return platforms

    for offer in results[0].offers:
        platforms.append({
            'name': offer.package.name,
            'icon': offer.package.icon,
            'url': offer.url,
        })

    return platforms

# def get_overview(movie_name):
#     # Buscar la película por nombre
#     search = tmdb.Search()
#     response = search.multi(query=movie_name, language='es-CL')

#     if not search.results:
#         return None

#     overview = response['results'][0]['overview']

#     return watch_providers, poster_url, puntuacion, descripcion

# def get_overview(movie_name):
#     # Buscar la película por nombre
#     search = tmdb.Search()
#     response = search.multi(query=movie_name, language='es-CL')

#     if not response['results']:
#         return None, None, None, None

#     # Obtener el ID de la primera película encontrada
#     movie_id = response['results'][0]['id']
#     poster_path = response['results'][0]['poster_path']
#     puntuacion = response['results'][0]['vote_average']
#     descripcion = response['results'][0]['overview']

#     # Obtener los proveedores de visualización para la película
#     movie = tmdb.Movies(movie_id)
#     providers_response = movie.watch_providers()

#     if 'results' in providers_response and 'CL' in providers_response['results']:
#         watch_providers = providers_response['results']['CL']['flatrate']
#     else:
#         watch_providers = None

#     # Construir la URL del póster
#     poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

#     return watch_providers, poster_url, puntuacion, descripcion
