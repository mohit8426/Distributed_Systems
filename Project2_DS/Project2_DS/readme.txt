You can directly run the code from command line using 'python <code_name.py>

Follow the below steps to run the program as per the requirements:
Part 1:
1) First you will be asked for participant 1 select "1=put"
2) Enter the message.
3) Now you will be asked for participant 2 select "1=put"
4) Enter the message.
5) Wait and do nothing the transaction coordinator will fail and the transaction will get aborted.

Part 2:
1) First you will be asked for participant 1 select "1=put"
2) Enter the message.
3) Now you will be asked for participant 2 select "1=put"
4) Enter the message.
5) After the program starts to run after 2 secs press enter and now you will be asked to enter 'yes' or 'no'. Enter yes.
6) For participant 2 don't enter anything.
7) Transaction will time-out and it will get aborted.

Part 3:
1) First you will be asked for participant 1 select "1=put"
2) Enter the message.
3) Now you will be asked for participant 2 select "1=put"
4) Enter the message.
5) After the program starts to run after 2 secs press enter and now you will be asked to enter 'yes' or 'no'. Enter yes.
6) You will be asked the same thing for participant 2. Enter yes.
7) You will be asked to 'ack' or 'nack' for participant 1. Enter ack.
8) The same thing will be asked for participant 2 don't enter anything.

Part 4:
1) First you will be asked for participant 1 select "1=put"
2) Enter the message.
3) Now you will be asked for participant 2 select "1=put"
4) Enter the message.
5) After the program starts to run after 2 secs press enter and now you will be asked to enter 'yes' or 'no'. Enter yes.
6) You will be asked the same thing for participant 2. Enter yes.
7) You will be asked to 'ack' or 'nack' for participant 1. Enter ack.
8) After that don't do anything the participant randomly times out after sending yes.
9) Again the participant comes back up and asks it for yes or no.
10) It sends yes but the TC has timed out and hence it sends tc already timed out and abort is sent.