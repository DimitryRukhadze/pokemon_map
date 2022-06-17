from django.db import models


class Pokemon(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Имя'
    )
    title_en = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Имя на англ.'
    )
    title_jp = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Имя на яп.'
    )
    image = models.ImageField(
        null=True,
        blank=True,verbose_name='Изображение'
    )
    description = models.TextField(
        blank=True,
        default='',
        verbose_name='Описание'
    )
    evolves_from = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Эволюционировал из',
        related_name='evolver'
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='Тип покемона',
        related_name='poke_type'
    )
    lat = models.FloatField(
        verbose_name='Широта'
    )
    lon = models.FloatField(
        verbose_name='Долгота'
    )
    appeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Когда появился'
    )
    disappeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Когда исчезнет'
    )
    level = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Уровень'
    )
    health = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Здоровье'
    )
    strength = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Сила'
    )
    defence = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Защита'
    )
    stamina = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Выносливость'
    )

    def __str__(self):
        return f'{self.pokemon.title} {self.id}'