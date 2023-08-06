from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *


class DndActiveCharacter:
    __tablename__ = "dndactivecharacters"

    @declared_attr
    def active_character_id(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def character_id(self):
        return Column(Integer, ForeignKey("dndcharacters.character_id"))

    @declared_attr
    def user_id(self):
        return Column(Integer, ForeignKey("users.uid"))

    @declared_attr
    def character(self):
        return relationship("DndCharacter", foreign_keys=self.character_id, backref="activated_by")

    @declared_attr
    def user(self):
        return relationship("User", foreign_keys=self.user_id, backref=backref("dnd_active_characters"))

    @declared_attr
    def interface_name(self):
        return Column(String)

    @declared_attr
    def interface_data(self):
        return Column(LargeBinary)

    def __repr__(self):
        return f"<{self.__class__.__qualname__} for {self.user_id}: {self.character_id}>"
