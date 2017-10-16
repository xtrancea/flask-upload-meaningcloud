# flask-upload-meaningcloud

Setup a flask application on your server. I chose to use python3 for this task.
Check out requirements.txt

# Step 1
sudo apt-get install python3-pip python3-dev nginx

# Step 2
mkdir ~/myproject
cd ~/myproject

# Step 3
pip3 install uwsgi flask

# The application

The web application itself is very straight forward. All you have to do is upload the files of
your choice or input text to see what language the contents are written in. I seem to have come
across a problem, the text gets the right response but file uploads don't end up producing the
correct language, will have to recheck and make a few changes, not much support from meaningcloud
side so its a bit confusing on why it's happening. Anyways if you have any tips let me know.
