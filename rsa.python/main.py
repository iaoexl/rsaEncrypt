#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP
import base64
import os
import sys

class RSAEncryptor:
    def __init__(self):
        self.config = configparser.ConfigParser()
        current_dir = os.path.dirname(sys.argv[0])
        config_path = os.path.join(current_dir, 'config.ini')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config.read_file(f)
            raw_key = self.config.get('RSA', 'public_key')
            self.public_key = f'-----BEGIN PUBLIC KEY-----\n{raw_key}\n-----END PUBLIC KEY-----' if not raw_key.startswith('-----BEGIN PUBLIC KEY-----') else raw_key
            self.message = self.config.get('RSA', 'message')
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            print(f"配置读取错误: {e}")
            exit(1)

    def encrypt(self):
        try:
            key = RSA.import_key(self.public_key)
            version = self.config.get('RSA', 'version', fallback='rsa1')
            if version == 'rsa1':
                cipher = PKCS1_v1_5.new(key)
            elif version == 'rsa2':
                cipher = PKCS1_OAEP.new(key)
            encrypted = cipher.encrypt(self.message.encode('utf-8'))
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception as e:
            print(f"加密时出错: {e}")
            print(f"公钥内容: {self.public_key}")
            print(f"消息内容: {self.message}")
            return None

    def save_result(self, encrypted_message):
        if encrypted_message is None:
            print("加密失败，请检查配置和输入信息")
        else:
            print(f"加密成功，结果如下:\n{encrypted_message}")

def main():
    encryptor = RSAEncryptor()
    encrypted = encryptor.encrypt()
    if encrypted:
        encryptor.save_result(encrypted)
    input("按回车键退出...")

if __name__ == "__main__":
    main()

