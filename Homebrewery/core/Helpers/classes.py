import pandas as pd
from pandas.core.api import value_counts
from FiveETools.datasets.modern_assembly import to_table
from FiveETools.datasets.sources import get_default_source_context
from Spreadsheet.sheets import modern_sheets
import math

source, json_source = get_default_source_context("modern")


def build_class_table(class_name):
    table = {}
    for index, row in df_class_tables.iterrows():
        if row.get("Class") == class_name:
            table[row.get("Level")] = {
                **(
                    {"Level": math.trunc(row.get("Level"))}
                    if pd.notnull(row.get("Level"))
                    else {}
                ),
                **(
                    {"Proficiency Bonus": math.trunc(row.get("Proficiency Bonus"))}
                    if pd.notnull(row.get("Proficiency Bonus"))
                    else {}
                ),
                **(
                    {"Spells Known": math.trunc(row.get("Spells Known"))}
                    if pd.notnull(row.get("Spells Known"))
                    else {}
                ),
                **(
                    {"Max Spell Level": math.trunc(row.get("Max Spell Level"))}
                    if pd.notnull(row.get("Max Spell Level"))
                    else {}
                ),
                **(
                    {"Points": math.trunc(row.get("Points"))}
                    if pd.notnull(row.get("Points"))
                    else {}
                ),
                **(
                    {"Total spell slots": math.trunc(row.get("Total spell slots"))}
                    if pd.notnull(row.get("Total spell slots"))
                    else {}
                ),
                **(
                    {row.get("Feature 1 Name"): math.trunc(row.get("Feature 1"))}
                    if pd.notnull(row.get("Feature 1 Name"))
                    else {}
                ),
                **({"0": math.trunc(row.get("0"))} if pd.notnull(row.get("0")) else {}),
                **({"1": math.trunc(row.get("1"))} if pd.notnull(row.get("1")) else {}),
                **({"2": math.trunc(row.get("2"))} if pd.notnull(row.get("2")) else {}),
                **({"3": math.trunc(row.get("3"))} if pd.notnull(row.get("3")) else {}),
                **({"4": math.trunc(row.get("4"))} if pd.notnull(row.get("4")) else {}),
                **({"5": math.trunc(row.get("5"))} if pd.notnull(row.get("5")) else {}),
                **({"6": math.trunc(row.get("6"))} if pd.notnull(row.get("6")) else {}),
                **({"7": math.trunc(row.get("7"))} if pd.notnull(row.get("7")) else {}),
                **({"8": math.trunc(row.get("8"))} if pd.notnull(row.get("8")) else {}),
                **({"9": math.trunc(row.get("9"))} if pd.notnull(row.get("9")) else {}),
                "Features": ", ".join(
                    f"{feat_row.get('Name')}"
                    for _, feat_row in df_class_features.iterrows()
                    if pd.notnull(feat_row.get("Name"))
                    and feat_row.get("Class") == class_name
                    and feat_row.get("Level") == row.get("Level")
                    and pd.isnull(feat_row.get("Parent"))
                    and pd.isnull(feat_row.get("Subclass"))
                )
                or "-",
            }

            # Generate a Markdown table from the levels in `table`
            # Use the first entry’s keys as the headers
    headers = list(next(iter(table.values())).keys())
    # Header row
    header_row = "|" + "|".join(headers) + "|"
    # Alignment row
    align_row = "|" + "|".join([":-:" for _ in headers]) + "|"
    # Data rows for each level
    data_rows = [
        "|" + "|".join(str(level_dict.get(header, "")) for header in headers) + "|"
        for level_key, level_dict in table.items()
    ]

    return f"""{header_row}
{align_row}
{"\n".join(data_rows)}
"""


def row_to_subclass(row, class_name):
    table = [
        f"|{math.trunc(feature.get('Level'))}|{feature.get('Name')}|"
        for _, feature in df_class_features.iterrows()
        if pd.notnull(row.get("Name"))
        and row.get("Class") == class_name
        and pd.isnull(row.get("Parent"))
        and row.get("Name") == feature.get("Subclass")
    ]

    abilities = [
        f"""
### {feature.get("Name")}
{feature.get("Entry")}
"""
        for index, feature in df_class_features.iterrows()
        if pd.notnull(feature.get("Name"))
        and feature.get("Class") == class_name
        and pd.isnull(feature.get("Parent"))
        and row.get("Name") == feature.get("Subclass")
    ]

    return f"""
### {row.get("Name")}
> {row.get("Slug")}  

{row.get("Description")}

#### Roleplay & Playstyle
{row.get("Playstyle")}  

#### Subclass Abilities
|Level|Feature|
|:-:|:--:|
  {"\n".join(table)}
---

#### Features
{"\n\n".join(abilities)}
\page
"""


def row_to_markdown(row):
    class_name = row["Name"].strip()
    hit_dice = row["Hit Dice"].strip()
    tags = " | ".join(row["Role"].split(", "))
    hit_point_at_first = row["Hit Points at 1st Level"]

    abilities = [
        f"""
### {row.get("Name")}
{row.get("Entry")}
"""
        for index, row in df_class_features.iterrows()
        if pd.notnull(row.get("Name"))
        and row.get("Class") == class_name
        and pd.isnull(row.get("Parent"))
        and pd.isnull(row.get("Subclass"))
        and pd.notnull(row.get("Entry"))
    ]

    subclasses = [
        row_to_subclass(row, class_name)
        for index, row in df_subclasses.iterrows()
        if pd.notnull(row.get("Name")) and row.get("Class") == class_name
    ]

    return f"""
# **{class_name}**
*{tags}*  
> *{row["Quotes"].strip()}*  

### Thematic Overview
{row["Thematic Overview"].strip()}  

### Creating a {class_name}
{row["Creating"].strip()}  

### Multiclassing
{row.get("Multiclasing")}

\column

## Class Features
- **Hit Dice:** *{hit_dice} per {class_name} level*  
- **Hit Points at 1st Level:** *{hit_point_at_first} + Constitution modifier*  
- **Hit Points at Higher Levels:** *{hit_dice} + Constitution modifier per level after 1st*

### Proficiencies
- **Armor:** *{row.get("Armor")}*  
- **Weapons:** *{row.get("Weapons")}* 
- **Tools:** *{row.get("Tools")}*  
- **Saving Throws:** *{row.get("Saving Throws")}*  
- **Skills:** *Choose two from {row.get("Skills")}*

### Equipment 
You start with the following equipment:
{row.get("Common")}
Inaddition you choose from the following equipment:
A:
{row.get("A")}
B:
{row.get("B")}

---
{{{{wide
## Class Table
{build_class_table(class_name)}
}}}}
\page
## Class Abilities
 {"\n".join(abilities)}
\page
## Subclasses: {row.get("Subclass Title")} of the {class_name}
{row.get("Subclass Fluff")}

{"--- \n".join(subclasses)}
"""


df_spells = modern_sheets.get_sheet_by_name("spells")
df_spells.head()

df_subclasses = modern_sheets.get_sheet_by_name("subclasses")
df_subclasses.head()

df_classes = modern_sheets.get_sheet("1924660120", header=1)
df_classes.head()

df_class_tables = modern_sheets.get_sheet("193036738", header=1)
df_class_tables.head()

df_class_features = modern_sheets.get_sheet("545140625", header=1)
df_class_features.head()

classes = "\page".join(
    [
        row_to_markdown(row)
        for index, row in df_classes.iterrows()
        if pd.notnull(row.get("Name")) and row.get("Source") == source
    ]
)
