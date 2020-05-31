import requests
import json


def send_single_sms(apikey, code, mobile):
    """
    发送单条短信
    :param apikey: 用户唯一标识
    :param code: 验证码
    :param mobile: 接收短信的手机号码
    :return:
    """
    url = 'https://sms.yunpian.com/v2/sms/single_send.json'
    text = f'【XXXX】您的验证码是{code}。如非本人操作，请忽略本短信'
    
    response = requests.post(url=url, data={'apikey': apikey, 'mobile': mobile, 'text': text})
    return json.loads(response.text)
