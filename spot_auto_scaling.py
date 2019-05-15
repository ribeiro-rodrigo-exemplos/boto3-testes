import http.client

# connection = http.client.HTTPSConnection('www.python.org', 80, timeout=10)
# print(connection)

connection = http.client.HTTPSConnection('www.journaldev.com')
connection.request('GET', '/')
response = connection.getresponse()

print("Status: {} and reason: {}".format(response.status, response.reason))
print(response.read().decode())

connection.close()
