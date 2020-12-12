from __future__ import print_function
from django.shortcuts import render, redirect
from pprint import pprint
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.conf import settings
from .models import Event


def homepage_view(request):
    return render(request, "base/homepg1.html")


def get_calender_events_view(request):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    credentials_file = settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + 'Z'

    calendar_list = service.calendarList().list().execute()
    calendar_ids = calendar_list['items']
    req_calendar = 'Prod_events'

    # pprint(calendar_ids)
    # calendar_id = calendar_ids[i]['id']
    for i in range(len(calendar_ids)):
        if (calendar_ids[i]['summary'] == req_calendar):
            calendar_id = calendar_ids[i]['id']

    # print(calendar_id)

    events_result = service.events().list(calendarId=calendar_id, timeMin=now).execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        title = event['summary']
        if event['description'] is not None:
            description = event['description']
        else:
            description = ""
        g_event_id = event['id']

        event, event_created = Event.objects.get_or_create(title=title,
                                                           description=description,
                                                           start_time=start_time,
                                                           g_event_id=g_event_id)
        if event_created:
            event.save()

    return redirect('events')


def disply_calendar_events(request):
    events = Event.objects.all()
    context = {
        'events_arr': events,
    }
    return render(request, 'base/events.html', context=context)
