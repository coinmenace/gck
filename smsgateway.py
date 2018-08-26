import requests
import json
import base64


class SMSGateway:
    def __init__(self, url, username, password):
        self.username = username
        self.password = password
        self.url = url
        auth = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        self.header = {"Content-Type": "application/json", "Authorization": "Basic " + auth}
        self.client = requests.Session()

    def sendMessage(self, method, endpoint, params):
        url = self.url + "/" + endpoint
        data = json.dumps(params)
        response = self.client.post(url, json=params, headers=self.header)
        print response.text

    def downloadLogs(self, endpoint):
        url = self.url + "/" + endpoint + "?limit=1000"
        response = self.client.get(url, headers=self.header)
        print response.text
        with open("smslog.txt", "wb+") as f:
            f.write(response.text)


class SMSGateway2:
    def __init__(self, url, username, password):
        self.username = username
        self.password = password
        self.url = url
        self.client = requests.Session()

    def sendMessage(self, method, endpoint, params):
        if method == "POST":
            data = {}
            for p in params:
                data[p] = params[p]

            url = self.url + "/" + endpoint
            response = self.client.post(url, data=data)
            print response.text
        else:
            url = self.url + "/" + endpoint
            i = 0
            for p in params:
                if i <= 0:
                    url = url + "?" + p + "=" + params[p]
                else:
                    url = url + "&" + p + "=" + params[p]
                i = i + 1
            response = self.client.get(url)
            print response.text


if __name__ == "__main__":
    # url="http://www.estoresms.com"
    # username="biddyweb"
    # password="googleboy234"
    # endpoint = "smsapi.php"
    username = "lp_app"
    password = "Legalp1234"
    url = "https://api.infobip.com/"
    endpoint = "sms/1/text/single"
    s = SMSGateway(url, username, password)
    method = "GET"
    params = {}
    # params['username']=username
    # params['password']=password
    # params['sender']="Legalpedia"
    # params['recipient']="2348135357510"
    # params['message']="Welcome to legalpedia online. Your validation token is: 234567"
    params['from'] = "Ridit"
    params['to'] = "2348135357510"
    params['text'] = "Welcome to legalpedia online. Your validation token is: 234567"
    s.sendMessage(method, endpoint, params)
    # endpoint="sms/1/logs"
    # s.downloadLogs(endpoint)
