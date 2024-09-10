import requests


class AnimeDetailsQuery:
    """
    Класс для запроса информации об аниме с сайта MyAnimeList.

    При инициализации класса необходимо предоставить client_id, который используется
    для аутентификации запросов к API MyAnimeList.

    Атрибуты:
        headers (dict): Заголовки для аутентификации запросов к API.

    Методы:
        get_anime_name(name): Возвращает название аниме по заданному запросу.
        get_anime_id(name): Возвращает идентификатор аниме по заданному запросу.
        get_anime_genres(name): Возвращает список жанров аниме по заданному запросу.
    """
    
    def __init__(self, client_id):
        """
        Инициализирует класс с заданным client_id.

        Параметры:
            client_id (str): Client ID для аутентификации запросов к API MyAnimeList.
        """
        self.headers = {'X-MAL-CLIENT-ID': client_id}
    
    def get_anime_id(self, name):
        """
        Осуществляет запрос к API MyAnimeList для получения идентификатора аниме.

        Параметры:
            name (str): Название аниме для поиска.

        Возвращает:
            int: Идентификатор аниме, если запрос успешен.
            None: Если аниме не найдено или произошла ошибка.
        """
        url = f'https://api.myanimelist.net/v2/anime?q={name}&limit=1'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            try:        
                return response.json()['data'][0]['node']['id']                
            except (KeyError, IndexError, TypeError):        
                return None
    
    def get_anime_name(self, name):
        """
        Осуществляет запрос к API MyAnimeList для получения названия аниме.

        Параметры:
            name (str): Название аниме для поиска.

        Возвращает:
            str: Название аниме, если запрос успешен.
            None: Если аниме не найдено или произошла ошибка.
        """
        url = f'https://api.myanimelist.net/v2/anime?q={name}&limit=1'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            try:        
                return response.json()['data'][0]['node']['title']        
            except (KeyError, IndexError, TypeError):        
                return None

    def get_anime_genres(self, name):
        """
        Осуществляет запрос к API MyAnimeList для получения списка жанров аниме.

        Параметры:
            name (str): Название аниме для поиска.

        Возвращает:
            list: Список жанров аниме, если запрос успешен.
            None: Если аниме не найдено или произошла ошибка.
        """

        anime_id = self.get_anime_id(name)
        if anime_id is None:
            return anime_id

        url = f'https://api.myanimelist.net/v2/anime/{anime_id}?fields=genres'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            try:                
                return ', '.join([genre['name'] for genre in response.json()['genres']])
            except (KeyError, IndexError, TypeError):        
                return None
