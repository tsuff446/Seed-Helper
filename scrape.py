import json
import urllib.request as urllib2
from graphqlclient import GraphQLClient


def get_entrant_data(slug):
    authToken = "325a2c28e4e510e9135f2616fab83ca6"
    apiVersion = "alpha"

    client = GraphQLClient('https://api.smash.gg/gql/' + apiVersion)
    client.inject_token('Bearer ' + authToken)

    result = client.execute("""
    query GetEntrantsFromTournamentSlug($slug: String) {
    tournament(slug: $slug){
        events(limit: 1){
        entrants(query: { page: 1, perPage: 10000 }){
        pageInfo{
            total
            perPage
            page
        }
        nodes{
            name
            participants{
            user{
                id
            }
            }
        }
        }

        }
    }
    },
    """,
    {
        "slug": slug,
    })
    resData = json.loads(result)
    if 'errors' in resData:
        print('Error:')
        print(resData['errors'])
    else:
        print('Success!')

get_entrant_data("tournament/university-of-kentucky-x-gen-g-present-cats-smash-clash")  
    