class FiddlerUtil():
    def __init__(self, raw_text, save_Path):
        """ Fiddler to python requsts
        :param raw_text:  raw文本
        :param save_Path:  输出文件地址
        """
        self.save_Path = save_Path
        self.text = raw_text
        self.url_list = []
        self.headers = {}
        self.cookies = {}
        self.data = {}

    def get_url(self):
        infos = self.text.split("\n")[0]
        self.url_list = [infos.split(" ")[0], infos.split(" ")[1]]

    def get_headers(self):
        """
        获取请求头
        :return:
        """
        infos = self.text.split("\n")[1:]
        for info in infos:
            if "Cookie: " in info:
                break
            infoItems = info.split(":")
            self.headers[infoItems[0].strip()] = infoItems[1].strip()

    def get_cookies(self):
        infos = self.text.split("\n")[1:]
        cookies_flag = 0
        for i in infos:
            if "Cookie: " in i:
                self.cookies = i.replace("Cookie: ", "")
                print(self.cookies)
                cookies_flag = 1
                break
        if cookies_flag == 1:
            self.cookies = {i.split("=")[0]: i.split("=")[1] for i in self.cookies.split("; ")}

    def get_data(self):
        """
        获取请求参数
        :return:
        """
        import json
        dataStr = ""
        try:
            infos = self.text.split("\n")
            for i in range(len(infos)):
                if "Cookie: " in infos[i]:
                    if (i + 1 != len(infos)):

                        dataStr = "".join(infos[i + 1:])
                        break

            if (dataStr != ""):
                if ("&" in self.data):
                    self.data = {i.split("=")[0]: i.split("=")[1] for i in self.data.split("&")}
                else:
                    self.data = json.loads(dataStr)
        except:
            pass

    def get_req(self):
        """
        输出请求信息到文件
        :return:
        """
        info_beg = """#!/usr/bin/python\n# -*- coding: UTF-8 -*-\nimport requests\nimport urllib3\nurllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)\n\n"""
        info_url = "url = \'{}\'\n".format(self.url_list[1])
        info_headers = "headers = {}\n".format(self.headers)
        info_cookies = "cookies = {}\n".format(self.cookies)
        info_data = "data = {}\n\n".format(self.data)
        if "GET" in self.url_list[0]:
            info_req = "response = requests.get(url, headers=headers, verify=False, cookies=cookies)\n"
        else:
            info_req = "response = requests.post(url, headers=headers, verify=False, cookies=cookies, data=data)\n"
        info_end = "print(response.status_code)\nprint(response.text)\n"
        text = info_beg + info_url + info_headers + info_cookies + info_data + info_req + info_end

        with open(self.save_Path, "w+", encoding="utf8") as p:
            p.write(text)
        print("转化成功！！")
        print(self.save_Path, "文件保存!")

    def start(self):
        """
        开始转化
        :return:
        """
        self.get_url()
        self.get_headers()
        self.get_cookies()
        self.get_data()
        print("self.url_list:", self.url_list)
        print("self.headers:", self.headers)
        print("self.cookies:", self.cookies)
        print("self.data:", self.data)
        self.get_req()


# simple demo
# raw_text = """GET https://www.baidu.com/s?ie=utf-8&mod=1&isbd=1&isid=bca2f86a000aa2c9&ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=fiidler%E8%BD%AC%E5%8C%96%E4%B8%BApython%20requests%E4%BB%A3%E7%A0%81&oq=fiddler%25E8%25BD%25AC%25E5%258C%2596%25E4%25B8%25BApython%2520requests%25E4%25BB%25A3%25E7%25A0%2581&rsv_pq=bca2f86a000aa2c9&rsv_t=573d%2BTpKT4yN28kPGOMd6B94HduXSz1aFHU1h7vCZS3TTrwGrQj3GTtM1i8&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_btype=t&bs=fiddler%E8%BD%AC%E5%8C%96%E4%B8%BApython%20requests%E4%BB%A3%E7%A0%81&rsv_sid=undefined&_ss=1&clist=&hsug=&f4s=1&csor=7&_cr1=39546 HTTP/1.1
# Host: www.baidu.com
# Connection: keep-alive
# Accept: */*
# is_xhr: 1
# X-Requested-With: XMLHttpRequest
# is_referer: https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=fiddler%E8%BD%AC%E5%8C%96%E4%B8%BApython%20requests%E4%BB%A3%E7%A0%81&oq=fiidler%25E6%258F%2592%25E4%25BB%25B6%25E5%25BC%2580%25E5%258F%2591%2520%25E8%25BD%25AC%25E5%258C%2596%25E4%25B8%25BApython%2520requests%25E4%25BB%25A3%25E7%25A0%2581&rsv_pq=b515f95400033294&rsv_t=8d7dr4sDJ1d9BK%2Bak1%2BCLVQAyXClhauK6ouL%2FYpRN1Au%2FoDHW54XbqEyuXQ&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_btype=t&inputT=332&rsv_sug3=101&rsv_sug2=0&rsv_sug4=1296&bs=fiidler%E6%8F%92%E4%BB%B6%E5%BC%80%E5%8F%91%20%E8%BD%AC%E5%8C%96%E4%B8%BApython%20requests%E4%BB%A3%E7%A0%81
# User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36
# is_pbs: fiddler%E8%BD%AC%E5%8C%96%E4%B8%BApython%20requests%E4%BB%A3%E7%A0%81
# Sec-Fetch-Site: same-origin
# Sec-Fetch-Mode: cors
# Sec-Fetch-Dest: empty
# Referer: https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=fiidler%E8%BD%AC%E5%8C%96%E4%B8%BApython%20requests%E4%BB%A3%E7%A0%81&oq=fiddler%25E8%25BD%25AC%25E5%258C%2596%25E4%25B8%25BApython%2520requests%25E4%25BB%25A3%25E7%25A0%2581&rsv_pq=bca2f86a000aa2c9&rsv_t=573d%2BTpKT4yN28kPGOMd6B94HduXSz1aFHU1h7vCZS3TTrwGrQj3GTtM1i8&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_btype=t
# Accept-Encoding: gzip, deflate, br
# Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
# Cookie: MSA_WH=1920_977; BIDUPSID=6D2CD0E5856AF7522B3471E097A62069; PSTM=1599120383; sug=3; sugstore=0; ORIGIN=0; bdime=0; BAIDUID=0422DA96AF043F3D6FA43E535592926C:SL=0:NR=10:FG=1; H_WISE_SIDS=154599_154770_155062_155554_152348_150968_152056_150075_147087_151187_150084_148867_154606_153629_150043_153439_154797_151532_151017_127969_154413_154174_153571_155329_152902_152981_154015_146732_154603_155424_131423_155486_154037_151147_155599_154189_151219_140367_154799_144966_154911_154440_155532_154212_155663_154801_154902_155237_153951_154148_147547_153203_148869_153690_153805_154309_110085; BDUSS=2dEdnBKalpLNWdCNWRZU2ZSeDdWalR5MGdlUXY5UFpUflJNNTRqbnFUcTEwWDVmSVFBQUFBJCQAAAAAAAAAAAEAAAAeP8VUz8TCrLCyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALVEV1-1RFdfc; BDUSS_BFESS=2dEdnBKalpLNWdCNWRZU2ZSeDdWalR5MGdlUXY5UFpUflJNNTRqbnFUcTEwWDVmSVFBQUFBJCQAAAAAAAAAAAEAAAAeP8VUz8TCrLCyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALVEV1-1RFdfc; BDSFRCVID=gttOJeC62R13FwTrSnZXbapttTNUI8QTH6aoYOeh_Xq7CLVTAaElEG0PHf8g0KubhaS4ogKK3gOTH4DF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=Jbkj_DIXtDvbfP0k5-o55-FHqxbXq-b9LgOZ0l8Ktt3dVD3ShR5oyj-e-xQj-n3E3m7joR7mWIQHDn7vDnOhXtkQyPrk0-bT-IT4KKJxWPPWeIJo5DcY3p0RhUJiB5JMBan7_pbIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbCD6ejt2j6o-eUbQa4JWHD6QB4TaajrjDnCryq7NXUI8LNDHtt7CB6nHQJ782KjDHtJm5h_KWtLIhRO7ttoyabvQKT6RBRrFJROhh-b-jML1Db3-W6vMtg3C3fQYtj6oepvoDPJc3Mv3Q-jdJJQOBKQB0KnGbUQkeq8CQft20b0EeMtjW6LEtR-tVCtatCI3HnRv5t8_5-LH-UoX-I62aKDsLpbaBhcqEIL4hqJHhl0pKRbTe4baK6RJLn39yDL5MUbSj4QoWhFkeMc-tbcfygvqbPbo-p5nhMJN257JDMP0-xPfa5Oy523iob3vQpPMshQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0xXj_0Djb-Datttjn2aIOt0Tr25RrjeJrmq4bohjPU04v9BtQO-DOxobA2BfjKVUJb5P5HKb03bPRi-qKeQgnk2p5dL-cDbD-lbnjCyqKNWGo30x-jLTny3l3ebxAVDPP9QtnJyUnQbPnnBT5i3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRu_CF-JIDWhI-GDjRs5tP8eaAX5-RLfKvJLp7F5l8-hx_lDUjb3bD9hR6v5tojbTnn2f5YfUjxOKQphprcbtkmWhLf3M7pQg6KKRRN3KJmObL9bT3v5tDJ-J-J2-biWb7M2MbdJpbP_IoG2Mn8M4bb3qOpBtQmJeTxoUJ25DnJhhCGe4bK-Tr0DG-8JxK; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; yjs_js_security_passport=35f103261fe63ec36d2a987cbbb04433688a881d_1600137625_js; COOKIE_SESSION=141_0_9_5_13_1_0_0_9_1_1_0_4609_0_0_0_1600080001_0_1600137761%7C9%231941_27_1599820234%7C9; delPer=0; BD_CK_SAM=1; PSINO=6; H_PS_PSSID=7540_32606_1421_7567_31254_7580_7606_31709_32583; BDSVRTM=0; WWW_ST=1600153715699; BD_UPN=12314353
# """
# simple = fiddler_Util(raw_text=raw_text,save_Path="./demo.py")
# simple.start()