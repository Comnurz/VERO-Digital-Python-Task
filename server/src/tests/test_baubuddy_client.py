import unittest
from unittest.mock import patch, MagicMock, Mock

import requests

from helpers.baubuddy_client import BaubuddyClient

class TestBaubuddyClient(unittest.TestCase):
    @patch('src.helpers.baubuddy_client.requests.request')
    def test_authenticate_successful(self, mock_request):
        res = MagicMock()
        res.json.return_value = {'oauth': {'access_token': 'test_token'}}
        res.status_code = 200

        mock_request.return_value = res

        client = BaubuddyClient()
        client._authenticate()
        self.assertEqual('test_token', client.TOKEN)

    @patch('src.helpers.baubuddy_client.requests.request')
    def test_authenticate_failure(self, mock_request):
        mock_request.return_value.status_code = 401
        mock_request.side_effect = requests.exceptions.HTTPError
        client = BaubuddyClient()
        with self.assertRaises(requests.exceptions.HTTPError):
            client._authenticate()

    @patch('src.helpers.baubuddy_client.requests.request')
    @patch('src.helpers.baubuddy_client.BaubuddyClient._authenticate')
    def test_request_with_valid_token(self, mock_authenticate, mock_request):
        res = MagicMock()
        res.json.return_value = {'data': 'test_data'}
        res.status_code = 200

        mock_request.return_value = res

        client = BaubuddyClient()
        client.TOKEN = 'valid_token'
        result = client._request('GET', 'https://127.0.0.1:8000/index.php/v1/test')
        self.assertEqual(result, {'data': 'test_data'})
        mock_authenticate.assert_not_called()

    @patch('src.helpers.baubuddy_client.requests.request')
    @patch.object(BaubuddyClient, '_authenticate')
    def test_request_with_invalid_token(self, mock_authenticate, mock_request):
        mock_request.side_effect = [
            MagicMock(status_code=401, raise_for_status=Mock(side_effect=requests.exceptions.HTTPError)),
            MagicMock(status_code=200, json=Mock(return_value={'data': 'test_data'}))]
        mock_authenticate.return_value = 'valid_token'
        client = BaubuddyClient()
        client.TOKEN = 'invalid_token'
        result = client._request('GET', 'https://127.0.0.1:8000/index.php/v1/test')
        self.assertEqual(result, {'data': 'test_data'})
        mock_authenticate.assert_called_once()

    @patch('src.helpers.baubuddy_client.requests.request')
    @patch.object(BaubuddyClient, '_authenticate')
    def test_request_check_if_it_raises_error(self, mock_authenticate, mock_request):
        mock_request.side_effect = [
            MagicMock(status_code=401, raise_for_status=Mock(side_effect=requests.exceptions.HTTPError)),
            MagicMock(status_code=401, raise_for_status=Mock(side_effect=requests.exceptions.HTTPError)),
            MagicMock(status_code=200, json=Mock(return_value={'data': 'test_data'}))]
        mock_authenticate.return_value = 'invalid_token'
        client = BaubuddyClient()
        client.TOKEN = 'invalid_token'
        with self.assertRaises(requests.exceptions.HTTPError):
            client._request('GET', 'https://127.0.0.1:8000/index.php/v1/test')
        mock_authenticate.assert_called_once()

    @patch.object(BaubuddyClient, '_request')
    def test_get_vehicles(self, mock_request):
        mock_request.return_value = [{'data': 'test_data'}]

        client = BaubuddyClient()
        res = client.get_vehicles()
        self.assertEqual([{'data': 'test_data'}], res)
        mock_request.called_with('GET', 'v1/vehicles/select/active')

    @patch.object(BaubuddyClient, '_request')
    def test_get_colors(self, mock_request):
        mock_request.return_value = [{'colorCode': 'test_color'}]

        client = BaubuddyClient()
        res = client.get_colors(1)
        self.assertEqual('test_color', res)
        mock_request.called_with('GET', 'v1/labels/1')
