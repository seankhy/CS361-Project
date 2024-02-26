# CS361-Project


In my app, if the user tries to programmatically request data from the implemented microservice, which in my app is the export feature of an expense tracker. A client application can make an HTTP GET request to the microservice's endpoint. In Python, the requests library can be utilized to send a GET request to the microservice's URL. The URL should be the full path where the microservice is exposed, including the domain, port, and specific route defined for exporting data. 
An example call might look like requests.get("http://localhost:5000/export")

Receiving data from the microservice involves handling the response from the aforementioned request. Once the request is made, the microservice processes it and sends back a response, which the client application receives. In the case of an export feature, it should be a CSV file containing the requested data. The client application will check the HTTP status code of the response to ensure the request was successful (200 OK status). It can then read the response body to access the returned data.
