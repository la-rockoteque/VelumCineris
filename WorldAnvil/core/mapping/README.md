# World Anvil Mapping Files

This directory contains JSON mapping files that define how to convert data from various sources (Google Sheets, Obsidian Portal, etc.) to World Anvil format.

## Mapping File Format

Mapping files are JSON objects where:
- **Keys** = World Anvil field names
- **Values** = Source column/field names

```json
{
  "title": "Name",
  "content": "Description",
  "tags": "Tag"
}
```

## Supported Field Formats

### Simple Fields
Direct 1:1 mapping:
```json
{
  "title": "Spell Name",
  "level": "Level",
  "school": "School"
}
```

### Nested Objects
Use dot notation for nested fields:
```json
{
  "speed.walk": "Walk Speed",
  "speed.fly": "Fly Speed",
  "world.title": "Source"
}
```

### Arrays
Use bracket notation for array indices:
```json
{
  "traits[0].name": "Trait 1",
  "traits[0].ability": "Ability 1",
  "traits[1].name": "Trait 2",
  "traits[1].ability": "Ability 2"
}
```

### Content Sections
Use `content.SectionName` to create sections in the article content:
```json
{
  "content.Intro": "Intro",
  "content.Origin": "Origin",
  "content.Appearance": "Appearance"
}
```

This generates BBCode with headings:
```
[h2]Intro[/h2]
[p]Intro text...[/p]

[h2]Origin[/h2]
[p]Origin text...[/p]
```

## Available Mappings

### Google Sheets Mappings

#### `gspread_fantasy_spells_2_WA.json`
Maps fantasy spell spreadsheet to World Anvil spell template.

**Source Columns**: Spell Name, Level, School, Description, etc.
**World Anvil Template**: `spell`

#### `gspread_fantasy_species_2_WA.json`
Maps fantasy species spreadsheet to World Anvil species template.

**Source Columns**: Name, Size, Speed, Traits, Languages, etc.
**World Anvil Template**: `species`

**Special Features**:
- Multiple traits with array notation (`traits[0]`, `traits[1]`, etc.)
- Nested content sections (Intro, Origin, Culture, etc.)
- Ability scores and language lists

#### `gspread_fantasy_monsters_2_wa.json`
Maps fantasy monster spreadsheet to World Anvil article template.

**Source Columns**: Name, Size, Type, AC, HP, Stats, etc.
**World Anvil Template**: `article`

### Obsidian Portal Mappings

#### `obsidianportal_journal_2_wa.json`
Maps Obsidian Portal adventure log entries to World Anvil articles.

**Source Fields**: title, published, content
**World Anvil Template**: `article`

#### `obsidianportal_characters_2_wa.json`
Maps Obsidian Portal characters to World Anvil character sheets.

**Source Fields**: title, content, pc (boolean)
**World Anvil Template**: `character`

#### `obsidianportal_items_2_wa.json`
Maps Obsidian Portal items to World Anvil item articles.

**Source Fields**: title, category, content
**World Anvil Template**: `item`

## Creating New Mappings

1. **Identify Source Fields**: List all column headers or field names from your source
2. **Identify World Anvil Fields**: Check World Anvil API documentation or existing articles
3. **Create JSON File**: Map WA fields to source fields
4. **Test Conversion**: Use the preview feature in the notebook
5. **Iterate**: Adjust mappings based on preview output

### Example Workflow

```python
# In the notebook
mapping = load_mapping("my_new_mapping")
sample_row = {"Name": "Test Item", "Description": "Test description"}
result = convert_with_mapping(sample_row, mapping, "article")
print(json.dumps(result, indent=2))
```

## World Anvil Field Reference

### Common Fields
- `title` - Article title
- `content` - Main article content (BBCode)
- `templateType` - Template to use (article, spell, character, etc.)
- `state` - Publication state (private, public)
- `tags` - Comma-separated tags
- `cover` - Cover image URL
- `icon` - Icon identifier

### Template-Specific Fields

#### Spell Template
- `level` - Spell level (0-9)
- `school` - School of magic
- `castingtime` - Casting time
- `duration` - Duration
- `spellrange` - Range
- `material` - Material components
- `ritual` - Boolean
- `concentration` - Boolean

#### Species Template
- `size` - Size category
- `speed.walk` - Walking speed
- `traits[].name` - Trait name
- `traits[].ability` - Associated ability
- `languages.list` - Known languages
- `languages.count` - Number of languages

#### Character Template
- `title` - Character name
- `content` - Character description
- `age` - Age
- `gender` - Gender
- `species` - Species/race

## BBCode Formatting

The converter automatically formats content using BBCode:
- Paragraphs: `[p]text[/p]`
- Headings: `[h2]Section[/h2]`
- Bold: `[b]text[/b]`
- Italic: `[i]text[/i]`
- Links: `[url=https://example.com]text[/url]`

Plain text in `content` fields is automatically wrapped in `[p]` tags.

## Tips

1. **Start Simple**: Begin with just title and content, then add more fields
2. **Test with Previews**: Always preview conversions before syncing
3. **Use Consistent Names**: Keep mapping file names descriptive
4. **Document Special Cases**: Add comments in README for complex mappings
5. **Version Control**: Commit mapping files to track changes over time

## Troubleshooting

### Field Not Appearing
- Check spelling of both WA field and source column
- Verify the source column has data (not empty/null)
- Check if field is supported by the template type

### Content Formatting Issues
- Ensure `content` field uses BBCode syntax
- Use `content.SectionName` for structured content
- Check for special characters that need escaping

### Array Fields Not Working
- Verify bracket notation: `field[0]`, `field[1]`, etc.
- Ensure indices are sequential starting from 0
- Check that parent field is initialized as array
