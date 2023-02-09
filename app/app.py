import pycurl
import base64
from flask import Flask, request, render_template
from io import BytesIO

app = Flask(__name__, template_folder='html')

@app.route('/', methods=['GET', 'POST'])
def get_webpage():
    
    if request.args.get('img_url'):
        achilles_image_url = request.args.get('img_url')
    elif request.form.get('img_url'):
        achilles_image_url = request.form.get('img_url')
    else:
        achilles_image_url = "https://storage.googleapis.com/achilles_bucket/face.jpg"
        
    buffer = BytesIO()
    curl = pycurl.Curl()  
    curl.exception = None
    curl.setopt(curl.URL, achilles_image_url)
    curl.setopt(curl.WRITEDATA, buffer)
    try:
        curl.perform()
    except Exception as e:
        buffer.write(str(curl.exception).encode('utf-8'))
    finally:
        img_data_raw = buffer.getvalue()
    
    curl.close()
    img_data_b64 = base64.b64encode(img_data_raw).decode('utf-8')
      
    achilles_html_response = render_template(
        template_name_or_list = "app.html",
        img_data = img_data_b64,
    )
    
    return achilles_html_response    
    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)