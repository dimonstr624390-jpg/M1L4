from random import choices, randint
import requests


class Pokemon:
    pokemons = {}

    RARITIES = {
        "Обычный": {
            "weight": 70,
            "bonus": 1,
        },
        "Редкий": {
            "weight": 20,
            "bonus": 2,
        },
        "Эпический": {
            "weight": 9,
            "bonus": 5,
        },
        "Легендарный": {
            "weight": 1,
            "bonus": 10,
        },
    }

    SUPER_BONUS = 100

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = randint(1, 1000)

        rarity_names = list(self.RARITIES.keys())
        rarity_weights = [
            item["weight"]
            for item in self.RARITIES.values()
        ]

        self.rarity = choices(
            rarity_names,
            weights=rarity_weights,
            k=1
        )[0]

        self.bonus = self.RARITIES[self.rarity]["bonus"]
        self.img = None
        self.name = f"Покемон №{self.pokemon_number}"

        self.load_data()

        self.super_bonus = (
            self.SUPER_BONUS
            if self.rarity == "Легендарный"
            else 0
        )

        Pokemon.pokemons[pokemon_trainer] = self

    def load_data(self):
        url = (
            "https://pokeapi.co/api/v2/pokemon/"
            f"{self.pokemon_number}"
        )

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            self.name = data["name"].capitalize()

            sprites = data.get("sprites", {})
            self.img = (
                sprites.get("front_shiny")
                or sprites.get("front_default")
            )

        except (
            requests.RequestException,
            ValueError,
            KeyError,
        ):
            pass

    def info(self):
        result = (
            f"Ваш покемон: {self.name}\n"
            f"Редкость: {self.rarity}\n"
            f"Множитель бонуса: x{self.bonus}"
        )

        if self.rarity == "Легендарный":
            result += (
                "\n\nПолучен супербонус."
                f"\nДополнительная награда: "
                f"{self.super_bonus} очков."
            )

        elif self.rarity == "Эпический":
            result += "\nПолучен дополнительный бонус."

        return result

    def show_img(self):
        return self.img