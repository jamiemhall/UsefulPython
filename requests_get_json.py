import requests

from requests.exceptions import HTTPError, Timeout

REQUEST_TIMEOUT = 300


def main(url: str, payload: dict):
    with requests.Session() as session:
        try:
            response = session.get(url, params=payload, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
        except Timeout as err:
            print(f'The request timed out: {err}')
            return False
        except HTTPError as err:
            print(f'HTTP error occurred: {err}')
            return False
        except Exception as err:
            print(f'Other error occurred: {err}')
            return False

    if response.status_code == requests.codes.ok:
        result = response.json()
        print(result)
        return True
    else:
        return False


if __name__ == "__main__":
    test_url = 'https://api.github.com'
    data = {'q': 'requests+language:python'}
    main(url=test_url, payload=data)
