def buzzBazz():
    """
    buzzBazz() function.
    
    Imprimira los numeros del 0 al 100.
    Adicionalmente agregara a la linea buzz si es par y bazz si es multiplo de 5

    *No retorna ningun valor o variable*
    """

    for i in range(0,101):
        output = str(i)

        if i % 2 == 0:
            output += "buzz"

        if i % 5 == 0:
            output += "bazz"

        print(output)

buzzBazz()