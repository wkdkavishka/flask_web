from website import create_app

app = create_app()

if __name__ == '__main__': # if for some reason need to import from this file
    app.run(debug=True)     # rerun the server upon any changes to the code
