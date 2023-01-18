from dotenv import load_dotenv
from os import environ
from typing import Dict, Tuple, Type,List
import requests

load_dotenv()

CLIENT_ID = environ.get("CLIENT_ID")
CLIENT_SECRET = environ.get("CLIENT_SECRET")
TOKEN = environ.get("TOKEN")

class StravaClient():
    ''' StravaListCollector usecase '''

    def get_activities(self, page: int) -> List:
        '''
        Request activities by page    
        Args:
            None
        Returns
            Tuple with status_code, request, response attributes
        ''' 
        req = requests.Request(
            method='GET',
            url="https://www.strava.com/api/v3/athlete/activities",
            headers={
            "Authorization": f"Bearer {TOKEN}",
            },
            params={"page":page}

        )
        req_prepared = req.prepare()

        http_session = requests.Session()
        response = http_session.send(req_prepared)

        return response

