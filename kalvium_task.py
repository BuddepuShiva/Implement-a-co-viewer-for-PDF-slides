# -*- coding: utf-8 -*-
"""Kalvium Task.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12ZEpFy9QcQ4yvTmkNEQhzYR6v0J65S3W

##Step 1: Install Required Packages
"""

!pip install flask flask-socketio pyngrok pdfminer.six

"""##Step 2: Configure ngrok with Your Authtoken"""

!ngrok config add-authtoken 2ohlscwY8i3ScWTdWjwffURXGoC_5dkVKAXMieiaZHN16Ax6Z

!pkill ngrok

"""##Step 3: Create the Flask Server"""

import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from pyngrok import ngrok

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Global variable to track the current PDF page
current_page = 1

# Expose the app via ngrok
public_url = ngrok.connect(5001)
print(f"Public URL: {public_url}")

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Admin changing page event
@socketio.on('admin-change-page')
def handle_admin_change_page(page):
    global current_page
    current_page = page
    emit('page-change', page, broadcast=True)

# Viewer changing page event
@socketio.on('viewer-change-page')
def handle_viewer_change_page(page):
    emit('page-change', page, broadcast=True)

# Start the server
def run_server():
    socketio.run(app, port=5000)

"""##Step 4: Create HTML Template for Frontend"""

# Commented out IPython magic to ensure Python compatibility.
# %%writefile templates/index.html
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>PDF Co-Viewer</title>
#     <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.js"></script>
#     <script src="https://mozilla.github.io/pdf.js/build/pdf.js"></script>
#     <style>
#         #pdf-render {
#             border: 1px solid black;
#             width: 80%;
#             height: 500px;
#             margin: 20px auto;
#             overflow: auto;
#         }
#         .controls {
#             text-align: center;
#         }
#         button {
#             padding: 10px;
#             margin: 10px;
#         }
#     </style>
# </head>
# <body>
#     <h1 style="text-align:center;">PDF Co-Viewer</h1>
#     <div id="pdf-render"></div>
#     <div class="controls">
#         <button onclick="changePage(-1)">Previous</button>
#         <span id="page-info">Page 1</span>
#         <button onclick="changePage(1)">Next</button>
#     </div>
# 
#     <script>
#         const socket = io.connect(window.location.origin);
#         let currentPage = 1;
#         const url = 'https://arxiv.org/pdf/1706.03762.pdf'; // Example PDF URL
# 
#         const pdfjsLib = window['pdfjs-dist/build/pdf'];
#         pdfjsLib.GlobalWorkerOptions.workerSrc = '//mozilla.github.io/pdf.js/build/pdf.worker.js';
# 
#         let pdfDoc = null;
# 
#         // Load PDF
#         pdfjsLib.getDocument(url).promise.then(doc => {
#             pdfDoc = doc;
#             renderPage(currentPage);
#         });
# 
#         // Render PDF Page
#         function renderPage(pageNum) {
#             pdfDoc.getPage(pageNum).then(page => {
#                 const viewport = page.getViewport({ scale: 1.5 });
#                 const canvas = document.createElement('canvas');
#                 const ctx = canvas.getContext('2d');
#                 canvas.height = viewport.height;
#                 canvas.width = viewport.width;
# 
#                 const pdfContainer = document.getElementById('pdf-render');
#                 pdfContainer.innerHTML = '';
#                 pdfContainer.appendChild(canvas);
# 
#                 const renderContext = {
#                     canvasContext: ctx,
#                     viewport: viewport
#                 };
#                 page.render(renderContext);
#                 document.getElementById('page-info').textContent = `Page ${pageNum} of ${pdfDoc.numPages}`;
#             });
#         }
# 
#         // Change Page
#         function changePage(offset) {
#             const newPage = currentPage + offset;
#             if (newPage > 0 && newPage <= pdfDoc.numPages) {
#                 currentPage = newPage;
#                 renderPage(currentPage);
#                 socket.emit('admin-change-page', currentPage);
#             }
#         }
# 
#         // Listen for page changes
#         socket.on('page-change', (page) => {
#             currentPage = page;
#             renderPage(page);
#         });
#     </script>
# </body>
# </html>
#

"""##Step 5: Start the Flask Server"""

# Updated run_server function
def run_server():
    socketio.run(app, port=5001, allow_unsafe_werkzeug=True)

# Start the Flask server with SocketIO in a non-blocking way
import threading

server_thread = threading.Thread(target=run_server)
server_thread.start()