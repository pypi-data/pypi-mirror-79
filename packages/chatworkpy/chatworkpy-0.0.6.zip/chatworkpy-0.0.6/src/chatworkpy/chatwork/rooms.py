from chatworkpy.chatwork.chatwork import Chatwork
from chatworkpy.chatwork.contacts import Contacts
import os
import requests
import calendar
import datetime

class Rooms(Chatwork):
    
    def __init__(self, api_token: str, room_id):
        self.room_id = room_id
        super().__init__(api_token)

    # private method
    # make prefix_message_for_to_id_list
    """
    # To: Hogehoge さん
    # To: Fugafuga さん
    """
    def _make_prefix_message_for_to_id_list(self, tos_dict: dict, to_all: bool=False):
        prefix = ''
        if to_all:
            prefix += f"[toall]{os.linesep}"
        else:
            for to in tos_dict:
                prefix += f"[To:{to['account_id']}] {to['name']} さん{os.linesep}"

        return prefix
    
    def _get_rooms(self):
        return self.exec_request("get", "rooms")

    def _get_rooms_members(self, room_id):
        try:
            return self.exec_request("get", f"rooms/{room_id}/members")
        except Exception as e:
            print(e)
            return None

    # To のIdに紐づく名前を取得する
    def _make_tos_dict(self, to_id_list:list):
        
        tos_dict = []
        response_get_rooms = self._get_rooms()
        for room in response_get_rooms:
            response_get_rooms_members = self._get_rooms_members(room["room_id"])
            if response_get_rooms_members != None:
                for member in response_get_rooms_members:
                    for to_id in to_id_list:
                        if to_id == member['account_id']:
                            item = {"account_id" : to_id, "name" : member["name"]}
                            if tos_dict.count(item) == 0:
                                tos_dict.append(item)
        return tos_dict
        
    def send_message(self, message: str, to_id_list: list, to_all: bool=False):
        tos_dict = self._make_tos_dict(to_id_list)

        prefix_message = self._make_prefix_message_for_to_id_list(tos_dict, to_all)
        request_params = {'body': prefix_message + message}        
        return self.exec_request("post", f"rooms/{self.room_id}/messages", request_params=request_params)

    def send_task(self, task_body: str, to_id_list:list, limit:datetime.datetime=None):
        if limit:
            utctimetuple = limit.utctimetuple()
            limit_datetime = calendar.timegm(utctimetuple)
            to_id_list_str = [str(n) for n in to_id_list]
            to_ids = ",".join(to_id_list_str)
            request_params = {'body': task_body, "to_ids": to_ids, "limit": limit_datetime}
        else:
            request_params = {'body': task_body, "to_ids": ",".join(to_id_list)}
            
        return self.exec_request("post", f"rooms/{self.room_id}/tasks", request_params=request_params)