import enum
import re

from decimal import Decimal

import emoji as emojilib


class _EmojiQual(str, enum.Enum):
    FullyQualified = "fully-qualified"
    MinimalQualified = "minimally-qualified"
    Unqualified = "unqualified"
    Component = "component"


file = open('emoji-test.txt', 'r')


def parse_row(row: str, group: str, subgroup: str):
    characters = row[:55].strip().split(' ')
    emoji = ''.join([chr(int(c, 16)) for c in characters])
    qualification = _EmojiQual(row[56:76].strip())
    version = Decimal(re.search(r'E\d+\.\d+', row[76:100].strip()).group(0)[1:])
    name = ""  # TODO
    child_of = ""  # TODO
    return [emoji, group, subgroup, name, child_of, emojilib.demojize(emoji), qualification, version]


group = None
subgroup = None
for line in file.readlines():
    line = line.strip()
    if line == '':
        continue
    elif line.startswith('#'):
        if line.startswith('# group:'):
            group = line[9:].strip()
        elif line.startswith('# subgroup:'):
            subgroup = line[12:].strip()
    else:
        line_data = parse_row(row=line, group=group, subgroup=subgroup)
        if line_data[6] is _EmojiQual.FullyQualified and line_data[7] >= Decimal('4.0'):
            print(line_data)

file.close()
