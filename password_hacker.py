#! /usr/bin/python3

import requests
import hashlib


def request_api_date(query_char):
    base_url = 'https://api.pwnedpasswords.com/range/' + str(query_char)
    res = requests.get(base_url)
    if res.status_code != 200:
        raise RuntimeError(f'error fetching:{res.status_code}, try again')
    return res


def pwned_api_check(password):
	sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	head, rest = sha1password[:5], sha1password[5:]
	response = request_api_date(head)
	count = check_pwd_leak(response,rest)
	return count
	
def check_pwd_leak(hash, hash_to_check):
	# print(hash.text.splitlines())
	for i in hash.text.splitlines():
		k,v = i.split(':')
		if k == hash_to_check:
			return v
	return 0

	

def main(password):
	for i in password:
		count = pwned_api_check(i)
		if count:
			print(f'{i} has been exploited {count} times')
		else:
			print(f'{i} is safe, feel free to use')

myset = set()
for line in open ('pwd.txt','r'):
	myset.add(line.strip('\n'))
	
main(myset) 

	
	
w