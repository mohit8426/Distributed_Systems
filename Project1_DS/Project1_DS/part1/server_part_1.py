from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import os

# Global variable
SERVER = SimpleXMLRPCServer(('localhost', 3000), logRequests=True)

SERVER_FOLDER = "./SERVER_FOLDER/"
CLIENT_FOLDER = "./CLIENT_FOLDER/"


# Function for client downloading the file from the server
def svr_download(f_binary, f_name):
    f_path = SERVER_FOLDER + f_name
    with open(f_path, "wb") as file:
        file.write(f_binary.data)
    return True


# Function for client uploading the file to the server
def svr_upload(f_name):
    f_path = SERVER_FOLDER + f_name
    with open(f_path, "rb") as file:
        return xmlrpc.client.Binary(file.read())
    

# Function for client deleting the file from the server
def svr_delete(f_name):
    file_path = SERVER_FOLDER + f_name
    if os.path.exists(file_path) == True:
        os.remove(file_path)
        result = "Deleted " + f_name + " from server"
        return result
    else:
        result = "Sorry the file you entered does not exist in Server"
        return result


# Function for client Renaming the file to the server
def svr_rename(old_filename, new_filename):
    current_file_path = SERVER_FOLDER + old_filename
    new_file_path = SERVER_FOLDER + new_filename
    if os.path.isfile(new_file_path) == True:
        result = "This file already exists in server"
        return result
    else:
        os.rename(current_file_path, new_file_path)
        result = "Successfully renamed in server"
        return result


# This the function for main with all the functions are called.
def main():
    try:
        # Function called by the client on the server using rpc
        SERVER.register_function(svr_download)
        SERVER.register_function(svr_upload)
        SERVER.register_function(svr_delete)
        SERVER.register_function(svr_rename)
        print('Server has started') 
        SERVER.serve_forever()
    except KeyboardInterrupt:
        print("Exited the server") 

# Running of the program starts from here
if __name__ == "__main__":
    main()