from flask import Flask, render_template, send_from_directory
from flask_frozen import Freezer
from flask_flatpages import FlatPages
import re


import markdown
import os

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FREEZER_RELATIVE_URLS = DEBUG


app = Flask(__name__)

freezer = Freezer(app)
app.config.from_object(__name__)
pages = FlatPages(app)


# Path to the posts directory
POSTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'posts')
FASH_POSTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'posts', 'fashion')
FT_POSTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'posts', 'feature')


# Directory where images are stored
IMAGE_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'posts', 'images')


def get_post(post_filename, DIR):
    post_path = os.path.join(DIR, post_filename)
    with open(post_path, 'r') as file:
        lines = file.readlines()
        img = post_filename.strip(".md")
        url = markdown.markdown(lines[0].strip())
        url = re.sub(r'<.*?>', '', url)  # This will remove any HTML tags
        caption = markdown.markdown(lines[1].strip())
        title = markdown.markdown(lines[2].strip('# ').strip())  # Title is the first line (Markdown heading)
        preview = ' '.join(lines[3:]).strip()  # Get a preview from the next few lines
        preview_html = markdown.markdown(preview)  # Convert preview to HTML
    return img, url, caption, title, preview_html

def get_misc_post(post_filename, DIR):
    post_path = os.path.join(DIR, post_filename)
    with open(post_path, 'r') as file:
        lines = file.readlines()
        img = post_filename.strip(".md")
        url = markdown.markdown(lines[0].strip())
        url = re.sub(r'<.*?>', '', url)  # This will remove any HTML tags
        caption = markdown.markdown(lines[1].strip())
        title = markdown.markdown(lines[2].strip('# ').strip())  # Title is the first line (Markdown heading)
        preview = ' '.join(lines[3:]).strip()  # Get a preview from the next few lines
        preview_html = markdown.markdown(preview)  # Convert preview to HTML
    return img, url, caption, title, preview_html

def get_fashion_post(post_filename, DIR):
    post_path = os.path.join(DIR, post_filename)
    with open(post_path, 'r') as file:
        lines = file.readlines()
        img = post_filename.strip(".md")
        url = markdown.markdown(lines[0].strip())
        url = re.sub(r'<.*?>', '', url)  # This will remove any HTML tags
        caption = markdown.markdown(lines[1].strip())
        title = markdown.markdown(lines[2].strip('# ').strip())  # Title is the first line (Markdown heading)
        subtitle = markdown.markdown(lines[3].strip())
        preview = ' '.join(lines[4:]).strip()  # Get a preview from the next few lines
        preview_html = markdown.markdown(preview)  # Convert preview to HTML
    return img, url, caption, title, preview_html, subtitle

def load_posts(directory, file_extension=".md"):
    posts = []
    for post_filename in os.listdir(directory):
        if post_filename.endswith(file_extension):
            img, url, caption, title, preview_html, subtitle = get_fashion_post(post_filename, directory)
            img = post_filename.strip(file_extension)
            img += ".jpg"
            posts.append({
                'filename': post_filename,                
                'img': img,
                'url': url,
                'subtitle': subtitle,
                'caption': caption,
                'title': title,
                'preview_html': preview_html
            })
    return posts

def show_post(post_filename, directory):
    post = {}
    if post_filename.endswith('.md'):
        # Get post preview data (img, caption, title, preview_html)
        img, url, caption, title, preview_html = get_post(post_filename, directory)
        
        # Remove the .md extension from filename and append .jpg
        img = post_filename.removesuffix(".md") + ".jpg"
        
        # Assign the data to the post dictionary
        post = {
            'filename': post_filename,
            'img': img,
            'url': url,
            'caption': caption,
            'title': title,
            'preview_html': preview_html
        }

    # Render the post to the template
    return post

@app.route('/uploads/img/<filename>/')
def get_image(filename):
    # Serve the image from the uploads/img folder
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/art/')
def art():
    posts = load_posts(POSTS_DIR)  # Use the helper function to load posts from the directory
    return render_template('posts.html', posts=posts, header_text="ART LISTINGS",
        subheader_text="Things you should see: the latest thrilling art and design shows, curated by me.",
        publication="The Grand Tourist")

@app.route('/art/post/<post_filename>/')
def artpost(post_filename):
    post = show_post(post_filename, POSTS_DIR)
    return render_template('post.html', post_filename=post_filename, post=post, header_text="ART LISTINGS")

@app.route('/fashion/')
def fashion():
    posts = load_posts(FASH_POSTS_DIR)  # Use the helper function to load posts from the directory
    return render_template('posts.html', posts=posts, header_text="FASHION NEWS",
        subheader_text="New collections, collaborations, and more.",
        publication="10 Magazine USA")

@app.route('/fashion/post/<post_filename>/')
def fashpost(post_filename):
    post = show_post(post_filename, FASH_POSTS_DIR)
    return render_template('post.html', post_filename=post_filename, post=post, header_text="FASHION NEWS")

@app.route('/misc/')
def misc():
    posts = load_posts(FT_POSTS_DIR)  # Use the helper function to load posts from the directory
    return render_template('posts.html', posts=posts, header_text="MORE FROM ME",
        subheader_text="Everything that isn’t art and fashion: British dogs, the world's best martini, etc.",
        publication="The Grand Tourist")

@app.route('/misc/post/<post_filename>/')
def miscpost(post_filename):
    post = show_post(post_filename, FT_POSTS_DIR)
    return render_template('post.html', post_filename=post_filename, post=post, header_text="MORE FROM ME")

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
    freezer.freeze()

