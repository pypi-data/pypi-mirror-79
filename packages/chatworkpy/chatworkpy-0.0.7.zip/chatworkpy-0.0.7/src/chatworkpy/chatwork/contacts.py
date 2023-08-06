from chatworkpy.chatwork.chatwork import Chatwork
import requests

class Contacts(Chatwork):
    def __init__(self, api_token, to_id_list: list):
        self.to_id_list = to_id_list
        super().__init__(api_token)

    # To のIdに紐づく名前を取得する
    def make_tos_dict(self):
        accounts_dict = {}
        response_get_contact_name = self._get_contact_name()
        if response_get_contact_name.status_code == 200:
            content = response_get_contact_name.content
            print(content)
        for to_id in self.to_id_list:
            item = (to_id, "name" + to_id)
            accounts_dict.update([item])
        return accounts_dict
    
    def _get_contact_name(self):
        get_url = f'{self.base_url}/contacts'

        headers = {'X-ChatWorkToken': self.api_token}
        return requests.get(get_url, headers=headers)
