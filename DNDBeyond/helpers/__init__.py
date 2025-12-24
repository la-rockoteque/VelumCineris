from .DnDBeyondAPI import DnDBeyondAPI
from .converter import convert_spell_to_ddb

# Helper function for spreadsheet DDB ID normalization
normalize_ddb_id = DnDBeyondAPI.normalize_ddb_id

__all__ = ['DnDBeyondAPI', 'convert_spell_to_ddb', 'normalize_ddb_id']
