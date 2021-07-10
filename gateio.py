import requests
import time
import hashlib
import hmac
import json


def printf(string, display=True):
    """

    :type string: string to print on the console and to save in the result.txt file
    """
    file1 = open("result.txt", "a+")
    file1.writelines(string)
    file1.close()
    if display:
        print(string)


class Gateio:
    """
    Class to interact with the Gateio API.
    """

    def __init__(self, key, secret):
        """
        create an object to interact with the Gateio interface
        :param str key:
        :param str secret:
        """
        self.host = "https://api.gateio.ws"
        self.prefix = "/api/v4"
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.key = key
        self.secret = secret

    def gen_sign(self, method, url, query_string=None, payload_string=None):
        key = self.key  # api_key
        secret = self.secret  # api_secret
        t = time.time()
        m = hashlib.sha512()
        m.update((payload_string or "").encode('utf-8'))
        hashed_payload = m.hexdigest()
        s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, t)
        sign = hmac.new(secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
        return {'KEY': key, 'Timestamp': str(t), 'SIGN': sign}

    def get_data(self,symbol):
        """
        Get 200 5m candle data
        :return: candle's data if the function has been executed correctly, return zero otherwise
        """
        url = '/futures/usdt/candlesticks'
        query_param = 'contract=' + symbol
        for i in range(1, 6):  # try 5 times with a waiting time between every tries
            try:
                r = requests.request('GET', self.host + self.prefix + url + "?" + query_param, headers=self.headers)
                return r.json()
            except Exception as e:
                printf('error during geting amount of usdt ' + str(e))
                time.sleep(5 * i)
                continue
        return 0


    def create_order(self, symbol, size):
        """
        create an order of the future market
        :param str symbol:
        :param float size: size of the order. Positive for long, negative for short, zero to close position
        :return: id of the order if the function has been executed correctly, return zero otherwise
        """
        url = '/futures/usdt/orders'
        query_param = ''
        if size == 0:
            body = '{"contract":'+symbol+',"size":0,"iceberg":0,"price":"0","close":true,"tif":"ioc","text":"t-my-custom-id"}'
        else:
            body = '{"contract":"' + symbol + '","size":' + str(
                size) + ',"iceberg":0,"price":"0","tif":"ioc","text":"t-my-custom-id"}'
        for i in range(1, 6):  # try 5 times with a waiting time between every tries
            try:
                sign_headers = self.gen_sign('POST', self.prefix + url, query_param, body)
                self.headers.update(sign_headers)
                r = requests.request('POST', self.host + self.prefix + url, headers=self.headers, data=body)
                printf(r.json())
                id = r.json()['id']
                return id
            except Exception as e:
                printf('error during creating order ' + str(e))
                time.sleep(5 * i)
                continue
        return 0

    def get_amount(self):
        """
        get available and total amount for future contract
        :return: tuple (available, total), if error return zero
        """
        url = '/futures/usdt/accounts'
        query_param = ''
        # sign headers sign with the keys
        sign_headers = self.gen_sign('GET', self.prefix + url, query_param)
        self.headers.update(sign_headers)
        for i in range(1,6):
            try:
                r = requests.request('GET', self.host + self.prefix + url, headers=self.headers)
                result = r.json()['total']
                return float(result)
            except Exception as e:
                printf('error during getting amount ' + str(e))
                time.sleep(5 * i)
                continue
        return 0

    def set_leverage(self,leverage):
        """
        :param int leverage:  leverage multiplicator
        :return: server response, if error return zero
        """
        url = '/futures/usdt/positions/BTC_USDT/leverage'
        query_param = 'leverage=' + str(leverage)
        for i in range(1,6):
            try:

                sign_headers = self.gen_sign('POST', self.prefix + url, query_param)
                self.headers.update(sign_headers)
                r = requests.request('POST', self.host + self.prefix + url + "?" + query_param, headers=self.headers)
                return r.json()
            except Exception as e:
                printf('error during geting amount of usdt ' + str(e))
                time.sleep(5 * i)
                continue
        return 0

    def set_margin(self,margin):
        """
        set a custom margin for the pair
        :param margin:
        :return: servers response, if error return zero
        """
        url = '/futures/usdt/positions/BTC_USDT/margin'
        query_param = 'change=' + str(margin)
        for i in range(1,6):
            try:

                # for `gen_sign` implementation, refer to section `Authentication` above
                sign_headers = self.gen_sign('POST', self.prefix + url, query_param)
                self.headers.update(sign_headers)
                r = requests.request('POST', self.host + self.prefix + url + "?" + query_param, headers=self.headers)
                return r.json()
            except Exception as e:
                printf('error during geting amount of usdt ' + str(e))
                time.sleep(5 * i)
                continue
        return 0

    def pair_info(self,symbol):
        """

        :param symbol:
        :return: return server response, if error return zero
        """
        for i in range(1,6):
            try:
                host = "https://api.gateio.ws"
                prefix = "/api/v4"
                headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

                url = '/futures/usdt/contracts/' + symbol
                query_param = ''
                r = requests.request('GET', host + prefix + url, headers=headers)
                return r.json()
            except Exception as e:
                printf('error during geting amount of usdt ' + str(e))
                time.sleep(5 * i)
                continue
        return 0


