import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'client_strava'))

import client_strava_file

x= client_strava_file.StravaClient()
print(x.get_activities(page=1).json())