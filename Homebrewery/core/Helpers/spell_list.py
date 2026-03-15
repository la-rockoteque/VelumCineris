import pandas as pd
from Spreadsheet.sheets import modern_sheets

df_spells = modern_sheets.get_sheet_by_name("spells")
df_spells.head()

df_sorted = df_spells.sort_values(['Level', 'Spell Name'])
grouped = df_sorted.groupby('Level')

def row_to_markdown(level, group):
    list = "\n".join([f"- {row['Spell Name']}" for _, row in group.iterrows()])
    return f"##### {level}\n\n{list}"

markdown = [row_to_markdown(level, group) for level, group in grouped]

spell_list = "\n\n".join(markdown)
