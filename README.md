# Daily Chores
## Components
### Users
Users are members of the household that are using the system that is created to orchestrate chores and help with automating simple thing.

### Chores
*Chores* are going to be assigned to *users* in a round-robin fashion. Let's say that we have N users. In this case, when a chore is completed, it is assigned to the individual that has not done it in the last N-1 iterations.

### Devices
This is a future feature which will allow us to interact with automated devices within the home network.

## Usage
V0 of the product will be using siri shortcuts alongside a Flask REST API to communicate with the server.

### Update Chore Status
1) `POST /chores/<chore identifier>/<username>`\
    Currently supported chores - 
    1) dishes
    2) trash
2) Siri sends text message with update


## Future
1) Visaulization
2) Cara to analyze traffic outside
