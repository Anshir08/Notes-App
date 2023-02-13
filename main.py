from website import create_app  # website will act as python package because __init__.py in it.

app = create_app()  # object of function

if __name__ == '__main__':
    app.run(debug=True)  # running the flask app, we can do debug=false if we run the app in production