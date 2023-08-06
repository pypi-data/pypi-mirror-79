import copy
from urllib import parse
import requests
import httpx
from mf88_affilitest import endpoints


API_RESP_ERROR = "API response error. Status code {} "


class AffiliTest(object):
    def __init__(self, api_key=None):
        self.api_key = api_key

    def login(self, email, password):
        return self._post(endpoints.LOGIN, {"email": email, "password": password})

    def logout(self):
        return self._get(endpoints.LOGOUT)

    def app_info(self, url=None, package=None, country=None):
        if url is None and package is None:
            raise APIException(
                "No parameters were passed to appInfo", endpoints.APPINFO
            )
        if url is not None and package is not None:
            raise APIException("Only one parameter should be passed", endpoints.APPINFO)
        if url is not None:
            return self._app_info_fetch(url, "url")
        return self._app_info_fetch(package, "package", country)

    def _app_info_fetch(self, data, reqType, country=None):
        payload = {}
        payload[reqType] = data
        if country:
            payload["country"] = country
        return self._get(endpoints.APPINFO, payload)["data"]

    def test(self, url, country, device, meta=False):
        body = {
            "inputType": "urlInput",
            "mainInput": url,
            "device": device,
            "country": country,
        }
        
        data = self._post(endpoints.TEST, body)
        if meta:
            return data
        return data["data"]

    async def async_multi_test(self, jobs, credentials: tuple, meta=False):
        async with httpx.AsyncClient(timeout=None) as client:
            login_data = {"email": credentials[0], "password": credentials[1]}
            await client.post(endpoints.LOGIN, data=login_data)
            print("success login")
            result = []
            for job in jobs:
                url, device, country = job["url"], job["device"], job["country"]
                body = {
                    "inputType": "urlInput",
                    "mainInput": url,
                    "device": device,
                    "country": country,
                }
                try:
                    resp = await client.post(
                        endpoints.TEST,
                        data=body,
                        headers=self._auth_headers(),
                    )
                    data = resp.json()
                    if data["error"]:
                        print("Response Error: %s > %s", url, data["error"])
                        continue
                    result.append(data["data"] if not meta else data)
                except Exception as err:
                    print(f"Error: {url} > {err}")
                    continue
            return result

    def compare_to_preview(self, url, preview_url, country, device, meta=False):
        data = self._post(
            endpoints.COMPARE,
            {
                "url": url,
                "previewURL": preview_url,
                "country": country,
                "device": device,
            },
        )
        if meta:
            return data
        return data["data"]

    def calls_left(self):
        return self._get(endpoints.CALLS_LEFT)["data"]

    def clone(self):
        api_clone = copy.deepcopy(self)
        api_clone._request_session = requests.Session()
        api_clone._request_session.cookies = self._request_session.cookies
        return api_clone

    def _post(self, endpoint, payload):
        self._last_response = self.requests_session().post(
            endpoint, data=payload, headers=self._auth_headers()
        )
        try:
            res_data = self._last_response.json()
        except Exception as e:
            raise APIException(
                API_RESP_ERROR.format(self._last_response.status_code), endpoint
            )
        if res_data["error"]:
            raise APIException(res_data["error"], endpoint)
        return res_data

    def _get(self, endpoint, payload=None):
        url = endpoint
        if payload is not None:
            url = endpoint + "?" + parse.urlencode(payload)
        self._last_response = self.requests_session().get(
            url, headers=self._auth_headers()
        )
        res_data = self._last_response.json()
        if res_data["error"]:
            raise APIException(res_data["error"], endpoint)
        return res_data

    def _auth_headers(self):
        if self.api_key:
            return {"Authorization": "AT-API " + self.api_key}
        return {}

    def last_response(self):
        return self._last_response

    def requests_session(self):
        if hasattr(self, "_request_session"):
            return self._request_session
        self._request_session = requests.Session()
        return self._request_session


class APIException(Exception):
    def __init__(self, error, endpoint):
        super(APIException, self).__init__(error, endpoint)
        self.endpoint = endpoint
