import pandas as pd
from FiveETools.modern.sources import source, json_source
from FiveETools.gsheets_client import modern_sheets
import inflection
from collections import defaultdict
from itertools import count
import string

df_subclasses = modern_sheets.get_sheet("338247460")
df_subclasses.head()

# Load class features with header row offset
df_class_features = modern_sheets.get_sheet("545140625", header=1)
df_class_features.head()


def get_features_for_subclass(class_name, subclass_name):
    def get_feature_label(row):
        name = row.get("Name")
        level = int(row.get("Level"))

        return f"{name}|{class_name}|{json_source}|{subclass_name}|{json_source}|{level}|{json_source}"

    return [
        *[
            get_feature_label(entry_row)
            for index, entry_row in df_class_features.iterrows()
            if pd.notnull(entry_row.get("Class"))
            and pd.notnull(entry_row.get("Name"))
            and str(entry_row.get("Subclass")) == subclass_name
        ]
    ]


def row_to_subclass(row):
    subclass_name = row.get("Name")
    class_name = row.get("Class")
    features = get_features_for_subclass(class_name, subclass_name)
    subclass = {
        "name": subclass_name,
        "source": json_source,
        "className": class_name,
        "classSource": json_source,
        "shortName": subclass_name,
        "subclassFeatures": features,
    }
    return subclass


subclasses_list = [
    row_to_subclass(row)
    for index, row in df_subclasses.iterrows()
    if pd.notnull(row.get("Name"))
    and str(row.get("Name")).strip() != ""
    and row.get("Source") == source
]
