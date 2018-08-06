# bronze

[![in-ancient-china-1926827_1280.jpg](https://s22.postimg.cc/8a3cf8vn5/in-ancient-china-1926827_1280.jpg)](https://postimg.cc/image/fq2m11jcd/)

Bronze is a minimal alarm that reads schedule and contacts data from Google Sheets and alerts the people on Slack.

## To create a new default alarm

A default alarm gets the current date, scans through the first column of the sheet, which are the scheduled dates, 
decides which interval the current date(today) falls in and sends alerts to the people(tags them) in that row via Slack.

To create a new default alarm, you can just copy an existing alarm as a template, modify it. Most importantly, if you 
want to follow default rules, you have to inherit from the `libs.DefaultAlarm` class and implement the `prepare_message()` 
static method. There are some external requirements to create a new alarm:
1. You have to have a Google Sheet that has two sheets within it:
    - 'Rotation' sheet should have a header of the format: `"[Dates, Person1, Person2, ...]"`, no need to follow the 
        exact words, but the first column should be dates for the alarm to parse from.
    - 'Rotation' sheet's "Dates" need to follow the format `'MMM D, YYYY'`
    - 'User IDs' sheet should have the header follows the format: `[User, slackID]`, again, follow the style of the
        content, not the literals.

2. You have to have either a OAuth2 client ID or a service account key that is created and downloaded through Google 
Cloud, enabling the G-Suite scopes, so that the alarm can talk to Google with the credentials.

3. You have to register a web app on slack and obtain the webhook urls which are corresponding to the channels you want
the alarm to send messages/alerts to.

4. Provide the above information(Slack webhook urls, Google service account keys, etc.) as environment variables to
the alarm, for details, check the existing alarms.

## To implement a brand new alarm

Since bronze provides a lot of low-level classes that help you interact with Google Sheet and Slack API 
(currently it only supports the incoming webhook feature). You can also follow the design of `libs.DefaultAlarm` class 
and create your new alarm from scratch!

## List of existing alarms

- [x] DCP OPS ALARM
- [x] DCP DEMO ALARM
