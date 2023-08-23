import time
import random
import os
import sys
from select import select

log_file1 = "transaction.log"

if os.path.exists(log_file1):
    os.remove(log_file1)
    
log_file1 = open("transaction.log", "a")


# This function is where TransactionCoordinator receives response from participants 
def rec_resp(participant, log_file1,failed):
    log_file1.write("TransactionCoordinator Waits for response from participant {}...\n".format(participant))
    print("TransactionCoordinator Waits for response from participant {}...\n".format(participant))
    start_time = time.time()
    while True:
        if time.time() - start_time >= 5:
            log_file1.write("Timeout reached. Participant {} did not respond within time.\n".format(participant))
            print("Timeout reached. Participant {} did not respond within time.\n".format(participant))
            return False
        elif select([sys.stdin.fileno()], [], [], 5)[0]:
            response_participant = input("Enter 'yes' or 'no' for participant {}:\n ".format(participant))
            if failed == 1:
                print("The TransactionCoordinator has already time out.\n")
                send_abort(log_file1)
                main()
                
            if(random.random()<0.4):
                time.sleep(4)
                print("Participant {} timed out after replying yes.\n".format(participant))
                failed = 1
                return rec_resp(participant,log_file1,1)
            else:
                failed = 0
                log_file1.write("Participant {} responded with: {}\n".format(participant, response_participant))
            
            print("Participant {} responded with: {}\n".format(participant, response_participant))
            if response_participant.lower() == 'yes':
                return True
            elif response_participant.lower() == 'no':
                return False
            else:
                print("Response is invalid. Please enter 'yes' or 'no' only.\n")

# this function is for the transaction coordinator where it recieves the commit messages and 
def rec_commit(participant,log_file1):
    print("TransactionCoordinator waits for commit message from participant {}...\n".format(participant))
    log_file1.write("TransactionCoordinator waits for commit message from participant {}...\n".format(participant))
    start_time = time.time()
    while True:
        if time.time() - start_time >= 5:
            print("Timeout reached. Participant {} did not respond within time.\n".format(participant))
            log_file1.write("Timeout reached. Participant {} did not respond within time.\n".format(participant))
            print("TransactionCoordinator Sends commit message to {} again".format(participant))
            return rec_commit(participant, log_file1)
        elif select([sys.stdin.fileno()], [], [], 5)[0]:
            response_participant = input("Enter 'ack' to commit  or 'nack' to abort for  participant {}: \n".format(participant))
            if response_participant.lower() == 'ack':
                return True
            elif response_participant.lower() == 'nack':
                return False
            else:
                print("Response is invalid. Please enter 'ack to commit' or 'nack to abort'.\n")
# this function is to send prepare message to the participants
def send_message(log_file1):
    # for loop to send prepare message to participants
    for participant in participants:
        print("TransactionCoordinator sends prepare message to participant {}...\n".format(participant))
        log_file1.write("TransactionCoordinator sends prepare message to participant {}...\n".format(participant))
        time.sleep(1)
        response_participant = rec_resp(participant,log_file1,0)
        if not response_participant:
            # abort the  transaction and exit
            print("Participant {} responded with 'no'. Aborting the transaction.\n".format(participant))
            log_file1.write("Participant {} responded with 'no'. Aborting the transaction.\n".format(participant))
            send_abort(log_file1)
            return

    # here it confirms that all participants has responded with 'yes'
    print("All participants responded with 'yes'. Sending commit message...\n")
    time.sleep(1)
    send_commit(log_file1)

#this function is to sending commit message to participants
def send_commit(log_file1):
    # send commit message to participants
    for participant in participants:
        
        print("TransactionCoordinator Sends commit message to participant {}...\n".format(participant))
        log_file1.write("TransactionCoordinator Sends commit message to participant {}...\n".format(participant))
        time.sleep(1)
        response_participant = rec_commit(participant,log_file1)
        if not response_participant:
            # abort transaction and exit
            print("Participant {} responded with 'abort'. Aborting the transaction.\n".format(participant))
            log_file1.write("Participant {} responded with 'abort'. Aborting the transaction.\n".format(participant))
            send_abort(log_file1)
            return
        else:
            # commit transaction
            print("Participant {} responded with 'commit'. Committing the transaction...\n".format(participant))
            log_file1.write("Participant {} responded with 'commit'. Committing the transaction...\n".format(participant))
            with open('data.txt', 'r') as f:
                lines = f.readlines()
            with open('data.txt', 'w') as f:
                for line in lines:
                    if f'id={participant},' not in line:
                        f.write(line)

    # transaction has been committed successfully
    print("Transaction has committed successfully.\n")
    log_file1.write("Transaction has committed successfully.\n")

# this  function  is to send abort message to all participants
def send_abort(log_file1):
    # sending  abort message to the  participants
    for participant in participants:
        log_file1.write("TransactionCoordinator sends abort message to participant {}...".format(participant))
        print("TransactionCoordinator sends abort message to participant {}...".format(participant))
        time.sleep(1)
        clear_data_form_file()

    # transaction has been  aborted
    print("Transaction has aborted.\n")


# this function  is to clear the data file
def clear_data_form_file():
    with open('data.txt', 'w') as f:
        f.write('')


# this function is to manage the transaction
def transaction_manager(id,log_file1):
   
    

    # this simulate Transaction Coordinator failure and times out before sending prepare message
    if random.random() < 0.4:
        print("TransactionCoordinator failed before sending prepare message.\n")
        log_file1.write("TransactionCoordinator failed before sending prepare message.\n")
        time.sleep(3)
        
        transaction_manager(1,log_file1)
        return

    #for loop for sending prepare message to participants 
    PrepareMessage = []
    for participant in participants:
        log_file1.write("TransactionCoordinator sends prepare message to participant {}...\n".format(participant))
        print("TransactionCoordinator sends prepare message to participant {}...\n".format(participant))
        time.sleep(1)
        if id == 1:
            response_participant = False
            id =0
        else:
            response_participant = rec_resp(participant,log_file1,0)
        if not response_participant:
            #in this it states abort transaction and exit
            log_file1.write("Participant {} responded with 'no'. Aborting the transaction.\n".format(participant))
            print("Participant {} responded with 'no'. Aborting the transaction.\n".format(participant))
            send_abort(log_file1)
            return
        PrepareMessage.append(response_participant)

    #in this it will save to the log with all participants responded with 'yes'
    log_file1.write("All participants responded with 'yes'. Sending commit message...\n")
    print("All participants responded with 'yes'. Sending commit message...\n")
    time.sleep(1)
    send_commit(log_file1)




# main function to start the transaction
def main():
    while True:
        for participant in participants:
        # get menu option for the operation from user
            while True:
                OperationToPerform = input(f"Enter operation for participant {participant} (1=put and 2=exit): ")
                if OperationToPerform == '1':
                    message = input("Enter message to update: ")
                    with open('data.txt', 'a') as f:
                        f.write(f"{time.time()}: id={participant}, message={message}\n")
                    print(f"Participant {participant} performs 'put' operation.")
                    break
                elif OperationToPerform == '2':
                    print("Exiting...")
                    sys.exit()
                else:
                    print("Invalid operation. Please enter 1, or 2.")
        transaction_manager(0,log_file1)
    
if __name__ == '__main__':
    participants = [1, 2]
    main()