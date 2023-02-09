import json, requests
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='html')

@app.route('/', methods=['GET', 'POST'])
def get_webpage():
    if request.args.get('img_url'):
        achilles_image_url = request.args.get('img_url')
    elif request.form.get('img_url'):
        achilles_image_url = request.form.get('img_url')
    else:
        achilles_image_url = "https://storage.googleapis.com/achilles_bucket/face.jpg"
    
    achilles_html_response = render_template(
        template_name_or_list = "app.html",
        image_url = achilles_image_url,
    )
    
    return achilles_html_response
    
if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8095,
        debug=True
    )
