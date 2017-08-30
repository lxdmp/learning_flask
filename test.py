import flask

app = flask.Flask(__name__)

@app.route('/')
def test():
	return 'test here!'

if __name__=='__main__':
	app.run()

