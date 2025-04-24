# utils/duration.py

import pandas as pd

def categorize_duration(start, end):
    if pd.isnull(start) or pd.isnull(end):
        return "Do not Know"

    duration = (end - start).days

    if start.month in [6, 7, 8]:
        if duration < 14:
            return "Summer: Less than Two Weeks"
        elif duration <= 56:
            return "Summer: Two Weeks to Eight Weeks"
        else:
            return "Summer: More than Eight Weeks"

    if start.month == 1:
        return "Short-term: January term"

    if (start.month in [8, 9, 10]) and (end.month in [5, 6, 7]) and duration > 240:
        return "Long-Term: Academic Year"

    if start.month == 1 and end.month == 12 and duration >= 330:
        return "Long-Term: Calendar Year"

    if 80 <= duration <= 110:
        return "Mid-length: One Semester"
    elif 120 <= duration <= 160:
        return "Mid-length: Two Quarters"
    elif 50 <= duration < 80:
        return "Mid-length: One Quarter"

    if duration < 14:
        return "Short-term: Less than Two Weeks during the Academic Year"
    elif duration <= 56:
        return "Short-term: Two to Eight Weeks during the Academic Year"

    return "Other (please specify duration)"
