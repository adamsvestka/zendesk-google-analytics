#!/usr/bin/python3

from base64 import b64encode


username = input('username (email): ')
password = input('password: ')
combined = username + ':' + password
encoded = b64encode(combined.encode('utf-8')).decode('utf-8')

print(encoded)