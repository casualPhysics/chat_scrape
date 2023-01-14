from gmail_api.credentials.ninja_token import ACCESS_TOKEN
import json
import requests


def get_historical_events_by_date(month, year):
    """
    Given a month and year, return some historical events
    :return: A list of dictionaries with the events
    """

    api_url = f'https://api.api-ninjas.com/v1/historicalevents?year={year}&month={month}'
    response = requests.get(api_url, headers={'X-Api-Key': ACCESS_TOKEN})
    if response.status_code == requests.codes.ok:
        text = response.text
        return json.loads(text)
    else:
        print("Error:", response.status_code, response.text)
        return None
