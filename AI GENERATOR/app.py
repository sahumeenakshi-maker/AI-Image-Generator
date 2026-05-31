import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    image_list = []
    error_message = None  # To tell you if the API failed
    
    if request.method == "POST":
        user_input = request.form.get("prompt")
        api_endpoint = "https://ai-text-to-image-generator-flux-free-api.p.rapidapi.com/aaaaaaaaaaaaaaaaaiimagegenerator/quick.php"
        # NOTE: Make sure this key matches exactly what you used in Jupyter!
        my_headers = {
            "x-rapidapi-key": "9ba3b99f07msh53e44f88a7f680ap118d0djsn1a98ab9a3664",
            "x-rapidapi-host": "ai-text-to-image-generator-flux-free-api.p.rapidapi.com",
            "Content-Type": "application/json"
        }
        
        generation_params = {
            "prompt": user_input,
            "style_id": 4,
            "size": "1-1"
        }
        
        try:
            response = requests.post(api_endpoint, json=generation_params, headers=my_headers)
            output_data = response.json()

            # Fix for KeyError: 'result'
            # We check if the 'result' key exists first
            if 'result' in output_data:
                raw_results = output_data['result']['data']['results']
                for item in raw_results:
                    image_list.append(item.get("origin"))
            else:
                # If 'result' is missing, the API probably sent an error message
                print("API Error Response:", output_data)
                error_message = "The AI is busy or the API key is incorrect."

        except Exception as e:
            print(f"Connection Error: {e}")
            error_message = "Could not connect to the AI server."
            
    return render_template("home.html", images=image_list, error=error_message)

if __name__ == "__main__":
    app.run(debug=True, port=5000)