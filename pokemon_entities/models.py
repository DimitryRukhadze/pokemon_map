from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField(blank=True)
    lon = models.FloatField(blank=True)
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
    level = models.IntegerField(blank=True)
    health = models.IntegerField(blank=True)
    strength = models.IntegerField(blank=True)
    defence = models.IntegerField(blank=True)
    stamina = models.IntegerField(blank=True)
