from app import app



if __name__ == '__main__':
	from werkzeug.serving import run_simple
	run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
    # app.run(debug=True, use_reloader=True)
