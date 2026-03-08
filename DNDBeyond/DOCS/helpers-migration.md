# Helpers Migration (DNDBeyond)

## Canonical location

Helper code now lives under:

- `DNDBeyond/core/Helpers/`
- `DNDBeyond/core/Helpers/entities/`

Use these paths for all new imports in Python files.

## Backward compatibility

Legacy imports from `DNDBeyond.helpers` still work through compatibility shims:

- `DNDBeyond/helpers/*.py`
- `DNDBeyond/helpers/entities/*.py`

This keeps existing notebooks and scripts functional while migration continues.

## Import guidance

Preferred:

```python
from DNDBeyond.core.Helpers import convert_spell_to_ddb
from DNDBeyond.core.Helpers.DnDBeyondAPI import DnDBeyondAPI
```

Legacy (still supported):

```python
from DNDBeyond.helpers import convert_spell_to_ddb
from DNDBeyond.helpers.DnDBeyondAPI import DnDBeyondAPI
```
