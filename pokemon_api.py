```python
import random
import requests
from typing import Dict, Any

__MAX_POKEMON_ID = 151


def fetch_random_pokemon() -> Dict[str, Any]:
    """Fetch random Pokemon data from PokeAPI with Traditional Chinese names."""

    pokemon_id = random.randint(1, __MAX_POKEMON_ID)

    response = requests.get(
        f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    )
    response.raise_for_status()
    pokemon_data = response.json()

    # Get species information
    species_url = pokemon_data["species"]["url"]
    species_response = requests.get(species_url)
    species_response.raise_for_status()
    species_data = species_response.json()

    # Traditional Chinese Pokemon name
    for name in species_data["names"]:
        if name["language"]["name"].lower() == "zh-hant":
            pokemon_name = name["name"]
            break
    else:
        pokemon_name = pokemon_data["name"].title()

    # Traditional Chinese species / genus
    for genus in species_data["genera"]:
        if genus["language"]["name"].lower() == "zh-hant":
            species_name = genus["genus"]
            break
    else:
        species_name = species_data["genera"][0]["genus"]

    # Remove "寶可夢" from species name
    species_name = species_name.replace("寶可夢", "").strip()

    # Pokemon types
    types = [t["type"]["name"] for t in pokemon_data["types"]]

    # Traditional Chinese type names
    type_translation = {
        "normal": "一般",
        "fire": "火",
        "water": "水",
        "electric": "電",
        "grass": "草",
        "ice": "冰",
        "fighting": "格鬥",
        "poison": "毒",
        "ground": "地面",
        "flying": "飛行",
        "psychic": "超能力",
        "bug": "蟲",
        "rock": "岩石",
        "ghost": "幽靈",
        "dragon": "龍",
        "dark": "惡",
        "steel": "鋼",
        "fairy": "妖精",
    }

    chinese_types = [
        type_translation.get(t, t.title())
        for t in types
    ]

    return {
        "id": str(pokemon_data["id"]).zfill(4),
        "name": pokemon_name,
        "types": ", ".join(chinese_types),
        "species": species_name,
        "height": f'{pokemon_data["height"] / 10} m',
        "weight": f'{pokemon_data["weight"] / 10} kg',
        "artwork": pokemon_data["sprites"]["other"]["official-artwork"]["front_default"]
    }
```
