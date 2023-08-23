import xmlrpc.client
import os

#Initializing the Global variable PROXY
PROXY = xmlrpc.client.ServerProxy('http://localhost:3000')

CLIENT_FOLDER_PATH = "./CLIENT_FOLDER/"     #Path for Client folder
SERVER_FOLDER_PATH = "./SERVER_FOLDER/"     #Path for Server Folder

#Menu Buttons to Select the Operations 
MENU = {
    1: "Upload File",
    2: "Download File",
    3: "Rename File",
    4: "Delete File",
    5: "Exit"
}

# This the function for main with all the functions are called.
def main():
    #While loop for the menu() function.
    while True:
        
        for key in MENU.keys():
            print(key, ")", MENU[key]) 
        option = " "

        try:
            menu_option = int(input("Select one of the options given above:"))

        except:
            print(" Selected option is invalid. Please try again ")

        #if loop for the menu option 1 to Upload a File in to the server 
        if menu_option == 1:
            f_name = input("Please enter the name of the file that you want to upload:")
            f_path = CLIENT_FOLDER_PATH + f_name
            if os.path.exists(f_path):
                print("Uploading the file mentioned above to the server")
                print("File is Uploaded succesfully")
                with open(f_path, "rb") as file:
                    f_binary =  xmlrpc.client.Binary(file.read())
                PROXY.svr_download(f_binary, f_name)
            else:
                result = "Sorry the file you entered does not exist in Client"
                print(result)
        #if loop for the menu option 2 to Download the File in to the server 
        elif menu_option == 2:
            f_name = input("Please enter the name of the file that you want to download:")
            f_path = CLIENT_FOLDER_PATH + f_name
            if os.path.exists(f_path):
                with open(f_path, "wb") as file:
                    file.write(PROXY.svr_upload(f_name).data)
                print("Finished downloading file")    
            else:
                result = "Sorry the file you entered does not exist in Client"
                print(result)        

        #if loop for the menu option 4 to Rename the File in to the server 
        elif menu_option == 3:
            current_file_name = input("Enter the name of the file you want to rename: ")
            new_file_name = input("Enter new name for the file: ")
            current_file_path = CLIENT_FOLDER_PATH + current_file_name
            new_file_path = CLIENT_FOLDER_PATH + new_file_name
            if os.path.isfile(new_file_path):
                result = "This file already exists in Client"
                print(result)
            else:
                os.rename(current_file_path, new_file_path)
                result = "Successfully renamed in Client"
                print(result)
            print(PROXY.svr_rename(current_file_name, new_file_name))
        #if loop for the menu option 4 to Delete the File in to the server 
        elif menu_option == 4:
            f_name = input("Enter the name of the file you want to delete on Client and Server: ")
            
            file_path = CLIENT_FOLDER_PATH + f_name
            if os.path.exists(file_path):
                os.remove(file_path)
                result = "Deleted file " + f_name + " from client "
                print(result)
                result = PROXY.svr_delete(f_name)
                print(result)
            else:
                print("Sorry the file you entered does not exist in Client")
                result = PROXY.svr_delete(f_name)
                print(result)
        #if loop for the menu option 5 to Exit the Menu options 
        elif menu_option == 5:
            print("Exiting the Menu options")
            exit()            

# Execution start
if __name__ == '__main__':
    main()