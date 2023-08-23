import threading
import random
import xmlrpc.client

# Global variable
PROXY = xmlrpc.client.ServerProxy("http://localhost:5050")
MENU = {
    1: "Addition using Synchronous method",
    2: "Addition using Asynchronous method",
    3: "Sorting using Synchronous method",
    4: "Sorting using Asynchronous method",
    5: "Result for Asynchronous method",
    6: "Exit"
}
# Keeping track for threads status
thrs = []

# synchronus sort
def synchro_sorting():
    arr = [data for data in input("Enter the data to be sorted: ").split()]
    result = PROXY.sync_sort_array(arr)
    print(result)

# asynchronus sort
def asynchro_sorting():
    arr = [data for data in input("Please enter the data you want to sort: ").split()]
    thread_id = "Sort-" + str(random.randint(1, 30))
    result = threading.Thread(target=PROXY.async_sort_array, args=(arr, thread_id,))
    thrs.append(result)
    print(f"ID for Asynchronous add: {thread_id}")
    result.start()
    result.join()

# synchronus addition
def sync_add():
    n1 = input("Enter the first number: ")
    n2 = input("Enter the second number: ")
    result = PROXY.sync_add_two_num(n1, n2)
    print(result)

# asynchronus addition
def async_add():
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))
    thread_id = "Add-" + str(random.randint(1, 30))
    result = threading.Thread(target=PROXY.async_add_two_num, args=(num1, num2, thread_id,))
    thrs.append(result)
    print(f"ID for Asynchronous add: {thread_id}")
    result.start()
    result.join()

# menu display
def menu_display():
    for key in MENU.keys():
        print(key, MENU[key])

# main function
def main():
    # Menu running forever
    while True:
        menu_display()
        option = " "
        try:
            user_option = int(input("Select one of the above option"))
            if user_option > 6:
                print('Choice is not vaild. Please select one of the above options')
        except ValueError:
            print("Choice is not valid ")
        if user_option == 1:
            sync_add()
        elif user_option == 2:
            async_add()
        elif user_option == 3:
            synchro_sorting()
        elif user_option == 4:
            asynchro_sorting()
        elif user_option == 5:
            status = input("Please enter the ID:")
            print(PROXY.async_thread_result(status))
        elif user_option == 6:
            print("Exiting client") 
            exit()
        
# Execution start point
if __name__ == "__main__":
    main()