from device_families.schlage.schlage_client import SchlageClient, SchlageLock


class _Resp:
    def json(self):
        return {"identityId": "user-1"}


def _client():
    client = SchlageClient(auth=None)
    client.calls = []
    client._request = lambda method, path, **kw: client.calls.append((method, path, kw.get("json"))) or _Resp()
    return client


def _lock(device_type: str) -> SchlageLock:
    return SchlageLock.from_json({"deviceId": "d1", "devicetypeId": device_type, "CAT": "cat-1",
                                  "attributes": {"lockState": 1}})


def test_wifi_lock_unlocks_with_an_attribute_put():
    client = _client()
    client.unlock(_lock("be489wifi2"))
    assert client.calls == [("PUT", "devices/d1", {"attributes": {"lockState": 0}})]


def test_other_locks_unlock_with_a_changelockstate_command():
    client = _client()
    client.unlock(_lock("be479ble"))
    assert client.calls == [
        ("GET", "users/@me", None),
        ("POST", "devices/d1/commands",
         {"data": {"CAT": "cat-1", "deviceId": "d1", "state": 0, "userId": "user-1"}, "name": "changelockstate"}),
    ]


def _states(*lock_states):
    """A client whose refresh returns these lockStates in turn; sleeps are recorded, not taken."""
    client = SchlageClient(auth=None)
    seq = iter(lock_states)
    client.refresh = lambda device_id: SchlageLock.from_json(
        {"deviceId": device_id, "attributes": {"lockState": next(seq)}})
    client.sleeps = []
    return client


def test_wait_for_returns_once_the_lock_reports_the_requested_state():
    client = _states(1, 1, 0, 1)
    lock = client.wait_for("d1", locked=False, sleep=client.sleeps.append)
    assert lock.is_locked is False and len(client.sleeps) == 3


def test_wait_for_gives_up_after_its_tries():
    client = _states(*[1] * 7)
    lock = client.wait_for("d1", locked=False, sleep=client.sleeps.append)
    assert lock.is_locked is True and len(client.sleeps) == 7


def test_wait_for_stops_on_a_jam():
    client = _states(1, 2)
    lock = client.wait_for("d1", locked=False, sleep=client.sleeps.append)
    assert lock.is_jammed and len(client.sleeps) == 2
