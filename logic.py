from random import randint
import requests


class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = randint(1, 1000)
        self.img = self.get_img()
        self.name = self.get_name()
        Pokemon.pokemons[pokemon_trainer] = self

    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['sprites']['front_shiny']
        return "Pokemon img"

    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['forms'][0]['name']
        return "Pokemon"

    def info(self):
        return f"Имя твоего покемона: {self.name}"

    def show_img(self):
        return self.img


