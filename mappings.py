from config import column_aliases

def auto_column_mapping(df):
    mapping = {}
    columns_lower = {col.lower(): col for col in df.columns}

    for field, aliases in column_aliases.items():
        found = None
        for alias in aliases:
            for col_lower, col_original in columns_lower.items():
                if alias in col_lower:
                    found = col_original
                    break
            if found:
                break
        mapping[field] = found

    print("\n🧠 Column mapping:")
    for k, v in mapping.items():
        print(f"- {k}: {v}")
    return mapping
