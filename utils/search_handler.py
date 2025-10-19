import pandas as pd


def searchMultipleColumns(df, columns, searchValue, operator):
    if not columns or not searchValue:
        return df
    
    if operator == "AND":
        result = df.copy()
        for col in columns:
            result = result[result[col].astype(str).str.contains(searchValue, case=False, na=False)]
        return result
    else:
        masks = []
        for col in columns:
            masks.append(df[col].astype(str).str.contains(searchValue, case=False, na=False))
        return df[pd.concat(masks, axis=1).any(axis=1)]
