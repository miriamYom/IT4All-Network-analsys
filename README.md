# IT4All Network Analysis Application
# Bootcamp project on behalf of Nvidia
This application analyzes network traffic and displays it visually,  Using with a graph data structure. The system is used as a tool for communication technicians to obtain network visualization and analysis. It can be used to identify faulty devices, create clarity about the different devices and networks, and ensure efficient service.

The application is built on a stack of technologies, including:

- Python server implemented with FastAPI
- MySQL database
- External APIs
- React front end
The application allows users to visualize and manipulate graph data.

# Features
The project has the following features:
* Ability to load network capture files.
* Ability to describe the network using a graph.
* Sending a network ID will show the devices available on the network.
* Advanced access and identification permissions - A user-based authentication system for the technicians and the clients they are authorized to work with.

# Getting Started
To get started with the project, you will need to have Python, and React installed. You can then clone the repository and install the dependencies using the following commands:

#### pip install -r requirements.txt

#### npm install

Once you have installed the dependencies, you can start the application by running the following command:

#### uvicorn main:app --reload

This will start the application on port 8080. You can then open the application in a web browser by visiting http://localhost:8080.
