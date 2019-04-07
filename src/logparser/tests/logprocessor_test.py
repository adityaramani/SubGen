from context import logprocessor
import json
import pytest


def global_schema():
    return json.load(open("../resources/schema.json"))

def cb(l):
    print (l)

processor = logprocessor.LogProcessor(global_schema(),cb)

def test_logprocessor():


        fp = open('../test/qosproc.log','r')
        accepted = 0
        for line in fp:
                ret = processor.read_line(line)
                if ret is True:
                        accepted+=1

        assert accepted == 205