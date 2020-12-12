from base.models import Event
import requests
import hashlib
import json


def webhook(sender, instance, created, **kwargs):
    if created:
        e_type = "add"
    else:
        e_type = "update"
    u = instance.owner
    for w in u.webhooks.all():
        data = {
            'owner': instance.owner.pk,
            'title': instance.title,
            'description': instance.description,
            'start': instance.start,
            'end': instance.end
        }
        s_data = json.dumps(data, default=str)
        s_sig = s_data + ":" + str(w.secret)
        s = bytes(s_sig, encoding='utf-8')
        sig = hashlib.sha256(s).hexdigest()
        try:
            requests.post(w.url, data=s_data, headers={
                'x-event': 'event.' + e_type,
                'x-signature': sig,
                'content-type': 'application/json'
            })
        except requests.exceptions.RequestException:
            pass
