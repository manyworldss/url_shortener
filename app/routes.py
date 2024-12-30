from app import app
from flask import render_template, request, redirect
import string
import random

# Store URL mappings
url_mappings = {}

def generate_short_code():
    """Generate a 6-character random string for short URLs"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form.get('url')
        
        # Basic validation
        if not long_url:
            return render_template('index.html', error="Please enter a URL")
        
        if not long_url.startswith(('http://', 'https://')):
            long_url = 'https://' + long_url
            
        # Generate short code
        short_code = generate_short_code()
        
        # Store the mapping
        url_mappings[short_code] = long_url
        
        # Create the full shortened URL
        short_url = request.host_url + short_code
        
        return render_template('index.html', short_url=short_url)
    
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    """Handle redirection of shortened URLs"""
    long_url = url_mappings.get(short_code)
    
    if long_url:
        return redirect(long_url)
    
    return render_template('index.html', error="URL not found")