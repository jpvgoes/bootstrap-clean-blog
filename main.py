from flask import Flask,render_template,url_for
import requests

posts_response = requests.get("https://gist.githubusercontent.com/gellowg/389b1e4d6ff8effac71badff67e4d388/raw/fc31e41f8e1a6b713eafb9859f3f7e335939d518/data.json").json()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html",all_posts=posts_response)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = None
    for p in posts_response:
        if p['id'] == post_id:
            post = p
            break
    return render_template('post.html', post_content=post)



if __name__ == "__main__":
    app.run(debug=True)