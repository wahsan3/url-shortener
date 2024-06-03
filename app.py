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
        if 'url' in request.form.keys(): # request.form is a dictionary object from Flask that contains all the data submitted with a form. request.form.keys() returns a view object that displays all the keys in the request.form dictionary. 
            urls[request.form['code']] = {'url':request.form['url']} #request.form['code'] retrieves the value of the form field named 'code,' which is the short code of the URL. request.form['url'] retrieves the value of the form field named 'url', which contains the actual URL to be stored. When they are set equal to one another, you are creating a new entry in the 'urls' dictionary.
        else:
            f = request.files['file'] #request.files['file'] retrieves the uploaded file from the form. request.files is a dictionary object provided by Flask that contains all the files uploaded with the form. 
            full_name = request.form['code'] + secure_filename(f.filename) #Generates a secure and unique filenae for the uploaded file. request.form['code'] retrieves the value of the form field named 'code'. secure_filename(f.filename) is a function from werkzeug.utils that sanitizes the filename to ensure it is safe and free of potentially harmful characters, which prevents issues like directory traversal attacks. The concatenation combines the short code with the sanitized original filename to create a unique filename.
            f.save('C:/Users/wahsa/OneDrive/Desktop/url-shortener/static/user_files/' + full_name) #Saves the uploaded file to a specific directory on the server. This ensures the file is saved in the designated directory, making it accessible later.
            urls[request.form['code']] = {'file':full_name} #Updates the 'urls' dictionary to include the uploaded file's information. Adds or updates the entry in the 'urls' dictionary with the short code as the key and the dictionary containing the filename as the value.


        with open('urls.json', 'w') as url_file: #opens the file 'urls.json' in write mode ('w'). If the file does not exist, it will be created. If it does exist, its contents will be overwritten. 
            json.dump(urls, url_file) #Writes the 'urls' dictionary to 'urls.json in JSON format. json.dump() is a function from the json module that serializes a Python object (in this case, the 'urls' dictionary) as a JSON formatted stream to a file-like object. This effectively writes the 'urls' dictionary to 'urls.json'.
            session[request.form['code']] = True # Adds an entry to the session dictionary with the short code as the key and 'True' as the value. This can be used to keep track of which short codes the user has created during their session.
        return render_template('your_url.html', code=request.form['code']) #render.template() is a Flask function that renders an HTML template. 'your_url.html' is the name of the template to render. code=request.form['code'] passes the short code to the template as a context variable named 'code', which allows the template to access and display the short code.
    else:
        return redirect(url_for('home')) #If the request method is not POST, redirect(url_for('home')) returns a response object that redirects the client to the 'home' endpoint using Flask's 'url_for()' function.

#We can provide a url, give it a short name, and it will go to that url 
@app.route('/<string:code>') #Defines a route in your Flask application that matches any URL path consisting of a single string after the root URL.
def redirect_to_url(code): #Defines a function to handle the logic for redirecting based on the provided 'code'. 'code' is the variable part of the URL captured by the route.
    if os.path.exists('urls.json'): #Returns 'True' if the file 'urls.json' exists.
        with open('urls.json') as urls_file: #Opens the file in read mode. 
            urls = json.load(urls_file) #Reads the JSON data from the file and converts it into a Python dictionary.
            if code in urls.keys(): #This line checks if the 'code' parameter provided in the URL exists as a key in the urls dictionary. If the key exists the code inside this block is executed.
                if 'url' in urls[code].keys(): #This line checks if the dictionary entry for the given 'code' contains a key named 'url.' The 'urls[code]' is itself a dictionary, and this line is verifying whether it has a 'url' key. If the 'url' key is present, it means the code maps to a URL.
                    return redirect(urls[code]["url"])
                else:
                   return redirect(url_for("static", filename = 'user_files/' + urls[code]['file'])) #If the 'url' key is not found, it meansthe code maps to a file rather than a URL. 'urls[code]['file] retrieves the filename associated with the code. This generates a URL for the file located in the 'static/user_files/' directory within the Flask application.

    return abort(404)

@app.errorhandler(404) #This line is a decorator that tells Flask to execute the decorated function whenever a 404 (Not Found) error occurs. The '404' code is an HTTP status code indicating that the requested resource could not be found on the server.
def page_not_found(error): #This defines the function 'page_not_found' that will handle the 404 error. This function accepts one parameter, 'error', which contains details about the error that triggered this handler.
    return render_template('page_not_found.html'), 404 #This function call uses Flask's 'render_template' method to render an HTML template called 'page_not_found.html'. The second value '404' after the comma is the status code that should be sent back to the client along with the rendered template. 

#A client will make a request to the '/api' endpoint. Flask calls the 'session_api' function to handle the request. The list of session keys is converted to JSON and returned to the client.
@app.route('/api') #This line is a decorator that creates a route for the Flask application that tells Flask to execute the 'session_api' function whenever a request is made to the '/api' URL endpoint.
def session_api():
    return jsonify(list(session.keys())) #'session.keys() is used to store data across requests for a particular user, and returns a view object that displays a list of all the keys in the session dictionary. jsonify is a function provided by Flask to create a JSON response from the given data.
    