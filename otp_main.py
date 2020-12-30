#! /usr/bin/env python3
from jinja2 import DictLoader, Environment
import secrets

# The characters available for the One Time Pad
OTP_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
# The number of characters in each group, separated by spaces
GROUP_SIZE = 5
# The groups in each row of a message, separated by newlines
GROUP_COUNT = 15
# The number of rows per message
ROW_COUNT = 4
# The number of messages per page
MESSAGE_COUNT = 9

def generate_row(group_count=GROUP_COUNT, group_size=GROUP_SIZE):
    """
    Generate a string of random characters, groups in this string are separated by spaces.

    Example:
        NLJDS KW9JG 30AZJ J0XQ4 IRP0Z L6YQT AB7AO RY5XG
    """
    groups = []
    for _ in range(group_count):
        groups.append(''.join([secrets.choice(OTP_CHARS) for _ in range(group_size)]))
    return ' '.join(groups)

def generate_message(row_count=ROW_COUNT, group_count=GROUP_COUNT, group_size=GROUP_SIZE):
    """
    Combine several rows into a single message.
    """
    return '\n'.join(generate_row(group_count, group_size) for _ in range(ROW_COUNT))

# This is the only page.  Links are shortened to make manual typing easier.
templates = {'one_time_pad': '''
<title>One Time Pad - Unique, just for you</title>
<style>
/* Remove decoration from links so they are readable when printed */
a { text-decoration: none; }
</style>
[[ for num, message in messages|enumerate(1) ]]
<pre>Message [- num -]</pre>
<pre>
[- message -]
</pre>
[[ endfor ]]
''', 'one_time_pad_txt':'''[[ for num, message in messages_txt|enumerate(1) ]]Message [- num -]
[- message -]

[[ endfor ]]
''',
}

env = Environment(
    loader=DictLoader(templates),
    autoescape=True,
    block_start_string='[[',
    block_end_string=']]',
    comment_start_string='[#',
    comment_end_string='#]',
    variable_start_string='[-',
    variable_end_string='-]',
)

env.filters['enumerate'] = enumerate