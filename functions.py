import re
 
 
def FindURLs(string):
# ---------------------------------------------------------------------------------------------------------------
# Concatena las preferencias del usuario  
# ---------------------------------------------------------------------------------------------------------------
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]

def Preferences(sFavMovies, sFavSeries, sFavKinds):
# ---------------------------------------------------------------------------------------------------------------
# Concatena las preferencias del usuario  
# ---------------------------------------------------------------------------------------------------------------
    sMsg = ''
    if len(sFavMovies) > 0:
        sMsg = f'películas favoritas: {sFavMovies}'

    if len(sFavSeries) > 0:
        if len(sMsg) > 0:
            sMsg += '; '

        sMsg += f'series favoritas: {sFavSeries}'

    if len(sFavKinds) > 0:
        if len(sMsg) > 0:
            sMsg += '; '

        sMsg += f'géneros favoritos de películas y series: {sFavKinds}'

    return sMsg

def getTools():
# ---------------------------------------------------------------------------------------------------------------
# Establece las funciones para function calling  
# ---------------------------------------------------------------------------------------------------------------
    tools = [
        {
            'type': 'function',
            'function': {
                "name": "where_to_watch",
                "description": "Returns a list of platforms where a specified movie can be watched.",
                "parameters": {
                    "type": "object",
                    "required": [
                        "name"
                    ],
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the movie to search for"
                        }
                    },
                    "additionalProperties": False
                }
            },
        },
        {
            'type': 'function',
            'function': {
                "name": "search_movie_or_tv_show",
                "description": "Returns information about a specified movie or TV show, like overview, poster, vote average.",
                "parameters": {
                    "type": "object",
                    "required": [
                        "name"
                    ],
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the movie/tv show to search for"
                        }
                    },
                    "additionalProperties": False
                }
            },
        },
        {
            'type': 'function',
            'function': {
                "name": "search_trailer",
                "description": "Returns information about trailer of a specified movie.",
                "parameters": {
                    "type": "object",
                    "required": [
                        "name"
                    ],
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the movie for which you are looking for the trailer"
                        }
                    },
                    "additionalProperties": False
                }
            },
        }
    ]

    return tools
