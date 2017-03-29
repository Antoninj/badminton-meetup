
# coding: utf-8

# Author : Antonin Jousson
# This script takes care of making a rsvp in the badminton meetup group for the weekly events I'm intersted in.

import argparse
import requests
import datetime

def get_event_ids(api_key,day_number):
    badminton_events_query_url = "https://api.meetup.com/2/events?key=%s&group_urlname=Brussels-Badminton-Meetup&sign=true"%(api_key)
    response = requests.get(badminton_events_query_url)
    data = response.json()
    events = data['results']
    
    event_ids = []
    for event in events:
        time = event['time']
        time = list(str(time))
        time = time[:10]
        time = int("".join(time))
        date = datetime.datetime.fromtimestamp(time)
        if date.weekday() == day_number:
            event_id = event['id']
            event_ids.append(event_id)
        
    return event_ids

# This is not needed, it was for testing purposes
def get_event_info(event_id):
    badminton_meetup_event_url = "https://api.meetup.com/2/events?key=%s&event_id=%s&sign=true"%(api_key,event_id)
    response = requests.get(badminton_meetup_event_url)
    data = response.json()
    
    return data['results']

def make_rsvp(event_id,api_key):       
    badminton_rsvp_query_url = "https://api.meetup.com/2/rsvp/"
    payload = {"event_id":event_id,"key":api_key,"guests":"0","rsvp":"yes","sign":"true"}
    rsvp_response= requests.post(badminton_rsvp_query_url,data = payload)
                
    return rsvp_response.json()

if __name__=="__main__":
    
    # Retrieve API key from text file
    file= open("meetup_api_key.txt","r")
    api_key = file.read()

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("day", help="Select the day of the week", type = int, choices=(4,6))
    
    args = parser.parse_args()
    day_number = args.day

    # Get the event ids 
    event_ids = get_event_ids(api_key,day_number)
    
    rsvp_responses = []
    for event_id in event_ids: 
        
        #event_info = get_event_info(event_id)
        
        # Book the event
        rsvp_response = make_rsvp(event_id,api_key)
        rsvp_responses.append(rsvp_response)
    
    # See the result of the rsvp
    for response in rsvp_responses:
        print(response,"\n")

