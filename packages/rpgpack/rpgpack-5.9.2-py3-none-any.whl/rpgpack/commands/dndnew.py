import re
# noinspection PyUnresolvedReferences
from royalnet.commands import *
import royalnet.utils as ru
from ..tables import DndCharacter
from ..types import DndProficiencyType


class DndnewCommand(Command):
    name: str = "dndnew"

    description: str = "Create a new DnD character."

    aliases = ["dn", "dndn", "new", "dnew"]

    syntax = "{name}\n{character_sheet}"

    @staticmethod
    def _search_value(name: str, string: str):
        return re.search(r"\s*" + name + r"\s*([0-9.]+)\s*", string, re.IGNORECASE)

    def _parse(self, character_sheet: str) -> dict:
        columns = list(self.alchemy.get(DndCharacter).__table__.columns)
        column_names = [column.name for column in columns if (not column.primary_key and
                                                              not column.foreign_keys and
                                                              column.name != "name")]
        arguments = {}
        for column_name in column_names:
            match = self._search_value(column_name, character_sheet)
            if match:
                if column_name.endswith("_proficiency"):
                    arguments[column_name] = DndProficiencyType(float(match.group(1)))
                else:
                    arguments[column_name] = match.group(1)
        return arguments

    def _syntax(self) -> str:
        columns = list(self.alchemy.get(DndCharacter).__table__.columns)
        column_names = [column.name for column in columns if (not column.primary_key and
                                                              not column.foreign_keys and
                                                              column.name != "name")]
        message = "ℹ️ How to create a new character:\n[p]/dndnew YOUR_CHARACTER_NAME\n"
        for column_name in column_names:
            message += f"{column_name} _\n"
        message += "[/p]"
        return message

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        character_sheet = args.joined()

        if character_sheet == "":
            await data.reply(self._syntax())
            return

        async with data.session_acm() as session:
            creator = await data.find_author(session=session, required=True)

            name, rest = character_sheet.split("\n", 1)

            character = self.alchemy.get(DndCharacter)(name=name, creator=creator, **self._parse(rest))
            session.add(character)

            try:
                await ru.asyncify(session.commit)
            except Exception as err:
                # THIS IS INTENDED
                if err.__class__.__name__ == "IntegrityError":
                    param_name = re.search(r'in column "(\S+)"', err.args[0]).group(1)
                    raise CommandError(f"Mandatory parameter '{param_name}' is missing.")
                raise

            await data.reply(f"✅ Character [b]{character.name}[/b] (ID: {character.character_id}) created!")
