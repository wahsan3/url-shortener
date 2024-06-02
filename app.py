from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os.path
from werkzeug.utils import secure_filename

#These first two lines of code set up a basic Flask application and configure a secret key necessary for securely handling sessions and cookies.
app = Flask(__name__) #This line initializes a new Flask web application. 'Flask' is a class provided by the Flask framework. '__name__' is a special variable in Python that represents the name of the current module. When the module is run directly, '__name__' is set to "__main__" By passing '__name__' to the 'Flask' constructor, Flask can determine the root path of the application to locate resources like templates and static files.
app.secret_key = 'jfrwnvjjvjrcfeejfnf' #This line sets a secret key for the Flask application. The secret key is used by Flask (and some of its extensions) for various security-related purposes, such as signing cookies and session data to prevent tampering. 

#At a high level, these next three lines of code has the user access the root URL ('/') of the Flask web application, and Flask will route this request to the 'home' function due to the @app.route('/') decorator. The 'home' function renders the 'home.html' template, and the rendered HTML is sent back to the user's browser as the response, displaying the homepage. 
@app.route('/') #This line tells Flask that the following function ('home') should be called when the root URL (i.e., '/') is accessed. The root URL typically represents the home page of the web application. 
def home(): #This function will be executed when the root URL is accessed due to the decorator above it.
    return render_template('home.html', codes=session.keys()) #This line returns the rendered HTML content of the 'home.html' template. 'render_template' is a function provided by Flask that renders an HTML template and returns it as a response to the client's request. 'home.html' is the name of the HTML template file that will be used to generate the content for the home page. This file should be located in the 'templates' folder within the Flask application.

@app.route('/your-url', methods=["GET", "POST"]) #@app.route(...) - Decorators are a way to modify the behavior of a function or method. In Flask, route decorators are used to bind URLs to functions so that Flask knows which function to execute when a specific url is requested. '/your-url' is the URL endpoint for the route. Flask will trigger the following function this decorator is applied to. The string '/your-url' defines the specific URL path at which the function should be accessible. 'methods= ["GET", "POST"]' - This specifies the HTTP methods this route can handle. GET: Used to request data from the server. When a user navigates to http://127.0.0.1:5000/your-url, a GET request is sent. POST is used to send data to the server, usually through forms. The function will process the submitted form data or perform another action based on the input.
def your_url():
    if request.method == "POST": #If the request method is POST, it creates an empty dictionary 'urls'. The function is therefore preparing to handle form data or input that may be sent with a POST request.
        urls = {} #urls = {} initializes an empty dictionary to potentially store data from the POST request.

        #If a JSON file named urls.json exists and if it does, read the contents of the file and parse it as Json, and load its contents into a dictionary.
        if os.path.exists('urls.json'): #Checks if the file urls.json exists in the current working directory. os.path is a module in Python's standard library that provides functions for interacting with the file system. 'exists' is a function in the 'os.path' module that returns 'True' if the specified path (urls.json) exists, and 'False' otherwise.
            with open('urls.json') as urls_file: #open('urls.json') is a function call that opens the file 'urls.json' in read mode by default. urls_file is a file object that provides methods and attributes to read the contents of the file.
                urls = json.load(urls_file) #'json.load(urls_file)' is a function call that reads the content of 'urls_file' and parses it as JSON. 'load' is a function in the 'json' module that reads a file-like object containing a JSON document and returns a Python dictionary. 'urls' is the variable that will hold the parsed Json data, typically a dictionary.

        #These three lines of code are used to check if a submitted form field value (specifically, a code which is a short name) is already present in the 'urls' dictionary. If it is, a flash message is displayed to the user, and they are redirected to the home page. 
        if request.form['code'] in urls.keys(): #request.form is a dictionary-like object provided by Flask that contains the data submitted with the form in the POST request. request.form['code'] retrieves the value associated with the form field names 'code'. urls.keys() returns a view object that displays a list of all the keys in the 'urls' dictionary. If the data submitted with the form in the POST request is one of the keys in the 'urls' dictionary, the condition evaluates to 'True', and the indented block of code is executed.
            flash('That short name has already been taken. Please select another name.') #'flash' is a function provided by Flask that allows you to send a one-time message to the next request. Flash messages are used for displaying informational messages, warnings, or errors to the user. 
            return redirect(url_for('home')) #redirect is a function provided by Flask that returns a response object that redirects the client to a target location. 'url_for('home')' generates a URL for the 'home' endpoint using Flask's 'url_for' function. The 'return redirect(url_for('home'))' sends a response back to the client that instructs the browser to navigate to the home page.
        
        #These lines handle the submission of form data, specifically dealing with two cases: submitting a URL or uploading a file. Depending on the contents of the form, the appropriate action is taken to store the data in the 'urls' dictionary or save the uploaded file to the server.
        if 'url' in request.form.keys(): # 
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('C:/Users/wahsa/OneDrive/Desktop/url-shortener/static/user_files/' + full_name)
            urls[request.form['code']] = {'file':full_name}


        with open('urls.json', 'w') as url_file: #Only move forward if you're able successfully create or open this url.json with the name url_file. Whatever's inside the dictionary and save it there
            json.dump(urls, url_file) #dump the dictionary urls into the url_file.
            session[request.form['code']] = True 
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))

#We can provide a url, give it a short name, and it will go to that url 
@app.route('/<string:code>')
def redirect_to_url(code): 
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]["url"])
                else:
                   return redirect(url_for("static", filename = 'user_files/' + urls[code]['file'])) 

    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))
    #jsonify - takes a list or dictionary and turns it into JSON code

#Get request - All the data from the form is displayed inside the URL
#Post request - takes the information and one can have access to it in the app.py file.

