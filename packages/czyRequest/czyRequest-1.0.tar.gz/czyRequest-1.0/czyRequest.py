'''
@File       : czyRequest.py
@Copyright  : rainbol
@Date       : 2020/9/8
@Desc       :
'''

import json
import requests




class CzyRequest(object):  # requests封装类
    time_out = 10  # 请求超时时间

    class CheckJsonIsStr(object):
        '''校验json中是否有非字符串的字段,除{}[] ''之外'''

        def __init__(self):
            self.key_list = []
            self.value_list = []

        def get_dict_all_keys(self, dict_a):
            """
            多维/嵌套字典数据无限遍历，获取json返回结果的所有key值集合,或者所有value值的集合
            :param dict_a:
            :return: key_list
            """
            if isinstance(dict_a, dict):  # 使用isinstance检测数据类型
                for x in range(len(dict_a)):
                    temp_key = list(dict_a.keys())[x]
                    temp_value = dict_a[temp_key]
                    self.key_list.append(temp_key)
                    self.value_list.append(temp_value)
                    self.get_dict_all_keys(temp_value)  # 自我调用实现无限遍历
            elif isinstance(dict_a, list):
                for k in dict_a:
                    if isinstance(k, dict):
                        for x in range(len(k)):
                            temp_key = list(k.keys())[x]
                            temp_value = k[temp_key]
                            self.key_list.append(temp_key)
                            self.value_list.append(temp_value)
                            self.get_dict_all_keys(temp_value)
            return self.value_list

        def deal(self) -> bool:
            '''value值存在一些缺陷,所以进行二次处理,
            return :True 存在不合法的值 '''
            for value in self.value_list:
                if type(value).__name__ == 'str':
                    continue
                elif type(value).__name__ == 'dict':
                    continue
                else:
                    if type(value).__name__ == 'list':
                        continue
                    return True

    def __init__(self, url, data=None, headers=None, file=None, wc=None):

        self.localhost = 'http://127.0.0.1'
        self.port = 8000
        self.url = url
        self.data = data
        self.headers = headers
        self.file = file
        self.wc = wc  # 默认为None,不校验非字符串字段

    def return_msg_to_json(self, *args):
        '''外层嵌套了一层,根据校验结果来判断'''
        return dict(
            status=args[0],
            data=args[1],
        )


    def post(self):
        try:
            self.data = json.dumps(self.data)
            req = requests.post(self.url, data=self.data, headers=self.headers,
                                files=self.file, timeout=self.time_out)
            req.encoding = req.apparent_encoding  # 将信息体的信息修改成content,也就是r.content.decode()
        except Exception as e:
            res = self.return_msg_to_json('0', e.args)  # 0代表请求失败
        else:
            try:
                res = self.return_msg_to_json('1', req.json())  # 1代表返回的json
            except Exception as e:
                res = self.return_msg_to_json('2', req.text)  # 2代表返回不是json
            else:
                try:
                    data = req.json()
                except Exception as e:
                    return req.text
                if not self.wc:
                    sjson = self.CheckJsonIsStr()
                    sjson.get_dict_all_keys(data['result'])
                    if sjson.deal():
                        res = self.return_msg_to_json('3', req.json())  # 3代表返回中有非字符串的字段,除{}[] ''之外
        return res

    def get(self):
        try:
            self.data = json.dumps(self.data)
            req = requests.get(self.url, params=self.data, headers=self.headers, timeout=self.time_out)
            req.encoding = req.apparent_encoding  # 将信息体的信息修改成content,也就是r.content.decode()
        except Exception as e:

            res = self.return_msg_to_json('0', e.args)  # 0代表请求失败
        else:
            try:
                res = self.return_msg_to_json('1', req.json())  # 1代表返回的json
            except Exception as e:
                res = self.return_msg_to_json('2', req.text)  # 2代表返回不是json
            else:
                try:
                    data = req.json()
                except Exception as e:
                    return req.text
                if not self.wc:
                    sjson = self.CheckJsonIsStr()
                    sjson.get_dict_all_keys(data['result'])
                    if sjson.deal():
                        res = self.return_msg_to_json('3', req.json())  # 3代表返回中有非字符串的字段,除{}[] ''之外
        return res

    def put(self):
        try:
            self.data = json.dumps(self.data)
            req = requests.put(self.url, params=self.data, headers=self.headers, timeout=self.time_out)
            req.encoding = req.apparent_encoding  # 将信息体的信息修改成content,也就是r.content.decode()
        except Exception as e:
            res = self.return_msg_to_json('0', e.args)  # 0代表请求失败
        else:
            try:
                res = self.return_msg_to_json('1', req.json())  # 1代表返回的json
            except Exception as e:
                res = self.return_msg_to_json('2', req.text)  # 2代表返回不是json
            else:
                try:
                    data = req.json()
                except Exception as e:
                    return req.text
                if not self.wc:
                    sjson = self.CheckJsonIsStr()
                    sjson.get_dict_all_keys(data['result'])

                    if sjson.deal():
                        res = self.return_msg_to_json('3', req.json())
        return res

    def delete(self):
        try:
            self.data = json.dumps(self.data)
            req = requests.delete(self.url, params=self.data, headers=self.headers, timeout=self.time_out)
            req.encoding = req.apparent_encoding  # 将信息体的信息修改成content,也就是r.content.decode()
        except Exception as e:
            res = self.return_msg_to_json('0', e.args)  # 0代表请求失败
        else:
            try:
                res = self.return_msg_to_json('1', req.json())  # 1代表返回的json
            except Exception as e:
                res = self.return_msg_to_json('2', req.text)  # 2代表返回不是json
            else:
                try:
                    data = req.json()
                except Exception as e:
                    return req.text
                if not self.wc:
                    sjson = self.CheckJsonIsStr()
                    sjson.get_dict_all_keys(data['result'])
                    if sjson.deal():
                        res = self.return_msg_to_json('3', req.json())
        return res
