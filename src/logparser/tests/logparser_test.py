from context import logparser
import json
import pytest

# @pytest.fixture(scope = "module")
def global_schema():
    return json.load(open("../resources/schema.json"))


# @pytest.fixture(scope = "module")
def global_keys():
    a = log_parser()
    return list(global_schema().keys())


def test_strip_meta_success():
    assert logparser.strip_meta("I0201 05:13:43.856241  5396 conf.cpp:252] raw_store_port")  == "raw_store_port"


def call_back(data_store):
    assert data_store == json.loads('{"file stats": "/qosfs/incoming/qos/work/7", "time taken": "14201 milliseconds", "input lines": "300001", "beacons failed": "0", "beacons processed": "300001"}')


def call_back_fail(data_store):
    assert data_store == json.loads('{"file stats": "/qosfs/incoming/qos/work/7", "time taken": "14201 milliseconds"}')

def test_log_input_success():
    lines =   [ "I0228 10:25:45.848237 10420 process.cpp:1325] file stats        :: /qosfs/incoming/qos/work/7",
                "I0228 10:25:45.848372 10420 process.cpp:1326] time taken        :: 14201 milliseconds",
                "I0228 10:27:54.977133 9999 process.cpp:1325] test stats        :: /qosfs/incoming/qos/work/0",
                "I0228 10:25:45.848438 10420 process.cpp:1327] input lines       :: 300001",
                "I0228 10:25:45.848623 10420 process.cpp:1328] beacons failed    :: 0",
                "I0228 10:27:54.977133 9999 process.cpp:1325] key1        :: val1",
                "I0228 10:25:45.848685 10420 process.cpp:1329] beacons processed :: 300001",
                "I0228 10:27:54.977133 9999 process.cpp:1325] key2        :: val2"]
    
    lp = logparser.LogParser(global_schema(), "file stats", call_back)

    lp.insert(lines[0],True)
    for line in lines[1:]:
        lp.insert(line)
    

def test_log_input_fail():
    lines =   [ "I0228 10:25:45.848237 10420 process.cpp:1325] file stats        :: /qosfs/incoming/qos/work/7",
                "I0228 10:25:45.848685 10420 process.cpp:1329] beacons processed :: 300001",]
    
    lp = logparser.LogParser(global_schema(), "file stats", call_back_fail)

    lp.insert(lines[0],True)
    for line in lines[1:]:
        lp.insert(line,False)
    

if __name__ == "__main__":
    test_log_input_success()