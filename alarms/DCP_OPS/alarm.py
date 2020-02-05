from bronze.libs.google.docs import spreadsheet as ss
from bronze.libs import alarm as bronze_alarm
import pendulum
import sys
import os
from bronze.utils import create_doc_from_template


# Create and initialize the alarm from the YAML file
ops_alarm = bronze_alarm.Alarm(alarm='alarm.yml')

# # Load the spreadsheet
# spreadsheet_url = ops_alarm.sheet_target
# spreadsheet = ss.SpreadSheetReader(ops_alarm.creds_target, spreadsheet_url)
#
# # Construct the name -> SlackID mapping
# slack_user_mapping = bronze_alarm.get_slack_mapping(
#     spreadsheet=spreadsheet, remove_header=True
# )

# Get the date of "today", which is the date of the script invocation time
invocation_date = pendulum.today(tz="UTC")
print(f"The current invocation date is {invocation_date}")

# If the alarm is called on Fridays, look for day shift + 3 (Monday)
# If the alarm is called on Mondays, look for today
if invocation_date.day_of_week == 5:
    invocation_date = invocation_date.add(days=3)
invocation_date_str = invocation_date.format("MMM D, YYYY")

# # Figure out which target date in the rotation the invocation day matches
# print(f"Looking for exact matches of {invocation_date_str} in the rotation sheet...")
# target_dates_df = spreadsheet.sheetToDataFrame(
#     sheet_name='#dcp-ops', sheet_range='A1:L1000', has_header=True
# )
# target = target_dates_df.loc[target_dates_df['Date'] == invocation_date_str]
#
# # Extract and validate the date and coordinator for composing the messages
# date = bronze_alarm.load_cell_from_row(column_name='Date', row=target)
# SERVICES = [
#     "Coordinator",
#     "Metadata",
#     "Ingest",
#     "Upload",
#     "DataStore",
#     "Analysis",
#     "Azul",
#     "DataBrowser",
#     "Matrix",
#     "Query",
#     "Auth",
# ]
# rotation = {"date": date}
#
# for service in SERVICES:
#     # Make sure issues with the Name -> SlackID mapping won't mess up the whole alarm
#     try:
#         person = bronze_alarm.load_cell_from_row(column_name=service, row=target)
#         person_slack_id = slack_user_mapping[person].tag
#     except KeyError:
#         person_slack_id = (
#             f"{person} - please register on the rotation spreadsheet!"
#             if (not person) or (person.lower() != 'skip')
#             else "skip"
#         )
#     rotation[service] = person_slack_id

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

# follow_up_msg = f"""Also, please fill out the following release notes *before* the release:
#     - *Production* Notes: {GOOGLE_DOC_URL.format(document_id=prod_release_note_id)}
#     - *Staging* Notes: {GOOGLE_DOC_URL.format(document_id=staging_release_note_id)}"""
# ops_alarm.send_msg(msg=follow_up_msg)
