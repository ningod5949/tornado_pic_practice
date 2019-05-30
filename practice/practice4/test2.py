import hashlib

a = hashlib.md5('qq'.encode('utf8'))

print(a)
print(a.digest())
print(a.digest().hex())

# ps -ef|grep redis
# redis-cli
# pip install redis
# pip install pycket