"""
Author: Bas van der Wielen
"""
import requests, sys, json
from loguru import logger
logger.add(sys.stderr, format="{time} {level} {message}", filter="mealie_client.py", level="DEBUG")

TIMEOUT = 3

class MealieClient():
    """
    Class containing basic recipe interactions.
    """
    def __init__(self, server_ip, server_port, auth_token) -> None:
        self.server = f"{server_ip}:{server_port}"
        self.header = {"Authorization": f"Bearer {auth_token}"}
        url = f"{self.server}/api/groups/self"
        response = requests.get(url, headers=self.header, timeout=TIMEOUT)

        if response.status_code == 200:
            logger.info('We can connect to Mealie!')
        else:
            logger.error('Could not connect to Mealie server!')

    def recipe_create(self, title: str):
        """https://docs.mealie.io/api/redoc/#tag/Recipe:-CRUD/operation/create_one_api_recipes_post"""

        json_data = {
            'name': title
        }

        response = requests.post(
            url=f"{self.server}/api/recipes",
            json = json_data,
            headers=self.header,
            timeout=TIMEOUT
        )

        logger.debug(f"status: {response.status_code}, response: {response.json()}")

        #TODO Error handling

        return response.json()

    def recipe_get(self, slug:str):
        """https://docs.mealie.io/api/redoc/#tag/Recipe:-CRUD/operation/get_one_api_recipes__slug__get"""

        response = requests.get(
            url=f"{self.server}/api/recipes/{slug}",
            headers=self.header,
            timeout=TIMEOUT
        )

        logger.debug(f"status: {response.status_code}, response: {response.json()}")

        #TODO Error handling

        return response.json()

    def recipe_delete(self, slug):
        """https://docs.mealie.io/api/redoc/#tag/Recipe:-CRUD/operation/delete_one_api_recipes__slug__delete"""

        response = requests.delete(
            url=f"{self.server}/api/recipes/{slug}",
            headers=self.header,
            timeout=TIMEOUT
        )

        logger.debug(f"status: {response.status_code}")

    def recipe_update(self, slug, data:dict):
        """https://docs.mealie.io/api/redoc/#tag/Recipe:-CRUD/operation/update_one_api_recipes__slug__put"""

        response = requests.patch(
            url=f"{self.server}/api/recipes/{slug}",
            json=data,
            headers=self.header,
            timeout=TIMEOUT
        )

        logger.debug(f"status: {response.status_code}: {response.json()}")

if __name__ == '__main__':
    mealie_server_ip = "http://10.0.0.1"
    mealie_server_port = 9925
    client_secret = '1234567890abcdef'

    client = MealieClient(mealie_server_ip, mealie_server_port, client_secret)

    client.recipe_create('test recept')
    client.recipe_get('test-recept')

    update = {"description": "Dit is een test recept!",}
    client.recipe_update('test-recept', update)

    client.recipe_delete('test-recept')