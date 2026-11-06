from device_families.schlage.protocol import _lock_state
from device_families.schlage.schlage_client import SchlageLock


def _lock(lock_state: int) -> SchlageLock:
    return SchlageLock.from_json({"deviceId": "d1", "attributes": {"lockState": lock_state}})


def test_lock_state_follows_lock_state_attribute():
    assert _lock_state(_lock(1)) == "locked"
    assert _lock_state(_lock(0)) == "unlocked"
    assert _lock_state(_lock(2)) == "jammed"
