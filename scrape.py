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
        print('Successfully got user ids')
    return resData
    
def get_user_winrate(user_id):
    authToken = "325a2c28e4e510e9135f2616fab83ca6"
    apiVersion = "alpha"

    client = GraphQLClient('https://api.smash.gg/gql/' + apiVersion)
    client.inject_token('Bearer ' + authToken)

    result = client.execute("""query MatchQuery ($user_id: ID){
    user(id: $user_id){
        player{
            gamerTag
            sets(page: 1, perPage: 100){
            nodes{
                displayScore
            }
            }
        }
    }
    },
    """,
    {
    "user_id": user_id
    })

    resData = json.loads(result)
    if 'errors' in resData:
        print('Error:')
        print(resData['errors'])
    
    tag = resData['data']['user']['player']['gamerTag']
    last_tag_word = tag.split()[-1]
    matches = resData['data']['user']['player']['sets']['nodes']
    win = 0
    loss = 0
    if(not matches):
        return -1
    for curr_set in matches:
        curr_match = curr_set['displayScore']
        if curr_match != "DQ" and curr_match:
            data = curr_match.split()
            if check_valid_display_score(curr_match):
                your_score = -1
                opp_score = 0
                scores = []
                scores.append(int(curr_match[curr_match.index(' - ')-1]))
                scores.append(int(curr_match[-1]))
                if(data[-2] == last_tag_word):
                    your_score = scores[1]
                    opp_score = scores[0]
                else:
                    your_score = scores[0]
                    opp_score = scores[1]

                if(your_score > opp_score):
                    win += 1
                else:
                    loss += 1
    if win + loss == 0:
        winrate = -1
    else:
        winrate = win/(win + loss)
    print("Winrate of " + tag + ": " + str(winrate))
    print("(", win, "/", (win + loss), ")")
    return winrate

def check_valid_display_score(score):
    return str.isdigit(score[-1]) and score.count('/') != 2

