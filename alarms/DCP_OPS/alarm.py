from bronze.libs.google.docs import spreadsheet as ss
from bronze.libs import alarm as bronze_alarm
import pendulum


# Create and initialize the alarm from the YAML file
ops_alarm = bronze_alarm.Alarm(alarm='alarm.yml')

# Load the spreadsheet
spreadsheet_url = ops_alarm.sheet_target
spreadsheet = ss.SpreadSheetReader(ops_alarm.creds_target, spreadsheet_url)

# Construct the name -> SlackID mapping
slack_user_mapping = bronze_alarm.get_slack_mapping(
    spreadsheet=spreadsheet, remove_header=True
)

# Get the date of "today", which is the date of the script invocation time
invocation_date = pendulum.today(tz="UTC")

# If the alarm is called on Fridays, look for day shift + 3 (Monday)
# If the alarm is called on Mondays, look for today
if invocation_date.day_of_week == 5:
    invocation_date = invocation_date.add(days=3)
invocation_date_str = invocation_date.format("MMM DD, YYYY")

# Figure out which target date in the rotation the invocation day matches
target_dates_df = spreadsheet.sheetToDataFrame(
    sheet_name='#dcp-ops', sheet_range='A1:L1000', has_header=True
)
target = target_dates_df.loc[target_dates_df['Date'] == invocation_date_str]

# Extract and validate the date and coordinator for composing the messages
date = bronze_alarm.load_cell_from_row(column_name='Date', row=target)
SERVICES = [
    "Coordinator",
    "Metadata",
    "Ingest",
    "Upload",
    "DataStore",
    "Analysis",
    "Azul",
    "DataBrowser",
    "Matrix",
    "Query",
    "Auth",
]
rotation = {"date": date}

for service in SERVICES:
    # Make sure issues with the Name -> SlackID mapping won't mess up the whole alarm
    try:
        person = bronze_alarm.load_cell_from_row(column_name=service, row=target)
        person_slack_id = slack_user_mapping[person].tag
    except KeyError:
        person_slack_id = (
            f"{person} - please register on the rotation spreadsheet!"
            if (not person) or (person.lower() != 'skip')
            else "skip"
        )
    rotation[service] = person_slack_id

# Compose the message while respecting the "skip" flags
if len(set(list(rotation.values()))) == 1 and list(rotation.values())[0] == "skip":
    msg = "There's no DCP demo for the week :pokemon-snorlax:"
else:
    msg = ops_alarm.message
    msg = msg.format(**rotation)

# Send out the message
ops_alarm.send_msg(msg=msg)
