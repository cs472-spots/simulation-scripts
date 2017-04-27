#!/usr/bin/env python
import sys

def write(s):
    sys.stdout.write(s)

def writeSpot(spot, indent):
    spotString = '{indent}"{label}" : false,\n'.format(indent=indent*2, label='authorized')
    spotString += '{indent}"{label}" : "",\n'.format(indent=indent*2, label='occupant')
    spotString += '{indent}"{label}" : "staff",\n'.format(indent=indent*2, label='type')
    spotString += '{indent}"{label}" : "false",\n'.format(indent=indent*2, label='vacancy')
    spotString += '{indent}"{label}" : {lat},\n'.format(indent=indent*2, label='latitude', lat=spot[0])
    spotString += '{indent}"{label}" : {lon}\n'.format(indent=indent*2, label='longitude', lon=spot[1])
    return spotString

def writeLot(spots):
    lotString = "{\n"
    spotsLen = len(spots)

    for spotNumber, spot in zip(range(spotsLen), spots):
        lotString += '  "{:0>4}" : {{\n'.format(spotNumber)
        lotString += writeSpot(spot, '  ')
        lotString += '  }}{}\n'.format("," if spotNumber < spotsLen-1 else "")

    lotString += "}\n"
    return lotString

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

print writeLot(spots)
