# CirroSockets

CirroSockets is an early alpha, lightweight **websockets** broadcasting project written using Python and the Bottle web framework. CirroSockets uses the *Bottle* (Python) web framework.

## Getting Started
1. Run `./install_packages && ./start_server` in Terminal
2. Open two browser windows to http://localhost:8080/ws.html and send messages

## Notes
* `requirements.txt` contains requirements to be installed using `pip`. `pip` is therefore required. 
* Python is required
* This project primarily consists of a Bottle server, glued to a simple WSGIServer with WebSockets enabled, with an HTML page that connects to the WSGIServer