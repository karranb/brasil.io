import json
from unittest.mock import Mock, patch

from django.test import TestCase, override_settings
from redis.client import Redis

from traffic_control.blocked_list import blocked_requests


class BlockedRequestListTests(TestCase):
    def test_in_memory_enqueueing(self):
        blocked_requests.clear()

        msg_1, msg_2 = {"path": "/"}, {"path": "/about/"}
        blocked_requests.lpush(msg_1)
        blocked_requests.lpush(msg_2)

        assert 2 == len(blocked_requests)
        assert msg_2 == blocked_requests.lpop()
        assert msg_1 == blocked_requests.lpop()
        assert 0 == len(blocked_requests)

    @override_settings(RQ_BLOCKED_REQUESTS_LIST="blocked_list")
    @patch("traffic_control.blocked_list.get_redis_connection")
    def test_redis_enqueing(self, mocked_get_conn):
        blocked_requests.__dict__.pop("redis_conn", None)
        conn = Mock(Redis, autospec=True)
        mocked_get_conn.return_value = conn
        msg = {"path": "/"}
        json_msg = json.dumps(msg)

        blocked_requests.lpush(msg)

        mocked_get_conn.assert_called_once_with("default")
        conn.lpush.assert_called_once_with("blocked_list", json_msg)

        conn.lpop.return_value = json_msg
        data = blocked_requests.lpop()
        assert msg == data

        conn.lpop.assert_called_once_with("blocked_list")
        blocked_requests.__dict__.pop("redis_conn", None)
