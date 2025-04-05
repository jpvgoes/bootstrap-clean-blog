from flask import Flask,render_template,url_for,request
import requests
import smtplib
from email.mime.text import MIMEText

posts_response = requests.get("https://gist.githubusercontent.com/gellowg/389b1e4d6ff8effac71badff67e4d388/raw/fc31e41f8e1a6b713eafb9859f3f7e335939d518/data.json").json()

app = Flask(__name__)

#route to show the home page with all posts
@app.route("/")
def home():
    return render_template("index.html",all_posts=posts_response)

#route to show about page
@app.route('/about')
def about():
    return render_template('about.html')

#route to show the contact form and send email
@app.route('/contact', methods=['POST','GET'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html', sent=False)
    else:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        
        print(name + "\n" + email + "\n" + phone + "\n" + message)
        
        send_email(name,email,phone,message)
    
        return render_template('contact.html', sent=True)
    
#route to show a specific post
@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = None
    for p in posts_response:
        if p['id'] == post_id:
            post = p
            break
    return render_template('post.html', post_content=post)


def send_email(name,email,phone,message):
    
    MY_EMAIL = "YOUR EMAIL"# Replace with your email
    MY_PASSWORD = 'YOUR EMAIL PASSWORD'# Replace with your email password
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(user=MY_EMAIL,password=MY_PASSWORD)
        
        msg = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
        
        mime_msg = MIMEText(msg, "plain", "utf-8")
        mime_msg["Subject"] = "New message from contact form"
        mime_msg["From"] = email
        mime_msg["To"] = MY_EMAIL

        # Enviar email
        server.sendmail(MY_EMAIL, MY_EMAIL, mime_msg.as_string())


if __name__ == "__main__":
    app.run(debug=True)