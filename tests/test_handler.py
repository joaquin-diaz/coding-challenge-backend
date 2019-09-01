import unittest
import os

from unittest.mock import patch, MagicMock

from handler import handler, get_qs, validate_limit

def mock_append_coordinates(locations):
  for location in locations:
    location['coordinate'] = {'lat': 123, 'lng': 456}

class TestHandler(unittest.TestCase):
  def setUp(self):
    os.environ["SF_LOCATIONS_API_KEY"] = "Test Key"

  def test_get_qs(self):
    mock_event = {
      'queryStringParameters': {
        'query': 'venom',
        'limit': 50,
        'include_coordinates': 'true'
      }
    }

    query, limit, include_coordinates = get_qs(mock_event)

    self.assertEqual(query, 'venom')
    self.assertEqual(limit, 50)
    self.assertEqual(include_coordinates, 'true')

  def test_get_qs_incomplete(self):
    mock_event = {
      'queryStringParameters': {
        'query': 'venom',
        'limit': 50,
      }
    }

    query, limit, include_coordinates = get_qs(mock_event)

    self.assertEqual(query, 'venom')
    self.assertEqual(limit, 50)
    self.assertIsNone(include_coordinates)

  def test_validate_qs_no_integer(self):
    with self.assertRaises(Exception) as e:
      validate_limit("ten", "true")

    err = e.exception
    self.assertEqual(str(err), "Please provide an integer value in the limit parameter")

  def test_validate_qs_above_limit(self):
    with self.assertRaises(Exception) as e:
      validate_limit("50", "true")

    err = e.exception
    self.assertEqual(str(err), "Please provide a limit between 0 and 10 when including locations")

  def test_validate_qs_above_limit_no_coordinates(self):
    self.assertIsNone(validate_limit("50", "false"))

  @patch('handler.append_coordinates_to_locations', mock_append_coordinates)
  @patch('handler.FilmLocationsAPI.fetch_film_locations')
  def test_fetch_locations_and_coordinates(self, mock_fetch_films):
    mock_fetch_films.return_value = [
      {
        'locations': 'Some Street 123'
      }
    ]
    mock_event = {
      'queryStringParameters': {
        'query': "venom",
        'limit': "5",
        'include_coordinates': "true"
      }
    }

    response = handler(mock_event, None)

    self.assertDictEqual(response, {
      "statusCode": 200,
      "body": '[{"locations": "Some Street 123", "coordinate": {"lat": 123, "lng": 456}}]'
    })

  @patch('handler.append_coordinates_to_locations', mock_append_coordinates)
  @patch('handler.FilmLocationsAPI.fetch_film_locations')
  def test_fetch_locations_and_coordinates_clean_locations(self, mock_fetch_films):
    mock_fetch_films.return_value = [
      {
        'locations': 'Some Street 123'
      }, {
        'not locations': 'something else'
      }
    ]
    mock_event = {
      'queryStringParameters': {
        'query': "venom",
        'limit': "5",
        'include_coordinates': "true"
      }
    }

    response = handler(mock_event, None)

    self.assertDictEqual(response, {
      "statusCode": 200,
      "body": '[{"locations": "Some Street 123", "coordinate": {"lat": 123, "lng": 456}}]'
    })

  @patch('handler.append_coordinates_to_locations')
  @patch('handler.FilmLocationsAPI.fetch_film_locations')
  def test_fetch_locations_and_coordinates_no_coordinates(self, mock_fetch_films, mock_append):
    mock_fetch_films.return_value = [
      {
        'locations': 'Some Street 123'
      }
    ]
    mock_event = {
      'queryStringParameters': {
        'query': "venom",
        'limit': "5",
        'include_coordinates': "false"
      }
    }

    response = handler(mock_event, None)

    mock_append.assert_not_called()
    self.assertDictEqual(response, {
      "statusCode": 200,
      "body": '[{"locations": "Some Street 123"}]'
    })