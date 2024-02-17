import openai
from flask import Flask, render_template, request

# Set up OpenAI API key
openai.api_key = 'API-KEY'

# Function to interact with GPT-3.5 chat model
def chat(query):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": "You are a friend who can understand emotions and mental health and can give solutions to being happy in 4 to 5 points with positive outlook in the end"
        }, {
            "role": "user",
            "content":f"{query}"
        }]
    )
    return response.choices[0].message.content

# Function to generate an image using DALL-E 2 model
def generate_image(cmd):
    response = openai.images.generate(
        model="dall-e-2",
        prompt=cmd,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return image_url

# Initialize Flask app
app = Flask(__name__, template_folder="html")

# Route for homepage
@app.route('/', methods=['GET', 'POST'])
def hello():
    output1 = ""
    output2 = ""
    if request.method == 'POST':
        # Get user input from form
        query = request.form['query']
        output1 = chat(query)
        
        # Get command from JSON data from the query
        cmd = request.json['cmd']
        output2 = generate_image(cmd)
    # Render template with outputs
    return render_template("template.html", output1=output1, output2=output2)

# Route for chat functionality
@app.route('/chat', methods=['POST'])
def generate():
    # Get user input from form
    query = request.form['query']
    # Call chat function and return result
    return chat(query)

# Route for image generation
@app.route('/generate', methods=['POST'])
def pic():
    # Get command from JSON data
    cmd = request.json['cmd']
    # Call generate_image function and return result
    return generate_image(cmd)

# Run the app if this file is executed directly
if __name__ == '__main__':
    app.run()
