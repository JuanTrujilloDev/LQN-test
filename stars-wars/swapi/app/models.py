from django.db import models
from model_utils.models import TimeStampedModel


class SimpleNameModel(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Planet(TimeStampedModel, SimpleNameModel):
    """ Planetas del universo de Star Wars """

    rotation_period = models.CharField(max_length=40, blank=True)
    orbital_period = models.CharField(max_length=40, blank=True)
    diameter = models.CharField(max_length=40, blank=True)
    climate = models.CharField(max_length=40, blank=True)
    gravity = models.CharField(max_length=40, blank=True)
    terrain = models.CharField(max_length=40, blank=True)
    surface_water = models.CharField(max_length=40, blank=True)
    population = models.CharField(max_length=40, blank=True)

    class Meta:
        db_table = 'planet'


class People(TimeStampedModel, SimpleNameModel):
    """ Personajes del universo de Star Wars 
    
    
    Attributes:

    height: CharField(Might need to recieve only numbers in the input field)
    mass: CharField(Same as Height)
    hair_color: CharField, uses a choices argument to select only from hair_color_options
    skin_color: CharField, it is open to the user, it should be changed to options aswell
    eye_color: Charfield, applies choices from eye_color_options.
    birth_year: Charfield, it can be changed to DateField.
    gender: Charfield.
    home_world: ForeignKey, references Planets model.
    
    """
    height = models.CharField(max_length=16, blank=True)
    mass = models.CharField(max_length=16, blank=True)
    hair_color_options = [
        ('Black', 'BLACK'),
        ('Brown', 'BROWN'),
        ('Blonde', 'BLONDE'),
        ('Red', 'RED'),
        ('White', 'WHITE'),
        ('Bald', 'BALD')
        
    ]
    hair_color = models.CharField(max_length=32, blank=True, choices=hair_color_options, default="Bald")
    skin_color = models.CharField(max_length=32, blank=True)

    eye_color_options = [
        ('Black','BLACK'), 
        ('Brown','BROWN'), 
        ('Yellow','YELLOW'), 
        ('Red','RED'), 
        ('Green', 'GREEN'),
        ('Purple', 'PURPLE'), 
        ('Unknown' , 'UNKNOWN')
    ]


    eye_color = models.CharField(max_length=32, blank=True, choices=eye_color_options, default="Unknown")
    birth_year = models.CharField(max_length=16, blank=True)
    gender = models.CharField(max_length=64, blank=True)
    home_world = models.ForeignKey(Planet, on_delete=models.CASCADE, related_name='inhabitants')

    class Meta:
        db_table = 'people'
        verbose_name_plural = 'people'


class Director(SimpleNameModel):
    """ Directores de películas"""

    class Meta:
        db_table = 'director'


class Producer(SimpleNameModel):
    """ Productores de películas"""

    class Meta:
        db_table = 'producer'


class Film(TimeStampedModel):
    title = models.CharField(max_length=100)
    episode_id = models.PositiveSmallIntegerField()
    opening_crawl = models.TextField(max_length=1000)
    release_date = models.DateField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='films')
    producer = models.ManyToManyField(Producer, related_name='films')
    characters = models.ManyToManyField(People, related_name='films', blank=True)
    planets = models.ManyToManyField(Planet, related_name='films', blank=True)

    class Meta:
        db_table = 'film'

    def __str__(self):
        return self.title
