"""
Pokemon.py

This pokemon script will recieve a file with pokemon names.

It will return the max possible last letter first letter combination with them.


"""



file_name = input("Write file name: ")
with open(file_name, 'r') as fh:
    pokemons = list()

    for line in fh.readlines():
        for word in line.rstrip().strip().split():
            pokemons.append(word) 


# We will group the pokemon names by letter so we can make each pathing easily
pokemons = set(pokemons)
d = dict()

for i in pokemons:
    if i[0] not in d.keys() :
        d[i[0]] = set()
    d[i[0]].add(i)

d = dict(sorted(d.items()))



def getRoutes(pokemon):
    """
    getRoutes Function

    It will recieve a pokemon name and will return a set of consecutive names

    Each name will pass through a filter going in a tree finding names with 
    the first letter of the last letter of the previous

    If we get coincidences we will append the name to a list if not we will pass only the name

    """
    routes = []
    last_char = pokemon[-1][-1] #Las character of the name
    val = d.get(last_char) #Viewing if the letter has coincidences
    if val:
        options =  d[last_char] - set(pokemon) #If it does we store the coincidences but we will delete any item we already used.
        if options:
            for option in options: #For each coincidence we will go through it childs 
                routes.append(getRoutes(pokemon+[option]))#Recursion will let us go through all the pokenames

            return max(routes, key=len) #When we end finding coincidences we will return the longest round with that name

        else:
            return pokemon #If we don't find anything we will return the pokemon.
    else:
        return pokemon

result = max([getRoutes([pokemon]) for pokemon in pokemons], key = len)
    
#Finally we will show the result

print("Longest consecutive last letter first letter names:", len(result))
print("Consecutive names:", result)











