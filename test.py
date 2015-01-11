import json
import Queue

class User():
    def __init__(self, username, ip, gameid=-1):
        self.username = username
        self.ip = ip
        self.gameid=gameid




if __name__ == "__main__":
    user1 = User("serbs","sss",334)
    user2 = User("serbs","sss")

    my_queue = Queue.Queue(maxsize=0)
    my_queue.put(user1)
    my_queue.put(user2)
    my_queue.put("1")
    my_queue.put("2")
    my_queue.put("3")
    print my_queue.get()
    my_queue.task_done()





def fromjson(val):
    #E.g. val is {"username": "Joe", "ip": "11.11.11.11", "serverip": "10.24.56.78", "serverport": "9898"}
    data = json.loads(val)
    return data
    #array = json.load(val)
    #return array

def jsonTest():

    python_object = {'some_text': 'my text',
                     'some_number': 12345,
                     'null_value': None,
                     'some_list': [1,2,3]}
    # here we are converting python object to json string
    json_string = json.dumps(python_object)
    # json_string = '{"some_list": [1, 2, 3], "some_text": "my text",
    #                 "some_number": 12345, "null_value": null}'
    # api converts a python dictionary to json object and vice versa
    # At this point we have a json_string in our hands. Now lets convert it back to pyton structure
    new_python_object = json.loads(json_string)
    # new_python_object = {u'some_list': [1, 2, 3], u'some_text': u'my text',
    #                      u'some_number': 12345, u'null_value': None}

    json_string='{"name":"Product-1","quantity":1,"price":12.50}'
    val = json.loads(json_string)
    #{u'name': u'Product-1', u'price': 12.5, u'quantity': 1}


    word = "This is some random text"
    word = 'PCCONN|{"username": "Joe", "ip": "11.11.11.11", "serverip": "10.24.56.78", "serverport": "9898"}'
    words2 = word.split("|")

    #json_string='{"username":"Joe","ip":"11.11.11.11","serverip":"10.24.56.78", "serverport": "9898"}'
    #val = json.loads(json_string)

    val = fromjson(words2[1])
    var = "ww"
