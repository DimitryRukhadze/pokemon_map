import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lt=timezone.localtime(),
        disappeared_at__gt=timezone.localtime()
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemon_entities:
        entity_img_uri = request.build_absolute_uri(entity.pokemon.image.url)
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            entity_img_uri
        )

    poke_models = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in poke_models:
        image_uri = request.build_absolute_uri(pokemon.image.url)
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': image_uri,
            'title_ru': pokemon.title,
        })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):

    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    pokemon_img_uri = request.build_absolute_uri(pokemon.image.url)
    previous_evolution = None
    if pokemon.evolves_from:
        previous_evolution = {
            "title_ru": pokemon.evolves_from.title,
            "pokemon_id": pokemon.evolves_from.id,
            "img_url": request.build_absolute_uri(
                pokemon.evolves_from.image.url
                )
        }

    try:
        successor = pokemon.evolver.get(evolves_from=pokemon)
        next_evolution = {
            "title_ru": successor.title,
            "pokemon_id": successor.id,
            "img_url": request.build_absolute_uri(successor.image.url)
        }
    except ObjectDoesNotExist:
        next_evolution = None

    pokemon_specs = {
        "pokemon_id": pokemon.id,
        "title_ru": pokemon.title,
        "title_en": pokemon.title_en,
        "title_jp": pokemon.title_jp,
        "description": pokemon.description,
        "img_url": pokemon_img_uri,
        "previous_evolution": previous_evolution,
        "next_evolution": next_evolution
    }

    requested_pokemons = PokemonEntity.objects.filter(pokemon=pokemon)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemons:
        entity_img_uri = request.build_absolute_uri(
            pokemon_entity.pokemon.image.url
            )
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            entity_img_uri
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_specs
    })
