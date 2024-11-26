import json
import requests
from bs4 import BeautifulSoup

def lambda_handler(event, context):
    # IMDb Top Movies Chart URL
    url = "https://www.imdb.com/chart/top/?ref_=nv_mv_25"

    # Set up custom headers to simulate a real browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    # Cookies to handle session
    cookies = {
        'session-id': '135-5936358-0331466',
        'session-id-time': '2082787201l',
        'session-token': 'DFSdNlZBQc2rfi/iwIV7S5SUe9PeaSZ2OZGAdlURdBjbmHiYeedpsw2O9OYdLWtPBd4eQfV1Y+eWH4C3eTZ/jODW5IesP5AZt9bQM4Ki1d2jlWcvmlWGhlnUGbPBNv4Rs5Fa7A9op1YvHRfq6WBsiJnbmn7Dx4eVym024E3G2fh7cUcjMxTAJn6BXl8/gKhAhnuD+r1oVvYGfIn3etqMQABUxWGX9wQGTamAd1zcwAIb+H/h7j26KEtGMftCGn0CCI2+xakU29L6Mo7hsGQ5sN+4zON3T2VHKQqkfcmcaKdpZS1fUOoPuRnrifkAjDryoVmgaCuZqT6WZVz1n3fap3I7Jm2AhrHe',
    }

    # Make the GET request to the IMDb Top Movies chart page
    response = requests.get(url, headers=headers, cookies=cookies)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the script tag with type="application/ld+json"
        ld_json_script = soup.find('script', type='application/ld+json')

        if ld_json_script:
            # Parse the JSON-LD data from the script tag
            ld_json_data = json.loads(ld_json_script.string)

            # Limit the itemListElement to the first 30 movies
            limited_data = ld_json_data
            limited_data['itemListElement'] = ld_json_data['itemListElement'][:30]

            # Create a list to store only the required details for each movie
            movies_details = []

            for item in limited_data['itemListElement']:
                movie = item['item']
                movie_details = {
                    "url": movie.get("url"),
                    "name": movie.get("name"),
                    "description": movie.get("description"),
                    "image": movie.get("image"),
                    "aggregateRating": movie.get("aggregateRating"),
                    "contentRating": movie.get("contentRating"),
                    "genre": movie.get("genre"),
                    "duration": movie.get("duration")
                }
                movies_details.append(movie_details)

            # Return the movie details as a JSON response
            return {
                'statusCode': 200,
                'body': json.dumps(movies_details),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }

        else:
            return {
                'statusCode': 404,
                'body': json.dumps({"error": "No 'application/ld+json' script tag found."}),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": "Failed to retrieve data from IMDb."}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
