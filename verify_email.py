#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
在线验证邮箱真实性
"""

import random
import smtplib
import logging
import sys
import time
import dns.resolver
from colorama import Fore, init

init(autoreset=True)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s [line:%(lineno)d] - %(levelname)s: %(message)s')

logger = logging.getLogger()


def fetch_mx(host):
    """
    解析服务邮箱
    :param host:
    :return:
    """
    logger.info('正在查找邮箱服务器')
    answers = dns.resolver.query(host, 'MX')
    res = [str(rdata.exchange)[:-1] for rdata in answers]
    logger.info('查找结果为：%s' % res)
    return res


def verify_istrue(email):
    """
    :param email:
    :return:
    """
    email_list = []
    email_obj = {}
    final_res = {}
    if isinstance(email, str) or isinstance(email, bytes):
        email_list.append(email)
    else:
        email_list = email

    for em in email_list:
        name, host = em.split('@')
        if email_obj.get(host):
            email_obj[host].append(em)
        else:
            email_obj[host] = [em]

    for key in email_obj.keys():
        host = random.choice(fetch_mx(key))
        logger.info('正在连接服务器...：%s' % host)
        s = smtplib.SMTP(host, timeout=10)
        for need_verify in email_obj[key]:
            helo = s.docmd('HELO chacuo.net')
            logger.debug(helo)

            send_from = s.docmd('MAIL FROM:<mail@gmail.com>')    # 声明自己的邮箱，自己改
            logger.debug(send_from)
            send_from = s.docmd('RCPT TO:<%s>' % need_verify)
            logger.debug(send_from)
            if send_from[0] == 250 or send_from[0] == 451:
                final_res[need_verify] = True  # 存在
            elif send_from[0] == 550:
                final_res[need_verify] = False  # 不存在
            else:
                final_res[need_verify] = None  # 未知

        s.close()

    return final_res


def read_file(filename):
    """
    读取txt文件
    """
    with open(filename, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file]  # 列表推导式，去除每行末尾的换行符
    return lines  # 返回包含所有行内容的列表


def output_file(emails):
    """
    保存为txt文件
    """
    # 将匹配项列表写入到文本文件中
    try:
        with open('valid_emails.txt', 'a', encoding='utf-8') as file:
            file.write(emails + '\n')

    except IndexError as e:
        error_message = str(e)
        print("报错语句如下：" + error_message + '\n')

    return f"\n保存成功!文本保存为valid_emails.txt."


def main():
    if len(sys.argv) != 2:
        print("命令: python verify_email.py filename.txt")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        for e in read_file(filename):
            verify = verify_istrue(e)
            for key, value in verify.items():
                if value:
                    print(f'{Fore.GREEN}[+] 验证有效,正在保存：{key}')
                    output_file(key)
                else:
                    print(f'{Fore.RED}[-] 验证失败：{key}')
    except IndexError as e:
        error_message = str(e)
        print("报错语句如下：" + error_message + '\n')


if __name__ == '__main__':
    main()
