import time
import xmlrpc.client
import os

PROXY = xmlrpc.client.ServerProxy('http://localhost:3000')

# This the function for main with all the functions are called.
def main():
    previous_check_file = os.listdir('./CLIENT_FOLDER/')
    #Variable to check the previous time of the file 
    previous_checked_time = time.time()
    try:
        #While loop for the menu() function.
        while True:
            print("A check for consistency will run after 20 seconds")
            time.sleep(20)
            print("Consistency will be checked now")
            # Scanning the files for the consistency check 
            client_exist_file = os.listdir('./CLIENT_FOLDER/')
            for file in client_exist_file:
                # For loop to check the time of the file 
                f_path = './CLIENT_FOLDER/' + file
                if os.path.getmtime(f_path) > previous_checked_time:
                    #if loop to Upload the File in to the server 
                    if file not in previous_check_file:
                        print(f"A new file {file} is being uploaded")
                        
                        f_path = "./CLIENT_FOLDER/" + file
                        with open(f_path, "rb") as files:
                            f_binary =  xmlrpc.client.Binary(files.read())
                        PROXY.svr_download(f_binary, file)
                        previous_check_file.append(file)
                        #else loop to Upload the File in to the server 
                    else:
                        print("Uploading" + file) ##
                        f_path = "./CLIENT_FOLDER/" + file
                        with open(f_path, "rb") as files:
                            f_binary =  xmlrpc.client.Binary(files.read())
                        PROXY.svr_download(f_binary, file)
            for file in previous_check_file:
                #if loop to Delete the File in to the server 
                if file not in client_exist_file:
                    print(f'{file} is being deleted from server')
                    filepath = "./CLIENT_FOLDER/" + file
                    result = PROXY.svr_delete(file)
                    print(result)
                    previous_check_file.remove(file)
            previous_checked_time = time.time()
    except KeyboardInterrupt:
        print("Exited from client")

# Running of the program starts from here
if __name__ == "__main__":
    main()