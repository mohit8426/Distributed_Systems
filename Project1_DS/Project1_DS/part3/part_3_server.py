from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

# Global variable
SERVER = SimpleXMLRPCServer(('localhost', 5050))
THREAD_CLIENT = {}

# Asynchronus sorting array
def async_sort_array(client_array, thread_id):
    client_array.sort()
    THREAD_CLIENT.update({thread_id: client_array})
    return True

# Synchronus sorting array
def sync_sort_array(client_array):
    client_array.sort()
    print(client_array)
    return client_array

# Asynchronus Addition
def async_add_two_num(num1, num2, thread_id):
    result = int(num1 + num2)
    THREAD_CLIENT.update({thread_id: result})
    return True

# Synchronus addition
def sync_add_two_num(num1, num2):
    return int(num1) + int(num2)

# Storing thread result as dictionary in THREAD_CLIENT list
def async_thread_result(status):
    try:
        return THREAD_CLIENT[status]
    except KeyError:
        exception = "The Entered ID is not correct. Please enter correct ID"
        return exception

# Main block
def main():
    # Register function to call from client
    SERVER.register_function(async_sort_array)
    SERVER.register_function(sync_sort_array)
    SERVER.register_function(async_add_two_num)
    SERVER.register_function(sync_add_two_num)
    SERVER.register_function(async_thread_result)
    # server started
    SERVER.serve_forever()

# Execution point of entry
if __name__ == "__main__":
    try:
        print("Server has started")
        main()
    except KeyboardInterrupt:
        print("Exiting the server")