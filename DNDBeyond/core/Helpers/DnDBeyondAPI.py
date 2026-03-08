from .client import DndBeyondClient
from .entities.backgrounds import BackgroundEntity
from .entities.feats import FeatEntity
from .entities.monsters import MonsterEntity
from .entities.species import SpeciesEntity
from .entities.spells import SpellEntity
from .utils import create_slug, normalize_ddb_id


class DnDBeyondAPI:
    """Facade for D&D Beyond homebrew entities."""

    def __init__(
        self,
        session,
        security_token: str,
        authenticity_token: str,
        verification_token: str = None,
    ):
        self.client = DndBeyondClient(
            session,
            security_token,
            authenticity_token,
            verification_token=verification_token,
        )
        self.spells = SpellEntity(self.client)
        self.species = SpeciesEntity(self.client)
        self.monsters = MonsterEntity(self.client)
        self.backgrounds = BackgroundEntity(self.client)
        self.feats = FeatEntity(self.client)

    @property
    def last_error(self):
        return self.client.last_error

    @last_error.setter
    def last_error(self, value):
        self.client.last_error = value

    @property
    def last_response(self):
        return self.client.last_response

    @last_response.setter
    def last_response(self, value):
        self.client.last_response = value

    @staticmethod
    def normalize_ddb_id(ddb_id):
        return normalize_ddb_id(ddb_id)

    @staticmethod
    def create_slug(name):
        return create_slug(name)

    def get_user_spells(self):
        return self.spells.list()

    def find_spell_by_name(self, name: str, user_spells=None):
        return self.spells.find_by_name(name, user_spells)

    def create_spell(self, data):
        return self.spells.create(data)

    def update_basic_information(self, spell_id, slug, data):
        return self.spells.update(spell_id, slug, data)

    def create_higher_level(self, spell_id, level_data):
        return self.spells.create_higher_level(spell_id, level_data)

    def create_modifier(self, spell_id, modifier_data):
        return self.spells.create_modifier(spell_id, modifier_data)

    def create_condition(self, spell_id, condition_data):
        return self.spells.create_condition(spell_id, condition_data)

    def delete_spell(self, spell_id, spell_name=None):
        return self.spells.delete(spell_id)

    def get_spell_extras(self, spell_id, slug):
        return self.spells.get_spell_extras(spell_id, slug)

    def delete_modifier(self, spell_id, modifier_id):
        return self.spells.delete_modifier(spell_id, modifier_id)

    def delete_condition(self, spell_id, condition_id):
        return self.spells.delete_condition(spell_id, condition_id)

    def delete_higher_level(self, spell_id, level_id):
        return self.spells.delete_higher_level(spell_id, level_id)

    def get_spell_details(self, spell_id, slug):
        return self.spells.get_spell_details(spell_id, slug)

    def publish_spell(self, spell_id):
        return self.spells.publish_spell(spell_id)

    def unpublish_spell(self, spell_id):
        return self.spells.unpublish_spell(spell_id)

    def get_user_backgrounds(self):
        return self.backgrounds.list()

    def find_background_by_name(self, name: str, user_backgrounds=None):
        return self.backgrounds.find_by_name(name, user_backgrounds)

    def create_background(self, data):
        return self.backgrounds.create(data)

    def update_background(self, background_id, slug, data):
        return self.backgrounds.update(background_id, slug, data)

    def delete_background(self, background_id):
        return self.backgrounds.delete(background_id)

    def get_user_feats(self):
        return self.feats.list()

    def find_feat_by_name(self, name: str, user_feats=None):
        return self.feats.find_by_name(name, user_feats)

    def create_feat(self, data):
        return self.feats.create(data)

    def update_feat(self, feat_id, slug, data):
        return self.feats.update(feat_id, slug, data)

    def delete_feat(self, feat_id):
        return self.feats.delete(feat_id)
