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
        self.hp = randint(200, 400)
        self.power = randint(30,60)


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
            f"Множитель бонуса: x{self.bonus}\n"
            f"Здоровье: {self.hp}\n"
            f"Сила: {self.power}\n"
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

    def attack(self, enemy):
        if isinstance(enemy, Wizard): # Проверка на то, что enemy является типом данных Wizard (является экземпляром класса Волшебник)
            num = randint(1,5)
            if num == 1:
                    return "Покемон-волшебник применил щит в сражении"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "

class Wizard(Pokemon):
    pass

class Fighter(Pokemon):
    def attack(self, enemy):
        add_damage = randint(5, 15)
        self.power += add_damage
        print(super())
        result = super().attack(enemy)
        self.power -= add_damage
        return result + f"\nБоец применил супер-атаку силой: {add_damage}"