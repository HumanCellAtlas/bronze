from bronze.libs.google.docs import spreadsheet as ss
from bronze.libs import alarm as bronze_alarm
import pendulum

# Create and initialize the alarm from the YAML file
pl_alarm = bronze_alarm.Alarm(alarm='alarm.yml')

# Load the spreadsheet
spreadsheet_url = pl_alarm.sheet_target
spreadsheet = ss.SpreadSheetReader(pl_alarm.creds_target, spreadsheet_url)

# Construct the name -> SlackID mapping
slack_user_mapping = bronze_alarm.get_slack_mapping(
    spreadsheet=spreadsheet, remove_header=True
)

# Get the date of "today", which is the date of the script invocation time
invocation_date = pendulum.today(tz="UTC")

# Look for tomorrow
invocation_date = invocation_date.add(days=1)
invocation_date_str = invocation_date.format("MMM DD, YYYY")

# Figure out which target date in the rotation the invocation day matches
target_dates_df = spreadsheet.sheetToDataFrame(
    sheet_name='#dcp-pl', sheet_range='A1:C1000', has_header=True
)
target = target_dates_df.loc[target_dates_df['Date'] == invocation_date_str]

# Extract and validate the date and coordinator for composing the messages
date = bronze_alarm.load_cell_from_row(column_name='Date', row=target)
facilitator = bronze_alarm.load_cell_from_row(column_name='Facilitator', row=target)
scribe = bronze_alarm.load_cell_from_row(column_name='Scribe', row=target)

# Make sure issues with the Name -> SlackID mapping won't mess up the whole alarm
try:
    facilitator_slack_id = slack_user_mapping[facilitator].tag
except KeyError:
    facilitator_slack_id = (
        f"{facilitator} - please register on the rotation spreadsheet!"
        if (not facilitator) or (facilitator.lower() != 'skip')
        else "skip"
    )

try:
    scribe_slack_id = slack_user_mapping[scribe].tag
except KeyError:
    scribe_slack_id = (
        f"{scribe} - please register on the rotation spreadsheet!"
        if (not scribe) or (scribe.lower() != 'skip')
        else "skip"
    )

# Compose the message while respecting the "skip" flags
if facilitator_slack_id == "skip" or scribe_slack_id == "skip":
    msg = "There's no PL meeting tomorrow :pokemon-snorlax:"
else:
    msg = pl_alarm.message
    msg = msg.format(
        **{"date": date, "facilitator": facilitator_slack_id, "scribe": scribe_slack_id}
    )

# Send out the message
pl_alarm.send_msg(msg=msg)
