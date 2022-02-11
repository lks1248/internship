import sys
from parser_working import eat_snapshot

src = sys.argv[1] #filepath to binary input file
header, gas, dm = eat_snapshot(src)
out = src + ".txt"
gas.write(out, format='ascii', overwrite=True)
