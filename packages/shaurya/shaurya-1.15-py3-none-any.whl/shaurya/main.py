import os
import requests
from flask import Flask

# SAFED_FOR_LATER

def open_file(file_name):
    os.system('open '+file_name)
 
def create_file(name, var="File created by shaurya inc. Remove this text please."):
    f= open(name,"w+")
    f.write(var)

def return_status_code(site):
    response = requests.get(site)
    status = response.status_code
    if status != 200:
       print("Status code {}, please check site!".format(status))
    else:
        return status


def flask(text):
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return text

    if __name__ == "__main__":
        app.run()


