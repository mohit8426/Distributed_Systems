from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import os

SERVER = SimpleXMLRPCServer(('localhost', 3000), logRequests = True)

# Function for client uploading the file to the server
def svr_download(f_binary, f_name):
    f_path = "./SERVER_FOLDER/" + f_name
    with open(f_path, "wb") as file:
        file.write(f_binary.data)
    return True

# Function for client deleting the file from the server
def svr_delete(f_name):
    f_path = "./SERVER_FOLDER/" + f_name
    if os.path.exists(f_path):
        os.remove(f_path)
        result = "Deleted " + f_name + " from the server"
        return result
    else:
        result = "Sorry the file you entered does not exist in Server"
        return result

# This the function for main wit hall the functions are called.
def main():
    try:
        # Function called by the client on the server
        SERVER.register_function(svr_download)
        SERVER.register_function(svr_delete)
        print('Server has started') 
        SERVER.serve_forever()
    except KeyboardInterrupt:
        print('Exiting the Server')

# Running of the program starts from here
if __name__ == "__main__":
    main()