"""Configuration of pytest tests."""

import pytest
import redis

pytest_plugins = 'pytester'


def pytest_addoption(parser):
    """Create pytest-redis test options."""
    parser.addoption('--redis-host', metavar='redis_host',
                     type=str, help='The host of the redis instance.',
                     required=True)
    parser.addoption('--redis-port', metavar='redis_port',
                     type=str, help='The port of the redis instance.',
                     required=True)
    parser.addoption('--redis-list-key', metavar='redis_list_key',
                     type=str,
                     help=('The key of the redis list containing '
                           'the test paths to execute.'),
                     required=True)
    parser.addoption("--force", dest='feature', action='store_true',
                     help=('A boolean value indicating if existing'
                           'redis lists should be deleted before starting'
                           'tests'),
                     default=False)


@pytest.fixture
def redis_host(request):
    """Return redis_host cmdline arg."""
    return request.config.getoption("--redis-host")


@pytest.fixture
def redis_port(request):
    """Return redis_port cmdline arg."""
    return request.config.getoption("--redis-port")


@pytest.fixture
def redis_list_key(request):
    """Return redis_list_key cmdline arg."""
    return request.config.getoption("--redis-list-key")


@pytest.fixture
def force_del_lists(request):
    """Return force_del_lists cmdline arg."""
    return request.config.getoption("--force")


@pytest.fixture
def redis_args(redis_host, redis_port, redis_list_key):
    """Return cmdline args for redis."""
    return {
        'redis-host': redis_host,
        'redis-port': redis_port,
        'redis-list-key': redis_list_key
    }


@pytest.fixture
def redis_connection(redis_args, force_del_lists):
    """Return redis_connection and check for empty redist-list-key."""
    r_client = redis.StrictRedis(host=redis_args['redis-host'],
                                 port=redis_args['redis-port'])
    if r_client.llen(redis_args['redis-list-key']):
        if not force_del_lists:
            exit_string = ("redis list '{}' exists in redis instance. "
                           "pass --force to ignore this and delete "
                           "list.").format(redis_args['redis-list-key'])
            pytest.exit(exit_string)
        else:
            print "Deleting pre-exiting redi list '{}'".format(
                redis_args['redis-list-key'])
            r_client.delete(redis_args['redis-list-key'])

    return r_client
