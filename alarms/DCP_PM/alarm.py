from bronze.libs.google.docs import spreadsheet as ss
from bronze.libs import alarm as bronze_alarm
import pendulum


# Create and initialize the alarm from the YAML file
pm_alarm = bronze_alarm.Alarm(alarm='alarm.yml')

# Load the spreadsheet
spreadsheet_url = pm_alarm.sheet_target
spreadsheet = ss.SpreadSheetReader(pm_alarm.creds_target, spreadsheet_url)

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
    sheet_name='#dcp-project-mgmt', sheet_range='A1:C1000', has_header=True
)
target = target_dates_df.loc[target_dates_df['Date'] == invocation_date_str]

# Extract and validate the date and coordinator for composing the messages
date = bronze_alarm.load_cell_from_row(column_name='Date', row=target)
coordinator = bronze_alarm.load_cell_from_row(column_name='Coordinator', row=target)
notetaker = bronze_alarm.load_cell_from_row(column_name='Notetaker', row=target)

# Make sure issues with the Name -> SlackID mapping won't mess up the whole alarm
try:
    coordinator_slack_id = slack_user_mapping[coordinator].tag
except KeyError:
    coordinator_slack_id = (
        f"{coordinator} - please register on the rotation spreadsheet!"
        if (not coordinator) or (coordinator.lower() != 'skip')
        else "skip"
    )

try:
    notetaker_slack_id = slack_user_mapping[notetaker].tag
except KeyError:
    notetaker_slack_id = (
        f"{notetaker} - please register on the rotation spreadsheet!"
        if (not notetaker) or (notetaker.lower() != 'skip')
        else "skip"
    )

# Compose the message while respecting the "skip" flags
if coordinator_slack_id == "skip" or notetaker_slack_id == "skip":
    msg = "There's no PM meeting tomorrow :pokemon-snorlax:"
else:
    msg = pm_alarm.message
    msg = msg.format(
        **{
            "date": date,
            "coordinator": coordinator_slack_id,
            "notetaker": notetaker_slack_id,
        }
    )

# Send out the message
pm_alarm.send_msg(msg=msg)
