from nose.tools import *
from unittest import TestCase
from unittest.mock import patch
from factom_sdk.request_handler.request_handler import RequestHandler


class TestRequestHandlerParams(TestCase):
    """Test Request Handler Params"""
    def test_url_is_not_valid(self):
        """Check base_url valid"""
        with assert_raises(Exception) as cm:
            RequestHandler("google", "1", "2")
            assert_true("The base_url provided is not valid." in str(cm.exception))

    def test_app_id_is_not_valid(self):
        """Check app_id valid"""
        with assert_raises(Exception) as cm:
            RequestHandler("http://google.com", 1, "2")
            assert_true("The app_id provided is not valid." in str(cm.exception))

    def test_app_key_is_not_valid(self):
        """Check app_key valid"""
        with assert_raises(Exception) as cm:
            RequestHandler("http://google.com", "1", 2)
            assert_true("The app_key provided is not valid." in str(cm.exception))

    def test_initial_success(self):
        """Check initial"""
        request_handler = RequestHandler("http://google.com", "1", "2")
        assert_equal(request_handler.base_url, "http://google.com")
        assert_equal(request_handler.app_id, "1")
        assert_equal(request_handler.app_key, "2")


class TestRequestHandler(TestCase):
    """Test Request Handler"""
    def setUp(self):
        self.request_handler = RequestHandler("http://google.com", "1", "2")

    def tearDown(self):
        self.request_handler = None

    def test_send_get_request(self):
        """Check send get request successfully"""
        with patch("factom_sdk.request_handler.request_handler.requests.get") as mock_get:
            mock_get.return_value.ok = True
            response = self.request_handler.get("")
            assert_is_not_none(response)

    def test_send_post_request(self):
        """Check Send post request successfully"""
        with patch("factom_sdk.request_handler.request_handler.requests.post") as mock_post:
            mock_post.return_value.ok = True
            response = self.request_handler.post("")
            assert_is_not_none(response)

