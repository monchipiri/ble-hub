from unittest.mock import Mock

def test_scanner_callback():
    cb=Mock()
    cb({'address':'AA:BB:CC'})
    cb.assert_called_once()
