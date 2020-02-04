from bronze.libs.google.docs import spreadsheet as ss
from bronze.libs import alarm as bronze_alarm
import pendulum
import sys
import os
from bronze.utils import create_doc_from_template


# Create and initialize the alarm from the YAML file
ops_alarm = bronze_alarm.Alarm(alarm='alarm.yml')

# Get the date of "today", which is the date of the script invocation time
invocation_date = pendulum.today(tz="UTC")
print(f"The current invocation date is {invocation_date}")

# If the alarm is called on Fridays, look for day shift + 3 (Monday)
# If the alarm is called on Mondays, look for today
if invocation_date.day_of_week == 5:
    invocation_date = invocation_date.add(days=3)
invocation_date_str = invocation_date.format("MMM D, YYYY")

# Compose the message while respecting the "skip" flags
#if len(set(list(rotation.values()))) == 1 and list(rotation.values())[0] == "skip":
#    msg = "There's no DCP demo for the week :pokemon-snorlax:"
#else:
#    msg = ops_alarm.message
#    msg = msg.format(**rotation)
#
# Send out the message
#ops_alarm.send_msg(msg=msg)

######################################################################################
# === Additionally, if and only if today is Monday(s), create the release notes from templates ===
#if not pendulum.today(tz="UTC").day_of_week == 1:
#    print(
#        f"Invocation day {pendulum.today(tz='UTC')} is not Monday, skip creating release notes..."
#    )
#    sys.exit(0)
# ======

GOOGLE_DOC_URL = "https://docs.google.com/document/d/{document_id}"
RELEASE_NOTES_TEMPLATE_ID = os.environ.get(
    ops_alarm.core.get('document_template_target_var')
)
RELEASE_NOTES_TEMPLATE_URL = GOOGLE_DOC_URL.format(
    document_id=RELEASE_NOTES_TEMPLATE_ID
)

# Production release notes:
prod_date = pendulum.today().add(days=1).strftime("%Y/%m/%d")
release_destination = 'Production'
print(f'Will create release notes for {prod_date} for {release_destination} promotion.')

prod_release_note_id = create_doc_from_template(
    template_url=RELEASE_NOTES_TEMPLATE_URL,
    service_account_key=ops_alarm.creds_target,
    copy_title=f"{prod_date} {release_destination} Release Notes",
    date=prod_date,
    release_destination=release_destination,
)

# Staging release notes:
staging_date = pendulum.today().add(days=2).strftime("%Y/%m/%d")
release_destination = 'Staging'
print(
    f'Will create release notes for {staging_date} for {release_destination} promotion.'
)

staging_release_note_id = create_doc_from_template(
    template_url=RELEASE_NOTES_TEMPLATE_URL,
    service_account_key=ops_alarm.creds_target,
    copy_title=f"{staging_date} {release_destination} Release Notes",
    date=staging_date,
    release_destination=release_destination,
)
