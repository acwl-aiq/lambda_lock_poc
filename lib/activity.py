import time
import os
import ddb_dao
import logging


def handler(event, context):
    lock_table_name = os.getenv('LOCK_TABLE_NAME')
    sleep_seconds = os.getenv('SLEEP_SECONDS')
    idempotency_token = str(event.get("idempotency_token", "")) or "default"
    lock_hold_seconds = int(event.get("idempotency_token", sleep_seconds))

    # Hack: Workaround for missing piece to funnel GET param from API GW to lambda
    if idempotency_token == "default":
        lock_hold_seconds = 600

    status_code = 401
    if idempotency_token:
        if ddb_dao.acquire_lock(lock_table_name, idempotency_token):
            print("Acquired Lock [%s]. Sleeping for %s seconds" % (idempotency_token, lock_hold_seconds))
            status_code = 200
            time.sleep(lock_hold_seconds)
            print("Finished sleeping. Releasing lock [%s]" % idempotency_token)
            if ddb_dao.release_lock(lock_table_name, idempotency_token): # If this fails, we can have a problem with a permanent lock
                print("Releasedlock [%s]" % idempotency_token)
            else:
                status_code = 500
                print("Failed to release lock [%s]" % idempotency_token)
        else:
            status_code = 400
            print("Cannot acquire lock [%s]" % idempotency_token)
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': ''
    }