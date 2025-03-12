from flask import Flask, render_template, send_from_directory
import markdown
import os

app = Flask(__name__)

# Path to the posts directory
POSTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'posts')

# Directory where images are stored
IMAGE_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'posts', 'images')

@app.route('/uploads/img/<filename>')
def get_image(filename):
    # Serve the image from the uploads/img folder
    return send_from_directory(IMAGE_FOLDER, filename)

# Function to read and convert markdown files to HTML
def convert_markdown_to_html(post_filename):
    with open(os.path.join(POSTS_DIR, post_filename), 'r') as file:
        content = file.read()
        html_content = markdown.markdown(content)  # Convert markdown to HTML
    return html_content

# Function to extract title (first line) and preview (first few lines)
def get_post_preview(post_filename):
    post_path = os.path.join(POSTS_DIR, post_filename)
    with open(post_path, 'r') as file:
        lines = file.readlines()
        img = lines[0].strip()
        caption = markdown.markdown(lines[1].strip())
        title = markdown.markdown(lines[2].strip('# ').strip())  # Title is the first line (Markdown heading)
        preview = ' '.join(lines[3:]).strip()  # Get a preview from the next few lines
        preview_html = markdown.markdown(preview)  # Convert preview to HTML
    return img, caption, title, preview_html

@app.route('/')
def index():
    posts = []
    for post_filename in os.listdir(POSTS_DIR):
        if post_filename.endswith('.md'):
            img, caption, title, preview_html = get_post_preview(post_filename)
            posts.append({
                'filename': post_filename,
                'img': img,
                'caption': caption,
                'title': title,
                'preview_html': preview_html
            })
    return render_template('layout.html', posts=posts)

@app.route('/post/<post_filename>')
def show_post(post_filename):
    post_html = convert_markdown_to_html(post_filename)
    return render_template('post.html', post_filename=post_filename, post_html=post_html)

if __name__ == '__main__':
    app.run(debug=True)
