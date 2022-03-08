import os
import urllib.request


def handler(event, context):
    target_url = os.getenv('API_GW_URL')
    idempotency_token = os.getenv('PROBED_IDEMPOTENCY_TOKEN')
    lock_hold_seconds = 600
    urllib.request.urlopen(target_url + "?idempotency_token=" + idempotency_token + "&lock_hold_seconds=" + str(lock_hold_seconds)).read()
