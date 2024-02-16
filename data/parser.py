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

unsupported_name = ['handshake', 'people with bunny ears', 'men with bunny ears', 'women with bunny ears',
                    'people wrestling', 'men wrestling', 'women wrestling',
                    'woman and man holding hands', 'men holding hands', 'women holding hands', 'people holding hands',
                    'kiss', 'couple with heart', 'family']

unsupported_modifier = ['beard', 'bald', 'blond hair', 'white hair', 'curly hair', 'red hair']


def parse_row(row: str, group: str, subgroup: str):
    characters = row[:55].strip().split(' ')
    emoji = ''.join([chr(int(c, 16)) for c in characters])
    qualification = _EmojiQual(row[56:76].strip())
    version = Decimal(re.search(r'E\d+\.\d+', row[76:].strip()).group(0)[1:])
    raw_name = re.search(r'E\d+\.\d+(.*)', row[76:].strip()).group(1).strip()
    split_name = raw_name.split(': ')
    if len(split_name) > 1:
        if split_name[0] in ['flag', 'keycap']:
            name = ": ".join(split_name)
            child_of = ""
        else:
            split_name = [split_name[0]] + [s.strip() for s in split_name[1].split(',')]
            if split_name[0] in unsupported_name:
                return None
            else:
                for modifier in split_name[1:]:
                    if modifier in unsupported_modifier:
                        return None

                name = ": ".join(split_name)
                child_of = split_name[0]
    else:
        name = split_name[0]
        child_of = None

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
        if line_data is not None and line_data[6] is _EmojiQual.FullyQualified:
            print(line_data)

file.close()
