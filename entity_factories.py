from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

player = Actor(
    char="@",
    codepoint=chr(0x100000),  # Map codepoint to the character sprite and use this instead of '@'
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=1, base_power=2),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)

orc = Actor(
    char="o",
    codepoint=chr(0x100001),
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)
troll = Actor(
    char="T",
    codepoint=chr(0x100002),
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)

confusion_scroll = Item(
    char="~",
    codepoint=chr(0x100003),
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    char="~",
    codepoint=chr(0x100003),
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
lightning_scroll = Item(
    char="~",
    codepoint=chr(0x100003),
    color=(255, 255, 255),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

health_potion = Item(
    char="!",
    codepoint=chr(0x100004),
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)

dagger = Item(
    char="/", codepoint=chr(0x100005), color=(0, 191, 255), name="Dagger", equippable=equippable.Dagger()
)
sword = Item(char="/", codepoint=chr(0x100005), color=(0, 191, 255), name="Sword", equippable=equippable.Sword())

leather_armor = Item(
    char="[",
    codepoint=chr(0x100006),
    color=(139, 69, 99),
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
)
chain_mail = Item(
    char="[", codepoint=chr(0x100006), color=(139, 69, 99), name="Chain Mail", equippable=equippable.ChainMail()
)
