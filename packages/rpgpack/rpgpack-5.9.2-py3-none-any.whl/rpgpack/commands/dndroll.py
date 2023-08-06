import random
import math
from royalnet.commands import *
from ..tables import DndCharacter
from ..utils import get_active_character


class DndrollCommand(Command):
    name: str = "dndroll"

    description: str = "Roll dice as the active DnD character."

    aliases = ["dr", "dndr", "roll", "droll"]

    _skill_names = {
        "str": "strength",
        "for": "strength",
        "dex": "dexterity",
        "des": "dexterity",
        "con": "constitution",
        "cos": "constitution",
        "inte": "intelligence",
        "wis": "wisdom",
        "sag": "wisdom",
        "cha": "charisma",
        "car": "charisma",

        "ststr": "strength_save",
        "stfor": "strength_save",
        "stdex": "dexterity_save",
        "stdes": "dexterity_save",
        "stcon": "constitution_save",
        "stcos": "constitution_save",
        "stint": "intelligence_save",
        "stwis": "wisdom_save",
        "stsag": "wisdom_save",
        "stcha": "charisma_save",
        "stcar": "charisma_save",

        "tsstr": "strength_save",
        "tsfor": "strength_save",
        "tsdex": "dexterity_save",
        "tsdes": "dexterity_save",
        "tscon": "constitution_save",
        "tscos": "constitution_save",
        "tsint": "intelligence_save",
        "tswis": "wisdom_save",
        "tssag": "wisdom_save",
        "tscha": "charisma_save",
        "tscar": "charisma_save",

        "acr": "acrobatics",
        "add": "animal_handling",
        "ani": "animal_handling",
        "arc": "arcana",
        "ath": "athletics",
        "dec": "deception",
        "ing": "deception",
        "his": "history",
        "sto": "history",
        "ins": "insight",
        "intu": "insight",
        "inti": "intimidation",
        "inv": "investigation",
        "med": "medicine",
        "nat": "nature",
        "perc": "perception",
        "perf": "performance",
        "pers": "persuasion",
        "rel": "religion",
        "sle": "sleight_of_hand",
        "soh": "sleight_of_hand",
        "rap": "sleight_of_hand",
        "ste": "stealth",
        "nas": "stealth",
        "sur": "survival",
        "sop": "survival",
    }

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        async with data.session_acm() as session:
            active_character = await get_active_character(session=session, data=data)
            if active_character is None:
                raise CommandError("You don't have an active character.")
            char = active_character.character

            first = args[0]
            second = args.optional(1)
            third = args.optional(2)

            advantage = False
            disadvantage = False
            extra_modifier = 0

            if third:
                try:
                    extra_modifier = int(third)
                except ValueError:
                    raise InvalidInputError("Invalid modifier value (third parameter).")
                if second.startswith("a") or second.startswith("v"):
                    advantage = True
                elif second.startswith("d") or second.startswith("d"):
                    disadvantage = True
                else:
                    raise InvalidInputError("Invalid advantage string (second parameter).")

            elif second:
                try:
                    extra_modifier = int(second)
                except ValueError:
                    if second.startswith("a") or second.startswith("v"):
                        advantage = True
                    elif second.startswith("d") or second.startswith("d"):
                        disadvantage = True
                    else:
                        raise InvalidInputError("Invalid modifier value or advantage string (second parameter).")

            skill_short_name = first.lower()
            for root in self._skill_names:
                if skill_short_name.startswith(root):
                    skill_name = self._skill_names[root]
                    break
            else:
                raise CommandError("Invalid skill name (first parameter).")

            skill_modifier = int(char.__getattribute__(skill_name))
            modifier = skill_modifier + extra_modifier
            modifier_str = f"{modifier:+d}" if modifier != 0 else ""

            if advantage:
                roll_a = random.randrange(1, 21)
                roll_b = random.randrange(1, 21)
                roll = max([roll_a, roll_b])
                total = roll + modifier
                await data.reply(f"🎲 [i]{skill_name.capitalize()}[/i]: 2d20h1{modifier_str} = ({roll_a}|{roll_b} ){modifier_str} = [b]{total}[/b]")
            elif disadvantage:
                roll_a = random.randrange(1, 21)
                roll_b = random.randrange(1, 21)
                roll = min([roll_a, roll_b])
                total = roll + modifier
                await data.reply(f"🎲 [i]{skill_name.capitalize()}[/i]: 2d20l1{modifier_str} = ({roll_a}|{roll_b}){modifier_str} = [b]{total}[/b]")
            else:
                roll = random.randrange(1, 21)
                total = roll + modifier
                await data.reply(f"🎲 [i]{skill_name.capitalize()}[/i]: 1d20{modifier_str} = {roll}{modifier_str} = [b]{total}[/b]")
