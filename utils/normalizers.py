import pandas as pd

def normalize_sex(value):
    if pd.isnull(value):
        return "Unknown"
    val = str(value).strip().lower()
    if val in ["m", "male", "man", "masculino", "hombre"]:
        return "Male"
    elif val in ["f", "female", "woman", "femenino", "mujer"]:
        return "Female"
    else:
        return "Other"
