# CS361-Project

A:
In my app, if you try to programmatically REQUEST data from the microservice, which in my app is the export feature of an expense tracker. A client application can make an HTTP GET request to the microservice's endpoint. In Python, the requests library can send a GET request to the microservice's URL. The URL should be the full path where the microservice is exposed, including the domain, port, and specific route defined for exporting data. 
***Note: You must run my app locally first and get the localhost URL***
An example call in your code might look like this " requests.get("http://localhost:5000/export") "

B:
Receiving data from my microservice involves handling the response from the above requirements request. Once your request is made, the microservice processes it and sends back a response, which the client application receives. In the case of an export feature, it should be a CSV file containing the requested data. The client application will check the HTTP status code of the response to ensure the request was successful (200 OK status). It can then read the response body to access the returned data. So, after you programmatically RECEIVE data from my microservice, you should be able to see the data you receive will be a CSV file that contains the Amount data from my web app.


<img width="765" alt="Screenshot 2024-02-26 at 8 03 30 PM" src="https://github.com/seankhy/CS361-Project/assets/130083506/020109e1-6170-4790-98e5-eeeab2c039a1">
