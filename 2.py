#!/usr/bin/env python3

import logging
import time
import argparse
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def post(emailAddress, password):
    session = requests.session()
    data = {'email_address': emailAddress,
            'password': password,
            'persistent': 'True'
            }  # login data
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'referer': 'https://inkread.com/feeds/explore/?bundles=zh'
    }
    session.headers = headers
    session.post('https://inkread.com/login/', data=data)
    logger.info(str(dict(session.cookies)))
    time.sleep(5)
    r = session.post('https://inkread.com/send_now/')
    with open('1.html', 'w')as f:
        f.write(r.text)
    return r.status_code


def delay(settingTime):
    logger.info('Waiting for the first time.')
    while settingTime != time.strftime("%H:%M", time.localtime(time.time())):
        time.sleep(55)


def loginTest(emailAddress, password):
    session = requests.session()
    data = {'email_address': emailAddress,
            'password': password,
            'persistent': 'True'
            }  # login data
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'referer': 'https://inkread.com/feeds/explore/?bundles=zh'
    }
    session.post('https://inkread.com/login/', data=data, headers=headers)
    return len(dict(session.cookies)) == 2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Automatic Script for Kindle4rss")
    parser.add_argument('-t', '--time', type=str, default='3:14', help='Set the Time to Send File, Default 3:14')
    parser.add_argument('-d', '--day', type=int, default=1, help='Days Between Sending Files, Default 1 Day')
    parser.add_argument('-u', '--user', type=str, required=True, help='User Name, Mostly E-mail Address')
    parser.add_argument('-p', '--password', type=str, required=True, help='Login Password')
    args = parser.parse_args()

    if '@' not in args.user:
        logger.error('Check your login email address please')
        exit(-1)
    if not loginTest('ywt-ywt@qq.com', '(imp@h01)'):
        logger.error('Login Failure. Check your user name or password.')

    if len(args.time) == 4:  # 头部加0
        args.time = '0' + args.time
    logger.info(
        'User {} Password {} Sending file at {} every {} day.'.format(args.user, args.password, args.time, args.day))
    while True:
        delay(args.time)
        logger.info('Start')
        post(args.user, args.password)
        logger.info('Finished, waiting for the next time')
        time.sleep(60 * 60 * 24 * args.day - 20)
