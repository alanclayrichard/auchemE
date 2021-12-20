from __future__ import print_function
import time
import cfbd
from cfbd.rest import ApiException
from pprint import pprint
from matplotlib import pyplot as plt
import numpy as np
from numpy.core.fromnumeric import size
from numpy.lib.function_base import rot90

# Configure API key authorization: ApiKeyAuth
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = 'BzwWdA0tWAsTFPhGA3WPQlWJ+zg7th9VfotBqe9FrVUXAgfbRFkcNyXtauMcueiq'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = cfbd.PlayersApi(cfbd.ApiClient(configuration))
team = 'Tennessee'
year = 2021  # int | Year filter

# Player stats by season
api_response = api_instance.get_transfer_portal(year=year)
n=0
player = []
date = []
for i in range(len(api_response)):
    if api_response[i].destination == team:
        player = np.append(player,api_response[i].first_name+" "+api_response[i].last_name+" "+api_response[i].position)
        date = np.append(date,api_response[i].transfer_date[0:10])
        print(player,date)
        plt.plot(date[n], n)
        plt.text(date[n], n+1 , player[n])
        n = n + 1

plt.title('Transfer Players vs date for: ' + team + ' ' + str(year))
plt.ylim((0, n+2))
plt.xticks(rotation=90, size='8')
plt.show()
