# import re
# import pandas as pd

# def preprocess(data):
#     pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
#     messages = re.split(pattern, data)[1:]
#     dates = re.findall(pattern, data)

#     df = pd.DataFrame({'user_message': messages, 'message_date': dates})

#     # Correct format string
#     format_str = "%m/%d/%y, %H:%M - "
    
#     # Parsing the date string
#     # df['message_date'] = pd.to_datetime(df['message_date'], format=format_str, dayfirst=False)
    
#     # Try to parse with multiple formats
#     try:
#         df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%Y, %H:%M -", errors="raise")
#     except:
#         try:
#             df['message_date'] = pd.to_datetime(df['message_date'], format="%m/%d/%y, %H:%M -", errors="raise")
#         except:
#             # fallback to automatic inference
#             df['message_date'] = pd.to_datetime(df['message_date'], dayfirst=True, errors="coerce")
#     df = df.dropna(subset=['message_date'])

#     # Rename column
#     df.rename(columns={'message_date': 'date'}, inplace=True)

#     # separate users and messages
#     users = []
#     messages = []
#     for message in df['user_message']:
#         entry = re.split(r'([\w\W]+?):\s', message)
#         if entry[1:]:     #user name
#             users.append(entry[1])
#             messages.append(entry[2])
#         else:
#             users.append('group_notification')
#             messages.append(entry[0])

#     df['user'] = users
#     df['message'] = messages
#     df.drop(columns = ['user_message'], inplace = True)

#     df['year'] = df['date'].dt.year
#     df['only_date'] = df['date'].dt.date
#     df['month_num'] = df['date'].dt.month
#     df['month'] = df['date'].dt.month_name()
#     df['day'] = df['date'].dt.day
#     df['day_name'] = df['date'].dt.day_name()
#     df['hour'] = df['date'].dt.hour
#     df['minute'] = df['date'].dt.minute 

#     period = []
#     for hour in df[['day_name', 'hour']]['hour']:
#         if hour == 23:
#             period.append(str(hour) + '-' + str('00'))
#         elif hour == 0:
#             period.append(str('00') + '+' + str(hour+1))
#         else:
#             period.append(str(hour) + '-' + str(hour+1))

#     df['period'] = period

#     # Ensure clean message column
#     df['message'] = df['message'].astype(str)
#     df = df[df['message'].str.strip() != '']  # remove empty messages


#     return df

















import re
import pandas as pd

def preprocess(data):
    # Regex pattern that handles:
    # - DD/MM/YY or DD/MM/YYYY
    # - 12hr (AM/PM) or 24hr
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}(?:\s?[APMapm]{2})?)\s-\s'

    # Split messages and capture dates
    messages = re.split(pattern, data)[1:]   # [date, time, msg, date, time, msg, ...]
    if not messages:
        return pd.DataFrame(columns=['user', 'message', 'date'])

    # Reshape into chunks of 3 (date, time, message)
    dates = []
    times = []
    msgs = []
    for i in range(0, len(messages), 3):
        dates.append(messages[i])
        times.append(messages[i+1])
        msgs.append(messages[i+2])

    df = pd.DataFrame({'date': dates, 'time': times, 'user_message': msgs})

    # Combine date + time
    df['message_date'] = pd.to_datetime(df['date'] + " " + df['time'], errors="coerce", dayfirst=True)
    df = df.dropna(subset=['message_date'])

    # Separate user and message
    users, messages_clean = [], []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
        if len(entry) > 2:
            users.append(entry[1])
            messages_clean.append(entry[2])
        else:
            users.append("group_notification")
            messages_clean.append(entry[0])

    df['user'] = users
    df['message'] = messages_clean

    # Drop helper cols
    df = df.drop(columns=['date', 'time', 'user_message'])

    # Extract datetime parts
    df['year'] = df['message_date'].dt.year
    df['only_date'] = df['message_date'].dt.date
    df['month_num'] = df['message_date'].dt.month
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['day_name'] = df['message_date'].dt.day_name()
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute

    # Create period ranges
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append(f"00-1")
        else:
            period.append(f"{hour}-{hour+1}")
    df['period'] = period

    # Clean message column
    df['message'] = df['message'].astype(str)
    df = df[df['message'].str.strip() != ""]

    return df
