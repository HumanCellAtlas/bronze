from bronze.libs import alarm as bronze_alarm


# Create and initialize the alarm from the YAML file
demo_alarm = bronze_alarm.Alarm(alarm='alarm.yml')

# Load the spreadsheet
# No need for this alarm

# Construct the name -> SlackID mapping
# No need for this alarm

# Get the date of "today", which is the date of the script invocation time
# No need for this alarm

# Figure out which target date in the rotation the invocation day matches
# No need for this alarm

# Extract and validate the date and coordinator for composing the messages
# No need for this alarm

# Make sure issues with the Name -> SlackID mapping won't mess up the whole alarm
# No need for this alarm

# Compose the message while respecting the "skip" flags
msg = demo_alarm.message

# Send out the message
demo_alarm.send_msg(msg=msg)
