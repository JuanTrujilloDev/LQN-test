from .models import Film, People

def generic_model_mutation_process(model, data, id=None, commit=True):
    """
    Funcion generic_model_mutation_process

    * Recibe un modelo cualquiera, informacion para llenar el modelo y un id.
    
    * Si el id es None solo crea el objeto a partir del modelo y posteriormente lo guarda.

    * En caso de que traiga id trae el objeto de la base de datos, y actualiza sus datos.

    POR LO TANTO LA FUNCION NOS SIRVE TANTO PARA CREAR O EDITAR CUALQUIER MODELO.
    
    NOTA:

    LO UNICO INVIABLE DE LA FUNCION ES QUE NO DEFINIMOS QUE ATRIBUTOS SE DEBEN INGRESAR, 
    POR LO QUE PUEDEN ENTRAR DATOS INCOMPLETOS, ERRONEOS O REDUNDANTES.

    """
    if id:
        item = model.objects.get(id=id)
        try:
            del data['id']
        except KeyError:
            # Sacar el id por si envían el data tal cual llega.
            pass

        for field, value in data.items():
            setattr(item, field, value)

    else:
        item = model(**data)
        # TODO: Verificaciones, auto_ids, hashing, asserts, etc.

    if commit:
        item.save()

    return item


def manageFilms(ids, kw, raw_id):
    '''
    Funcion manageFilms

    Recibe los ids de las peliculas, los kwargs del metodo POST y el id de la persona en caso de que exista.

    La funcion extraera las peliculas del usuario si existe, y las comparara con las que actualiza.
    
    De igual manera si de entrada nos trae los ids de las peliculas a agregar anade a la persona a la pelicula.

    NOTA:

    - Si la funcion recibe peliculas nuevas las comparara con las antiguas.
    - En caso de que en los ids de las peliculas nuevas no este las que ya estaban afiliadas se eliminaran.
    - Asi se comparan las peliculas y se registran.
    - Al final usamos la funcion auxiliar generic_model_mutation_process para actualizar o anadir el usuario.
    '''
    people = generic_model_mutation_process(**kw)
    if raw_id:
        old_movies = Film.objects.filter(characters__id = kw['id']).all()
        if old_movies and ids:
            new_movies = [Film.objects.filter(id=pk) for pk in ids if Film.objects.filter(id=pk)]
            for old_movie in old_movies:
                if old_movie not in new_movies:
                    old_movie.characters.remove(people)

    if ids:
        new_movies = [Film.objects.filter(id=pk) for pk in ids if Film.objects.filter(id=pk)]
        for movie in new_movies:
            movie[0].characters.add(people)



