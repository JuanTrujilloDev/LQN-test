import json

from graphene_django.utils.testing import GraphQLTestCase
from swapi.schema import schema

class QueryAllTestCase(GraphQLTestCase):
    fixtures = ['app/fixtures/unittest.json'] #Data que sera cargada a la BD -> Son 87 personas
    GRAPHQL_URL = '/graphql/'
    GRAPHQL_SCHEMA = schema
    print("----------------------------TESTING NOTES-----------------------------")


    def test_add_mutation(self):
        response = self.query(

        '''
           mutation{
                addPeople(input:{
                name:"Luke Skywalker"
                homeWorldId:"1"
                height : "172"
                mass: "77", 
                hairColor: "blond"
                skinColor: "fair" 
                eyeColor: "blue" 
                birthYear: "19BBY",
                gender: "male" 
                }) {
                people{
                    name
                    id
                }
                }

}
        '''
        )
        content = json.loads(response.content)["data"]["addPeople"]["people"]["name"]
        self.assertResponseNoErrors(response)
        self.assertEqual("Luke Skywalker", content)



    def test_all_query(self):
        
        response = self.query(
        '''
            query{
                allPeople(id:""){
                    edges{
                        node{
                            id
                            name
                        }
                    }
                }
            }

        '''
        )
        cantidad = len(json.loads(response.content)['data']['allPeople']['edges'])
        persona_update = json.loads(response.content)['data']['allPeople']['edges'][0]
        print(f"\nPersona a Actualizar: \n\n"+ f"-id: {persona_update['node']['id']} \n" +
                f"-Nombre:  {persona_update['node']['name']} \n")
        #Validating status code
        self.assertResponseNoErrors(response)
        self.assertEqual(87, cantidad)

    def test_update_people(self):

        response = self.query(
         '''
           mutation{
                addPeople(input:{
                id: "UGVvcGxlTm9kZTox"
                name:"David Gates"
                homeWorldId:"1"
                height : "172"
                mass: "77", 
                hairColor: "blond"
                skinColor: "fair" 
                eyeColor: "blue" 
                birthYear: "19BBY",
                gender: "male" 
                }) {
                people{
                    name
                    id
                }
                }

}
        '''
        )

        persona = json.loads(response.content)["data"]["addPeople"]["people"]
        print("Persona Actualizada: \n\n" + f"-id: {persona['id']}\n" + f"-Nombre: {persona['name']}\n")
        self.assertResponseNoErrors(response)
        self.assertEqual("David Gates", persona["name"])






        