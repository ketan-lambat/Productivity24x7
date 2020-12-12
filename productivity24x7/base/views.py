from django.shortcuts import render, redirect
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.conf import settings
from .models import Event
from django.contrib.auth.decorators import login_required


def homepage_view(request):
    return render(request, "base/homepage.html")


@login_required()
def get_calender_events_view(request):
    scopes = ['https://www.googleapis.com/auth/calendar']
    credentials_file = settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON
    cred = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            cred = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, scopes)
            cred = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(cred, token)

    service = build('calendar', 'v3', credentials=cred)

    now = datetime.datetime.utcnow().isoformat() + 'Z'

    calendar_list = service.calendarList().list().execute()
    calendar_ids = calendar_list['items']
    req_calendar = 'Prod_events'

    calendar_id = None
    for i in range(len(calendar_ids)):
        if calendar_ids[i]['summary'] == req_calendar:
            calendar_id = calendar_ids[i]['id']

    events_result = service.events().list(calendarId=calendar_id, timeMin=now).execute()
    events = events_result.get('items', [])

    if not events:
        pass
    for event in events:
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        end_time = event['end'].get('dateTime', event['end'].get('date'))
        title = event['summary']
        if event['description'] is not None:
            description = event['description']
        else:
            description = ""
        g_event_id = event['id']

        event, event_created = Event.objects.get_or_create(title=title,
                                                           description=description,
                                                           start=start_time,
                                                           end=end_time,
                                                           g_event_id=g_event_id,
                                                           owner=request.user)
        if event_created:
            event.save()

    return redirect('events')


@login_required()
def disply_calendar_events(request):
    events = Event.objects.all().order_by('start')
    context = {
        'events_arr': events,
    }
    return render(request, 'base/events.html', context=context)
