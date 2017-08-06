
# coding: utf-8

# @Author : Antonin Jousson
# This script takes care of making a rsvp in the badminton meetup group for the weekly events I'm interested in.

# Link to get your meetup API key: https://secure.meetup.com/meetup_api/key/
# Link to get your twilio Account SID and Auth Token from twilio.com/console

import argparse
import requests
import datetime
from twilio.rest import Client

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

# This function is not needed, it was for testing purposes
def get_event_info(event_id):
    badminton_meetup_event_url = "https://api.meetup.com/2/events?key=%s&event_id=%s&sign=true"%(api_key,event_id)
    response = requests.get(badminton_meetup_event_url)
    data = response.json()
    
    return data['results']

def make_rsvp(event_id,api_key,rsvp_response,guest_nbr):       
    badminton_rsvp_query_url = "https://api.meetup.com/2/rsvp/"
    payload = {"event_id":event_id,"key":api_key,"guests":guest_nbr,"rsvp":rsvp_response,"sign":"true"}
    rsvp_response= requests.post(badminton_rsvp_query_url,data = payload)
                
    return rsvp_response.json()

if __name__=="__main__":
    
    # Retrieve API key from text file
    with open("meetup_api_key.txt","r") as file_1:
        api_key = file_1.read()

    # Your Account SID from twilio.com/console
    with open("account_sid.txt","r") as file_2:
        account_sid = file_2.read()

    # Your Auth Token from twilio.com/console
    with open("twilio_token_key.txt","r") as file_3:
        auth_token  = file_3.read()
        
    # Create twilio client to send confirmation sms
    client = Client(account_sid, auth_token)

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--day", help="Day of the week you want to register for the event(s) (sunday by default)", type = int, choices=(0,1,2,3,4,5,6) , default = 6)
    parser.add_argument("-r","--rsvp", help = "RSVP status (yes by default) " , type = str, choices = ("yes" , "no") , default  = "yes")
    parser.add_argument("-g","--guest", help = "Add a plus one (0 by default) " , type = str, choices = ("0","1") , default  = 0)

    parser.add_argument("-m","--mode",nargs='?', help="Run mode of script : choose 0 to enable sms confirmation (1 by default)", type = int, choices=(0,1) , default = 1)

    # Parse command line arguments
    args = parser.parse_args()
    day_number = args.day
    rsvp_response = args.rsvp
    guest_nbr = args.guest
    run_mode = args.mode

    # Get the event ids 
    event_ids = get_event_ids(api_key,day_number)
    
    # Get today's date
    today = datetime.datetime.today()

    # Book all events and store the results of the rvsp
    rsvp_responses = [make_rsvp(event_id,api_key,rsvp_response,guest_nbr) for event_id in event_ids]

    first_response = rsvp_responses[0]
    event_name = first_response["event"]["name"] 
    event_tallies = first_response["tallies"]
    event_rsvp_response = first_response["response"]
    message_body = "Badminton meetup name  : %s \nCurrent event status : %s \nMy rsvp response : %s " \
    %(event_name,event_tallies,event_rsvp_response)

    # See the result of the rsvp
    print(message_body)

    if run_mode == 0:
        # Send sms confirmation to my phone number
        message = client.messages.create(to="+32494886420", from_="+32460209835", body=message_body)

        
