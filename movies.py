from simplejustwatchapi.justwatch import search as justwatch_search
import tmdbsimple as tmdb
from googleapiclient.discovery import build
from dotenv import load_dotenv
from os import getenv

load_dotenv()
tmdb.API_KEY = getenv('TMDB_API_KEY')


def search(movie_name):
    search = tmdb.Search()
    response = search.multi(query=movie_name, language='es-CL')

    if not search.results:
        return None
    print(search.results[0])

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

# def get_movie_trailer(movie_name):
#     search = tmdb.Search()
#     response = search.movie(query=movie_name)
    
#     if response['results']:
#         try:
#             movie_id = response['results'][0]['id']
#             movie = tmdb.Movies(movie_id)
#             videos = movie.videos()
            
#             for video in videos['results']:
#                 if video['type'] == 'Trailer' and video['site'] == 'YouTube':
#                     return f"https://www.youtube.com/watch?v={video['key']}"
#         except:
#             return "No se encontró el tráiler."
    
#     return "No se encontró el tráiler."

DEVELOPER_KEY = getenv('DEVELOPER_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def search_youtube(movie_name):
    try:
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

        search_response = youtube.search().list(
                            q=movie_name + ' trailer',
                            part='id,snippet',
                            maxResults=3,
                            type='video'
                        ).execute()

        #print(search_response)

        sMsg = ''
        for search_result in search_response.get('items', []):

            #print(search_result)

            if search_result['id']['kind'] == 'youtube#video':
                sMsg = f'El tráiler de la película {movie_name} está disponible en Youtube (https://www.youtube.com/watch?v={search_result["id"]["videoId"]})'
                #print(sMsg)

                return sMsg

        return 'El tráiler de la película {movie_name} no encontrado'
    except:
        return 'El tráiler de la película {movie_name} no encontrado'
