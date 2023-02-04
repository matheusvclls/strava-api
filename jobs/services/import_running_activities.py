import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'client_strava'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared/', 'models'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared/', 'schemas'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared/', 'db'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'crud'))

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import client_strava_file
from db_setup import engine, get_db
import activity_models
from activity_crud import get_strava_activity, create_activity

activity_models.Base.metadata.create_all(bind=engine)

for page in range(1,100):

    strava_requests = client_strava_file.StravaClient()
    get_strava_activities = strava_requests.get_activities(page=page).json()
    
    # Check if the request has records
    if get_strava_activities == []:
        break

    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Iterate in the list of records
    for record in get_strava_activities:

        # Check if the record is run
        if record['type'] in ['Run','VirtualRun']:
            dict_record = {}
            print(record)
            print('\n')
            # Get the attributes
            dict_record['id']=record['id']
            dict_record['name']=record['name']
            dict_record['distance']=record['distance']
            dict_record['average_speed']=record['average_speed']
            if record['has_heartrate'] == True:
                dict_record['average_heartrate']=record['average_heartrate']
            else:
                dict_record['average_heartrate']=None
            dict_record['start_date']=record['start_date']

            db_user = get_strava_activity(db=session, activity_id=dict_record['id'])

            # Check if we have already had a record with this ID
            if db_user is None:
                # Create this record using this ID
                create_activity(db=session, activity=dict_record)
            else:
                pass
