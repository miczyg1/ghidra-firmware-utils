#!/usr/bin/env python3

import os
import re
import sys

stream = os.popen('grep --exclude-dir=.git -r -E \".*Guid\s+= \{.*0x\"')
GUIDS = stream.read()

for line in GUIDS.splitlines():
	try:
		line = line[:line.index('}')]
	except ValueError:
		print("incorrectly formatted line {}".format(line) ,file=sys.stderr)
		continue

	tmp = line.split(':')[-1]
	tmp = tmp.replace('EFI_GUID', '')
	tmp = tmp.replace('GUID', '')
	tmp = tmp.replace(' ', '')
	tmp = tmp.replace('#', '')

	name = tmp.split('=')[0]
	name = name.replace('GLOBAL_REMOVE_IF_UNREFERENCEDEFI_', '')
	GUID = tmp.split('=')[1]
	GUID = GUID.replace('{','')
	GUID = GUID.replace('}','')
	GUID = GUID.replace('0x','')
	GUID = GUID.replace(';','')

	Data1 = GUID.split(',')[0].zfill(8).upper() # 32 bit
	Data2 = GUID.split(',')[1].zfill(4).upper() # 16 bit
	Data3 = GUID.split(',')[2].zfill(4).upper() # 16 bit
	Data4 = GUID.split(',')[3].zfill(2).upper() + GUID.split(',')[4].zfill(2).upper() # 16 bit
	Data5 = ''

	for byte in GUID.split(',')[5:]:
		Data5 = Data5 + byte.zfill(2).upper()

	print ("{}-{}-{}-{}-{},{}".format(Data1, Data2, Data3, Data4, Data5, name))
