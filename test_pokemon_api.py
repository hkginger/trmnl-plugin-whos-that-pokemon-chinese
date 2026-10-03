import pytest
from unittest.mock import Mock, patch

from pokemon_api import fetch_random_pokemon


@pytest.fixture
def mock_pokemon_response():
    return {
        "id": 25,
        "name": "pikachu",
        "types": [
            {
                "type": {
                    "name": "electric"
                }
            }
        ],
        "species": {
            "name": "pikachu",
            "url": "https://pokeapi.co/api/v2/pokemon-species/25"
        },
        "height": 4,
        "weight": 60,
        "sprites": {
            "other": {
                "official-artwork": {
                    "front_default": "https://example.com/pikachu.png"
                }
            }
        }
    }


@pytest.fixture
def mock_species_response():
    return {
        "name": "pikachu",
        "names": [
            {
                "name": "Pikachu",
                "language": {
                    "name": "en"
                }
            },
            {
                "name": "皮卡丘",
                "language": {
                    "name": "zh-Hant"
                }
            }
        ],
        "genera": [
            {
                "genus": "Mouse Pokémon",
                "language": {
                    "name": "en"
                }
            },
            {
                "genus": "鼠寶可夢",
                "language": {
                    "name": "zh-Hant"
                }
            }
        ]
    }


def test_fetch_random_pokemon_returns_correct_response(
    mock_pokemon_response,
    mock_species_response
):
    with patch("requests.get") as mock_get:
        mock_get.side_effect = [
            Mock(
                json=lambda: mock_pokemon_response,
                raise_for_status=lambda: None
            ),
            Mock(
                json=lambda: mock_species_response,
                raise_for_status=lambda: None
            )
        ]

        with patch("random.randint", return_value=25):
            result = fetch_random_pokemon()

    assert result["id"] == "0025"
    assert result["name"] == "皮卡丘"
    assert result["types"] == "電"
    assert result["species"] == "鼠"
    assert result["height"] == "0.4 m"
    assert result["weight"] == "6.0 kg"
    assert result["artwork"] == "https://example.com/pikachu.png"


def test_fetch_random_pokemon_falls_back_to_english_name(
    mock_pokemon_response
):
    species_response_no_chinese = {
        "name": "pikachu",
        "names": [
            {
                "name": "Pikachu",
                "language": {
                    "name": "en"
                }
            }
        ],
        "genera": [
            {
                "genus": "Mouse Pokémon",
                "language": {
                    "name": "en"
                }
            }
        ]
    }

    with patch("requests.get") as mock_get:
        mock_get.side_effect = [
            Mock(
                json=lambda: mock_pokemon_response,
                raise_for_status=lambda: None
            ),
            Mock(
                json=lambda: species_response_no_chinese,
                raise_for_status=lambda: None
            )
        ]

        with patch("random.randint", return_value=25):
            result = fetch_random_pokemon()

    assert result["name"] == "Pikachu"
    assert result["species"] == "Mouse Pokémon"


def test_fetch_random_pokemon_calls_correct_endpoints(
    mock_pokemon_response,
    mock_species_response
):
    with patch("requests.get") as mock_get, \
         patch("random.randint") as mock_randint:

        mock_get.side_effect = [
            Mock(
                json=lambda: mock_pokemon_response,
                raise_for_status=lambda: None
            ),
            Mock(
                json=lambda: mock_species_response,
                raise_for_status=lambda: None
            )
        ]

        mock_randint.return_value = 25

        fetch_random_pokemon()

        assert mock_randint.called
        assert mock_get.call_count == 2

        first_url = mock_get.call_args_list[0].args[0]
        second_url = mock_get.call_args_list[1].args[0]

        assert first_url == "https://pokeapi.co/api/v2/pokemon/25"
        assert second_url == "https://pokeapi.co/api/v2/pokemon-species/25"


def test_fetch_random_pokemon_handles_lowercase_language_code(
    mock_pokemon_response
):
    species_response = {
        "name": "pikachu",
        "names": [
            {
                "name": "皮卡丘",
                "language": {
                    "name": "zh-hant"
                }
            }
        ],
        "genera": [
            {
                "genus": "鼠寶可夢",
                "language": {
                    "name": "zh-hant"
                }
            }
        ]
    }

    with patch("requests.get") as mock_get:
        mock_get.side_effect = [
            Mock(
                json=lambda: mock_pokemon_response,
                raise_for_status=lambda: None
            ),
            Mock(
                json=lambda: species_response,
                raise_for_status=lambda: None
            )
        ]

        with patch("random.randint", return_value=25):
            result = fetch_random_pokemon()

    assert result["name"] == "皮卡丘"
    assert result["species"] == "鼠"
