import requests

class Chatwork:
    def __init__(self, api_token):
        self.base_url = 'https://api.chatwork.com/v2'
        self.api_token = api_token

    def exec_request(self, method, url, url_params={}, query_params={}, request_params={}):
        """
        - Method: method
        - URL: url.format(**url_params)
        - Parameter: query_params & apiKey=api_key
        - Request Body(data): request_params
        """
        _url = url.format(**url_params).lstrip("/")
        _endpoint = f"{self.base_url}/{_url}"   #self.endpoint.format(path=_url)
        _headers = {'X-ChatWorkToken': self.api_token}

        #request_params = BacklogClient.remove_mb4(request_params)

        resp = None

        method = method.lower().strip()
        if method == "get":
            resp = requests.get(_endpoint, params=query_params, headers=_headers)
        elif method == "patch":
            resp = requests.patch(
                _endpoint, params=query_params, data=request_params, headers=_headers)
        elif method == "post":
            resp = requests.post(
                _endpoint, params=query_params, data=request_params, headers=_headers)
        elif method == "delete":
            resp = requests.delete(
                _endpoint, params=query_params, data=request_params, headers=_headers)
        else:
            raise Exception("Unsupported Method")

        if resp.status_code >= 400:
            raise Exception(resp, resp.text)

        if resp.status_code == 204:
            # 204 NO_CONTENT is blank response
            # used in star
            return None

        return resp.json()