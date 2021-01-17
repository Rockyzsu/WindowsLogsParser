import requests
import json

class IP:
    def __init__(self, ip_str):
        self.url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query={}&co=&resource_id=5809&t=1610896529549&ie=utf8&oe=gbk&cb=op_aladdin_callback&format=json&tn=baidu&cb=jQuery110207596353232994173_1610879604049&_=1610879604079'.format(
            ip_str)

        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "sp0.baidu.com",
            "Pragma": "no-cache",
            "Referer": "https://www.baidu.com/s?wd=ip&rsv_spt=1&rsv_iqid=0x9d633ff00019fa82&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=1&rsv_dl=tb&rsv_btype=t&inputT=1861&rsv_t=e6f4iNi5qleNhIdFSutFXZYfxJYVCMS0cM1pCkOpMucGghy3QPZ5TZ6MLe1hUt3Na3Bs&oq=xml%2520python%25E8%25A7%25A3%25E6%259E%2590&rsv_pq=a69a86110050bdb0&rsv_sug3=16&rsv_sug1=10&rsv_sug7=100&rsv_sug2=0&rsv_sug4=3352",
            "Sec-Fetch-Dest": "script",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
        }

    def get(self):
        try:
            r = requests.get(self.url, headers=self.headers)
        except Exception as e:
            print(e)
            return None

        else:
            return r.text

    @property
    def ip_address(self):
        html = self.get()
        if html is None:
            return '查询失败'

        data = html[html.find('(')+1:html.rfind(')')]
        js_data = json.loads(data,encoding='utf8')
        # print(js_data)
        if len(js_data['data'])>0:
            return js_data['data'][0]['location']

        return None

        

