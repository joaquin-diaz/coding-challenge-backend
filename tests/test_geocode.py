import copy

import unittest
from unittest.mock import patch, MagicMock

from .common import mock_response, mock_response_2
from geocode import append_coordinates_to_locations, _get_coordinates_from_address
import geocode

class TestGeocode(unittest.TestCase):
  @patch('geocode._get_coordinates_from_address')
  def test_get_coordinates_from_locations(self, mock_get_coordinates):
    append_coordinates_to_locations(mock_response)

    mock_get_coordinates.assert_called_once_with('Epic Roasthouse (399 Embarcadero)')

  @patch('geocode._get_coordinates_from_address')
  def test_get_coordinates_from_locations_local_cache(self, mock_get_coordinates):
    append_coordinates_to_locations(mock_response_2)
    # Subsequence calls should not get coordinates from Google
    append_coordinates_to_locations(mock_response_2)
    append_coordinates_to_locations(mock_response_2)

    mock_get_coordinates.assert_called_once_with('Hyde St at Chestnut St')

  @patch('geocode._get_coordinates_from_address')
  def test_get_coordinates_from_locations_store_coordinates(self, mock_get_coordinates):
    mock_response_3 = [copy.deepcopy(mock_response[0])]
    mock_response_3[0]['locations'] = 'Some Street 123' 

    mock_coordinates = {'lat': 123, 'lng': 456}
    mock_get_coordinates.return_value = mock_coordinates

    append_coordinates_to_locations(mock_response_3)

    self.assertEqual(mock_response_3[0]['coordinates'], mock_coordinates)

  def test_get_coordinates_from_address_missing_g_key(self):
    geocode.google_api_key = None
    with self.assertRaises(Exception) as e:
      _get_coordinates_from_address('Some street 123')

    err = e.exception
    self.assertEqual(str(err), "Please provide a valid Google API token")


  @patch('geocode.googlemaps.Client')
  def test_get_coordinates_from_address(self, mock_client):
    geocode.google_api_key = 'Some Key'

    mocked_geocode = MagicMock(return_value=[
      {
        'geometry': {
          'location': {
            'lat': 123,
            'lng': 456
          }
        }
      }
    ])
    mock_client.return_value = MagicMock(
      geocode=mocked_geocode
    )

    location = _get_coordinates_from_address('Some Street 123')

    mock_client.assert_called_once_with(key='Some Key')
    mocked_geocode.assert_called_once_with('Some Street 123, San Francisco, CA')
    self.assertDictEqual(location, {
      'lat': 123,
      'lng': 456
    })
