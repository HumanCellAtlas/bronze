from bronze.libs.google.docs import spreadsheet as ss
from bronze.libs import alarm as bronze_alarm
import pendulum
import sys


# Create and initialize the alarm from the YAML file
demo_alarm = bronze_alarm.Alarm(alarm='alarm.yml')

# Load the spreadsheet
spreadsheet_url = demo_alarm.sheet_target
spreadsheet = ss.SpreadSheetReader(demo_alarm.creds_target, spreadsheet_url)

# Construct the name -> SlackID mapping
slack_user_mapping = bronze_alarm.get_slack_mapping(
    spreadsheet=spreadsheet, remove_header=True
)

# Get the date of "today", which is the date of the script invocation time
invocation_date = pendulum.today(tz="UTC")

# Look for tomorrow
invocation_date = invocation_date.add(days=1)
invocation_date_str = invocation_date.format("MMM D, YYYY")

# Figure out which target date in the rotation the invocation day matches
target_dates_df = spreadsheet.sheetToDataFrame(
    sheet_name='dcp-demo', sheet_range='A1:B1000', has_header=True
)
target = target_dates_df.loc[target_dates_df['Date'] == invocation_date_str]

# Extract and validate the date and coordinator for composing the messages
try:
    date = bronze_alarm.load_cell_from_row(column_name='Date', row=target)
except ValueError:
    # No entry found, mostly means there's no demo, early termination!
    # TODO: make this logic less error-prone
    msg = "There's no demo tomorrow :pokemon-snorlax:"
    demo_alarm.send_msg(msg=msg)
    sys.exit(0)

coordinator = bronze_alarm.load_cell_from_row(column_name='Coordinator', row=target)

# Make sure issues with the Name -> SlackID mapping won't mess up the whole alarm
try:
    slack_id = slack_user_mapping[coordinator].tag
except KeyError:
    slack_id = (
        f"{coordinator} - please register on the rotation spreadsheet!"
        if (not coordinator) or (coordinator.lower() != 'skip')
        else "skip"
    )

# Compose the message while respecting the "skip" flags
if slack_id == "skip":
    msg = "There's no demo tomorrow :pokemon-snorlax:"
else:
    msg = demo_alarm.message
    msg = msg.format(**{"date": date, "coordinator": slack_id})

# Send out the message
demo_alarm.send_msg(msg=msg)
