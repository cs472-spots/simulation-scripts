#!/usr/bin/env python
import sys

def write(s):
    sys.stdout.write(s)

def writeSpot(spot, indent):
    write('{indent}"{label}" : false,\n'.format(indent=indent*2, label='authorized'))
    write('{indent}"{label}" : "",\n'.format(indent=indent*2, label='occupant'))
    write('{indent}"{label}" : "staff",\n'.format(indent=indent*2, label='type'))
    write('{indent}"{label}" : "false",\n'.format(indent=indent*2, label='vacancy'))
    write('{indent}"{label}" : {lat},\n'.format(indent=indent*2, label='latitude', lat=spot[0]))
    write('{indent}"{label}" : {lon}\n'.format(indent=indent*2, label='longitude', lon=spot[1]))

def writeLot(f, spots):
    write("{\n")
    spotsLen = len(spots)

    for spotNumber, spot in zip(range(spotsLen), spots):
        write('  "{:0>4}" : {{\n'.format(spotNumber))
        writeSpot(spot, '  ')
        write('  }}{}\n'.format("," if spotNumber < spotsLen-1 else ""))

    write("}\n")

spots = [
        (36.106795, -115.143744),
        (36.106818, -115.143744),
        (36.106841, -115.143744),
        (36.106867, -115.143744),
        (36.106894, -115.143744),
        (36.106916, -115.143744),
        (36.106942, -115.143744),
        (36.106967, -115.143744),
        (36.106992, -115.143744)
        ]

filename = sys.argv[1]

spotsFile = open(filename, 'w')

writeLot(spotsFile, spots)
