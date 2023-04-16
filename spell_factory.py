from components.ai import SpellAI
from components.castable import BasicSpell, Castable
from components.spell_book import SpellBook
from entity import Actor, Spell

basic_spell = Spell(
    char="*",
    codepoint=chr(0x100000),  # Map codepoint to the character sprite and use this instead of '@'
    color=(255, 255, 255),
    name="Basic Spell",
    ai_cls=SpellAI,
    castable=BasicSpell(spell_power=1, spell_range=4),
)
