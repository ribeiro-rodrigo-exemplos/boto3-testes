import http.client 
import pprint
import json

def request_python_org():
    connection = http.client.HTTPSConnection('www.python.org',80,timeout=10)
    print(connection)
    connection.close()

def test_get():
    connection = http.client.HTTPSConnection('www.journaldev.com')
    connection.request('GET','/')
    response = connection.getresponse()
    print("Status: {} and reason: {}".format(response.status,response.reason))
    connection.close()

def teste_get_header():
    connection = http.client.HTTPSConnection('www.journaldev.com')
    connection.request('GET','/')
    response = connection.getresponse()
    headers = response.getheaders()

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint("Headers: {}".format(headers))
    connection.close()

def teste_post():
    connection = http.client.HTTPSConnection('www.httpbin.org')
    headers = {'Connection-type':'application/json'}
    foo = {'text':'Hello HTTP'}
    json_data = json.dumps(foo)
    connection.request('POST','/post',json_data,headers)

    response = connection.getresponse()
    print(response.read().decode())


def teste_put():
    connection = http.client.HTTPSConnection('www.httpbin.org')
    headers = {'Content-type':'application/json'}

    foo = {'text':'Hello HTTP'}
    json_data = json.dumps(foo)

    connection.request('PUT','/put',json_data)
    response = connection.getresponse()
    print(response.status,response.reason)

#request_python_org()
#test_get()
#teste_get_header()
#teste_post()
teste_put()