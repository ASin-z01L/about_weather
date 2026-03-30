import pytest
from app.providers.ttl_cache import SessionTTLCache


@pytest.fixture()
def session_id():
    return 'session_id_001'


@pytest.fixture()
def session_ttl_cache(session_id):
    session = SessionTTLCache(session_id, {})

    return session


# set
def test_session_set(session_ttl_cache, session_id):
    session_ttl_cache.set('user_name', 'John')

    assert session_ttl_cache._cache.get(session_id, {}).get('user_name') == 'John'


# get(
def test_session_get(session_ttl_cache, session_id):
    session_ttl_cache._cache[session_id].setdefault('user_name', 'John')

    assert session_ttl_cache.get('user_name') == 'John'


def test_session_get_with_default_value(session_ttl_cache):
    assert session_ttl_cache.get('user_name', 'John') == 'John'


# delete
def test_session_delete(session_ttl_cache, session_id):
    session_ttl_cache._cache[session_id].setdefault('user_name', 'John')

    session_ttl_cache.delete('user_name')

    assert session_ttl_cache._cache[session_id] == {}
