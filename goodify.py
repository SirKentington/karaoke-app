#!/usr/bin/env python

import sys
import re

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

lines = [line.replace('.mp3', '').strip() for line in lines if 'mp3' in line]
lines = [re.sub(r'\[.+\]', '', line).strip() for line in lines]

for line in lines:
    tokens = line.split('-')
    print '%s # %s' % ('-'.join(tokens[:-1]), tokens[-1])

# vim: set expandtab sw=4 ts=4:
