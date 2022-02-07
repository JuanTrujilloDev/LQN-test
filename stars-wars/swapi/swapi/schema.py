import graphene

from app.schema import Query as sw_query, Mutation as sw_mutation


class Query(sw_query):
    pass


class Mutation(sw_mutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

#query = '''
#            query{
#                allPeople(id:""){
#                    edges{
#                        node{
#                            id
#                        }
#               }
#            }
#
#        '''

#Revisando query
#def test_query():
#    result = schema.execute(query)
#    print(len(result.data['allPeople']['edges']))

#test_query()
