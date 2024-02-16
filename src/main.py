import enum

from dataclasses import dataclass
from decimal import Decimal


class _EmojiVersion(str, enum.Enum):
    E1_0 = "1.0"
    E2_0 = "2.0"
    E3_0 = "3.0"
    E4_0 = "4.0"
    E5_0 = "5.0"
    E11_0 = "11.0"
    E12_0 = "12.0"
    E12_1 = "12.1"
    E13_0 = "13.0"
    E13_1 = "13.1"
    E14_0 = "14.0"
    E15_0 = "15.0"
    E15_1 = "15.1"


@dataclass()
class Emoji:
    emoji: str
    alias: str
    version: Decimal
    _variants: list[Emoji] | None = None

    @property
    def variants(self) -> list[str]:
        out = []
        for variant in self._variants:
            out.append(variant.emoji)
        return out


class EmojiContainer:

    def emojis(self) -> list[Emoji]:
        pass


class EmojiGroup(EmojiContainer):

    def __init__(self):
        pass

    def subgroups(self) -> list[EmojiContainer]:
        pass


class EmojiIndex:

    def __init__(self):
        self._version = _EmojiVersion.E15_1

    @property
    def version(self) -> _EmojiVersion:
        return self._version

    def set_version(self, version: str):
        if version in _EmojiVersion.__members__.values():
            self._version = _EmojiVersion(version)
        else:
            raise ValueError(f"Version {version} not supported")

    @staticmethod
    def groups(version: str | None = None) -> list[EmojiGroup]:
        # TODO
        pass
