from turtle import home
import graphene
from django.db.models import Q
import graphene_django
from graphene_django.filter import DjangoFilterConnectionField
from django_filters import OrderingFilter, FilterSet
from graphene_django.types import DjangoObjectType
from graphql_relay.node.node import from_global_id

from .models import Planet, People, Film, Director, Producer
from .utils import generic_model_mutation_process, manageFilms


class PlanetNode(DjangoObjectType):
    class Meta:
        model = Planet
        interfaces = (graphene.relay.Node,)
        filter_fields = {'name': ['iexact', 'icontains', 'contains', 'exact'], }

#Esta mutacion agrega o actualiza planteas.
#Depende si le pasamos el id en la data.
class AddOrUpdatePlanet(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=False)
        name = graphene.String(required=True)
        rotation_period = graphene.String(required=False)
        orbital_period = graphene.String(required=False)
        diameter = graphene.String(required=False)
        climate = graphene.String(required=False)
        gravity = graphene.String(required=False)
        terrain = graphene.String(required=False)
        surface_water = graphene.String(required=False)
        population = graphene.String(required=False)

    planet = graphene.Field(PlanetNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, **kwargs):
        # TODO: Por que args es None?
        # No estoy seguro de esta respuesta pero creo que es debido a que al hacer las queries
        # se toman por defecto pares de key, values kwargs (en el JSON Data) y por lo tanto los args
        # No se definen los args


        # TODO: Para que sirve el context?
        # El execution context nos sirve para traer informacion como el usuario que se encuentra logeado,
        # el acceso de la base de datos, este es compartido por todos los resolvers


        # kwargs recibe toda la data que se envia desde el mutation
        print(context)

        raw_id = kwargs.get('id', None)
        kw = {'model': Planet, 'data': kwargs}
        if raw_id:
            kw['id'] = from_global_id(raw_id)[1]
        planet = generic_model_mutation_process(**kw)
        return AddOrUpdatePlanet(planet=planet)







class DirectorNode(DjangoObjectType):
    class Meta:
        model = Director
        interfaces = (graphene.relay.Node,)
        filter_fields = ['name']


class AddDirector(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=False)
        name = graphene.String(required=True)

    director = graphene.Field(DirectorNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, **kwargs):
        raw_id = kwargs.get('id', None)

        kw = {'model': Director, 'data': kwargs}
        if raw_id:
            kw['id'] = from_global_id(raw_id)[1]
        director = generic_model_mutation_process(**kw)
        return AddDirector(director=director)


class ProducerNode(DjangoObjectType):
    class Meta:
        model = Producer
        interfaces = (graphene.relay.Node,)
        filter_fields = ['name']


class AddProducer(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=False)
        name = graphene.String(required=True)

    producer = graphene.Field(ProducerNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, **kwargs):
        raw_id = kwargs.get('id', None)

        kw = {'model': Producer, 'data': kwargs}
        if raw_id:
            kw['id'] = from_global_id(raw_id)[1]
        producer = generic_model_mutation_process(**kw)
        return AddProducer(producer=producer)


class ProducerInput(graphene.InputObjectType):
    """ Esto se puede utilizar dentro del class Input del AddProducer """

    class Meta:
        model = Producer

    id = graphene.ID()
    name = graphene.String()


class FilmNode(DjangoObjectType):
    class Meta:
        model = Film
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'title': ['iexact', 'icontains', 'contains', 'exact'],
            'episode_id': ['exact'],
            'release_date': ['exact']
        }


class AddFilm(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=False)
        title = graphene.String(required=True)
        episode_id = graphene.Int(required=True)
        opening_crawl = graphene.String(required=False)
        release_date = graphene.Date()
        director = graphene.ID(required=False)
        producer = graphene.List(of_type=ProducerInput)

    film = graphene.Field(FilmNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, **kwargs):
        raw_id = kwargs.get('id', None)

        # TODO: trabajar con el id de graphene.
        director_id = kwargs.pop('director')

        producers = kwargs.pop('producer')
        print(producers)

        kw = {'model': Film, 'data': kwargs}
        if raw_id:
            kw['id'] = from_global_id(raw_id)[1]
        film = generic_model_mutation_process(commit=False, **kw)

        if director_id:
            film.director_id = director_id

        film.save()

        if producers:
            q = Q()
            for producer_name in producers:
                q |= Q(name__iexact=producer_name['name'])
            producer_instances = [producer for producer in Producer.objects.filter(q)]
            film.producer.set(producer_instances)

        return AddFilm(film=film)


class GenderChoices(graphene.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class PeopleNode(DjangoObjectType):
    class Meta:
        model = People
        interfaces = (graphene.relay.Node,) 
        #TODO FILTRAR ENUMS
        fields = ["name", "height", "mass", "gender", "hair_color", "skin_color", "eye_color", "birth_year",
                    "home_world"]
        filter_fields = {
            'id' : ['exact', 'istartswith'],
            'name' : ['exact', 'istartswith'],
            'gender' : ['exact', 'iexact']
        }
        filter_order_by = ['name']
        
    

class AddOrUpdatePeople(graphene.relay.ClientIDMutation):
    """
    Clase AddOrUpdate PEOPLE

    Le modifique el nombre debido a que aqui directamente tambien podemos actualizar los modelos
    haciendo uso del generi_model_mutation_process

    En los inputs tenemos todos los atributos del modelo Persona.

    Van desde: id - film_ids

    Los foreign keys los manejamos con el id.

    """
    class Input:
        id = graphene.ID(required=False)
        name = graphene.String(required=True)
        height = graphene.String(required=False)
        mass = graphene.String(required=False)
        hair_color = graphene.String(required=False)
        skin_color = graphene.String(required=False)
        eye_color = graphene.String(required=False)
        birth_year = graphene.String(required=False)
        gender = graphene.String(required=False)

        home_world_id = graphene.ID(required=True)
        
        #Anadiendo campo film al mutation

        film_ids = graphene.List(graphene.ID,required=False)

    people = graphene.Field(PeopleNode)
    planet = graphene.Field(PlanetNode)
    film = graphene.Field(FilmNode)

  #  @classmethod
  #  def mutate_and_get_payload(cls, args, context, **kwargs):
  #      raw_id = kwargs.get('id', None)
#
#        kw = {'model': People, 'data': kwargs}
#        if raw_id:
#            kw['id'] = from_global_id(raw_id)[1]
#        people = generic_model_mutation_process(**kw)
#        return AddPeople(people=people)

    #CREANDO MI PROPIA MUTACON PARA ANADIR PEOPLE

    @classmethod
    def mutate_and_get_payload(cls, args, context, **kwargs):
        """
        Funcion mutate and get payload

        Reutilizamos la funcion hecha en addplanets.

        1. Traemos los kwargs con el json de la persona a crear.

        2. Si no trae id lo dejamos como None y por lo tanto se creara la persona.

        3. De lo contrario editara los campos brindados de esa persona.

        4. Para anadir o editar 
        
        """
        raw_id = kwargs.get('id', None)
        film_ids = kwargs.get('film_ids', None)
        kw = {'model': People, 'data': kwargs}

        
        # Extraemos el id en caso de que exista    
        if raw_id:
            kw['id'] = from_global_id(raw_id)[1] #from_global_id traduce el id de GraphQL a el int=pk de sqlite (En este caso)
            print(kw['id'])
        # Si mandamos films extraemos los id's de los films
        # Y ejecutamos el manage Films el cual retorna la persona
        if film_ids:
            ids = [ids for ids in kw['data'].pop('film_ids')]
            people = manageFilms(ids, kw, raw_id)
        #Si no utilizamos la funcion auxiliar para crear las personas.
        else:
            people = generic_model_mutation_process(**kw)


        # Al final retornamos el usuario.
        return AddOrUpdatePeople(people=people)
        





class Query(graphene.ObjectType):
    class GenreEnum(graphene.Enum):
        YES = 1
        NO = 2

    planet = graphene.relay.Node.Field(PlanetNode)
    all_planets = DjangoFilterConnectionField(PlanetNode)

    people = graphene.relay.Node.Field(PeopleNode)
    all_people = DjangoFilterConnectionField(PeopleNode)

    film = graphene.relay.Node.Field(FilmNode)
    all_films = DjangoFilterConnectionField(FilmNode)

    director = graphene.relay.Node.Field(DirectorNode)
    all_directors = DjangoFilterConnectionField(DirectorNode)

    producer = graphene.relay.Node.Field(ProducerNode)
    all_producers = DjangoFilterConnectionField(ProducerNode)


class Mutation(graphene.ObjectType):
    add_or_update_planet = AddOrUpdatePlanet.Field()  # TODO: debería tener 1 para add y otro para update?
                                                      # ANS: No, con el add planet si le pasamos el ID podemos actualizarlo.
    add_director = AddDirector.Field()

    add_producer = AddProducer.Field()

    add_people = AddOrUpdatePeople.Field()

    add_film = AddFilm.Field()
