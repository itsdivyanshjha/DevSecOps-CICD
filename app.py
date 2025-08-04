from flask import Flask, jsonify

# Create an instance of the Flask class
app = Flask(__name__)

# Define a route for the root URL '/'
@app.route('/')
def home():
    """This function runs when someone visits the main page."""
    return jsonify(message="Hello! This is a simple Flask app for the DevSecOps demo.")

# Run the app
if __name__ == '__main__':
    # Bind to 0.0.0.0 to make it accessible from outside the container
    app.run(host='0.0.0.0', port=5000)