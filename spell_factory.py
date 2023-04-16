from components.ai import SpellAI
from components.castable import BasicSpell
from entity import Spell

basic_spell = Spell(
    name="Basic Spell",
    ai_cls=None,
    castable=BasicSpell(spell_power=1, spell_range=4, spell_colors=None),
)
