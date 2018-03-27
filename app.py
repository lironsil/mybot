from flask import Flask
import json

app = Flask(__name__)
 


@app.route("/average")
def average():
	jsonFile = open('bot_avg.json', 'r')
	values = json.load(jsonFile)
	jsonFile.close()
	return str(values['average'])

 
 
@app.route("/average/<string:name>/")
def username(name):
	jsonFile = open('users_avg.json', 'r')
	values = json.load(jsonFile)
	jsonFile.close()
	return str(values[name]['average'])

 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)