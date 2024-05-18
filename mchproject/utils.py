from datetime import datetime, timedelta


def convert_to_string(time_obj):
    if not time_obj:
        return None
    return time_obj.strftime('%I:%M %p')
    
def convert_to_time(time_str):
    if not time_str:
        return None
    try:
        # Parse the time string and return a datetime.time object
        return datetime.strptime(time_str, '%I:%M %p').time()
    except ValueError:
        return None
    
def generate_time_choices(start_hour, end_hour):
    choices = []
    for hour in range(start_hour, end_hour + 1):
        for minute in range(0, 60, 30):
            time = f"{hour % 12 if hour % 12 != 0 else 12}:{minute:02d} {'pm' if hour >= 12 else 'am'}"
            choices.append((time, time))
    return choices

# def get_available_dates(start_date, end_date):
#     """
#     Generate a list of available dates between start_date and end_date, excluding Sundays.
#     """
#     available_dates = []
#     current_date = start_date
#     while current_date <= end_date:
#         if current_date.weekday() != 6:  # 6 corresponds to Sunday
#             available_dates.append(current_date)
#         current_date += timedelta(days=1)
#     return available_dates