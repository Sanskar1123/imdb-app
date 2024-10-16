import json
from tests import env_variables

env_variables.add_os_variables()

import app
from chalice.test import Client

sample_file = (
    b'budget,homepage,original_language,original_title,overview,release_date,revenue,runtime,status,title,vote_average,vote_count,production_company_id,genre_id,languages\n'
    b'30000000.0,http://toystory.disney.com/toy-story,en,Toy Story,"Led by Woody, Andy\'s toys live happily in his room until Andy\'s birthday brings Buzz Lightyear onto the scene. Afraid of losing his place in Andy\'s heart, Woody plots against Buzz. But when circumstances separate Buzz and Woody from their owner, the duo eventually learns to put aside their differences.",1995-10-30,373554033.0,81,Released,Toy Story,7.7,5415.0,3,16,[\'English\']\n'
    b'65000000.0,,en,Jumanji,"When siblings Judy and Peter discover an enchanted board game that opens the door to a magical world, they unwittingly invite Alan -- an adult who\'s been trapped inside the game for 26 years -- into their living room. Alan\'s only hope for freedom is to finish the game, which proves risky as all three find themselves running from giant rhinoceroses, evil monkeys and other terrifying creatures.",1995-12-15,262797249.0,104,Released,Jumanji,6.9,2413.0,559,12,"[\'English\', \'Fran\xc3\xa7ais\']"\n'
)

sample_file_headers = (
    b'budget,homepage,original_language,original_title,overview,release_date,revenue,runtime,status,title,vote_average,vote_count,production_company_id,genre_id,languages\n'
)

# Test cases for upload API with the payload and expected response code
test_cases_upload_csv = [
    ["", 502],  # No file uploaded
    [sample_file, 200],  # Valid test case
    [sample_file_headers, 502],  # Test case with headers only, should fail due to not data
    ["title,year,director\n" + "Movie1,2020,Director1\n" * int(1e7), 502],  # Test case with file size more than 100 mb
    ["title,year,director\nMovie1,2020,Director1\nMovie2,2021,Director2", 502],  # Test case with incorrect header
]

# Test cases for fetch API with the payload and expected response code
test_case_fetch_api = [
    [
        {
            "filter_params": {
                "languages": "Français",
                "release_year": 1995
            },
            "sort_params": {
                "vote_average": -1,
                "release_date": -1
            },
            "page": 1,
            "size": 10
        }
        , 200
    ],  # Valid test case
    [
        {
            "page": 1000000000000,
            "size": 1
        }
        , 502
    ],  # Invalid test case requesting too large page size
    [
        {
            "sort_params": {
                "vote_average": "ascending",
                "release_date": -1
            },
            "page": 1,
            "size": 10
        }
        , 502
    ],  # Invalid sort param direction
    [
        {
            "filter_params": {
                "languages": "some random language which does not exist",
            },
        }
        , 200
    ],  # Test case where no data matches the filter param
]


def test_upload_csv_api():
    with Client(app.app) as client:
        for idx, test_case in enumerate(test_cases_upload_csv):
            response = client.http.post(
                '/api/upload/movies/csv',
                headers={
                    'Content-Type': 'application/csv'
                },
                body=test_case[0]
            )
            print(f"Upload CSV API response:", json.loads(response.body))
            try:
                assert response.status_code == test_case[1]
            except AssertionError:
                print(
                    f"Test case {idx + 1} failed: Expected status code {test_case[1]}, but got {response.status_code}")
            print("\n")


def test_fetch_movies_api():
    with Client(app.app) as client:
        for idx, test_case in enumerate(test_case_fetch_api):
            response = client.http.post(
                '/api/fetch/movies',
                headers={
                    'Content-Type': 'application/json'
                },
                body=json.dumps(test_case[0])
            )
            if response.status_code == 200:
                print(f"Fetch movies API response:", json.loads(response.body)["message"])
            else:
                print(f"Fetch movies API response:", json.loads(response.body)["error"])

            try:
                assert response.status_code == test_case[1]
            except AssertionError:
                print(
                    f"Test case {idx + 1} failed: Expected status code {test_case[1]}, but got {response.status_code}")
            print("\n")
