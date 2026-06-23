from app.rules.engine import evaluate_rule

def test_rule_triggered():
    event={'device_mac':'AA:BB:CC','rssi':-55}
    rule={'conditions':{'device_mac':'AA:BB:CC'}}
    assert evaluate_rule(event, rule)
