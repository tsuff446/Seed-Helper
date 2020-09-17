from scrape import get_entrant_data
from scrape import get_user_winrate
import json

top_n = 30
raw_data = get_entrant_data("tournament/10-the-smash-plaza-tournament-arc-s6")  
event_data = raw_data['data']['tournament']['events'][0]
entrant_data = event_data['entrants']['nodes']

for curr_user in entrant_data:
    try:
        user_id = curr_user['participants'][0]['user']['id']
        curr_user['winrate'] = get_user_winrate(user_id)
    except:
        curr_user['winrate'] = -1

entrant_data.sort(key=lambda x: x['winrate'], reverse=True)

for x in range(top_n):
    print("#" + str(x + 1))
    print(entrant_data[x]['name'])
    print(entrant_data[x]['winrate'])