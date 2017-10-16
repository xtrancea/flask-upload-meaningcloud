import os, requests, json
from flask import Flask, request, redirect, url_for, flash, render_template, Response
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/root/myproject/upload' #change your upload folder directory
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Match file and allowed extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#Meaning cloud API

def text_lang(text):
	url = "http://api.meaningcloud.com/lang-2.0"
	YOUR_KEY_VALUE = '57217084eb1f8bff5aad4316172ac493'
	YOUR_URL_VALUE = 'YOUR_URL_VALUE'
	YOUR_TXT_VALUE = text
	YOUR_DOC_VALUE = 'YOUR_DOC_VALUE'
	payload = "key="+YOUR_KEY_VALUE+"&txt="+YOUR_TXT_VALUE+"&url="+YOUR_URL_VALUE+"&doc="+YOUR_DOC_VALUE
	headers = {'content-type': 'application/x-www-form-urlencoded'}
	lang_id_response = requests.request("POST", url, data=payload, headers=headers)
	data = json.loads(lang_id_response.text)
	language = data['language_list'][0]['name']
	return language

def file_lang(file):
	url = "http://api.meaningcloud.com/lang-2.0"
	YOUR_KEY_VALUE = '57217084eb1f8bff5aad4316172ac493'
	YOUR_URL_VALUE = 'YOUR_URL_VALUE'
	YOUR_TXT_VALUE = 'YOUR_TXT_VALUE'
	YOUR_DOC_VALUE = file
	payload = "key="+YOUR_KEY_VALUE+"&txt="+YOUR_TXT_VALUE+"&url="+YOUR_URL_VALUE+"&doc="+YOUR_DOC_VALUE
	headers = {'content-type': 'application/x-www-form-urlencoded'}
	lang_id_response = requests.request("POST", url, data=payload, headers=headers)
	data = json.loads(lang_id_response.text)
	language = data['language_list'][0]['name']
	return language

#Index - file upload/text input
@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST' and 'file' in request.files:
		if len(request.files.getlist('file')) > 1:
			languages = []
			for f in request.files.getlist('file'):
				filename = secure_filename(f.filename)
				f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
				x = f.filename 
				languages.append(file_lang(UPLOAD_FOLDER+'/'+x))
			return Response(json.dumps(languages),  mimetype='application/json')
		else:
			for f in request.files.getlist('file'):
				return file_lang(UPLOAD_FOLDER+'/'+f.filename)
	if request.method == 'POST':
		YOUR_TXT_VALUE = request.form['text']
		return text_lang(YOUR_TXT_VALUE)

	return '''
    <!doctype html>
    	<title>Upload File</title>
    	<body>
    		<h2>Upload File And Check Language</h2>
    		<form method=post enctype=multipart/form-data>
      			<p><input type='file' name='file' multiple>
         		<input type='submit' value='Send'>
    		</form>

    		<h2>Find out the language of the text.</h2>
    		<form action="." method="POST">
        		<input type="text" name="text">
        		<input type="submit" name="my-form" value="Send">
    		</form>

    		
		</body>
	</html>
    '''
if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')