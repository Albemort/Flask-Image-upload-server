## Image Upload Web Application Documentation

### Overview

This web application is built using Flask, providing users with the ability to upload images from a web page. The server-side logic manages image processing, storage, and real-time communication with clients through Flask-SocketIO.

### Components

#### Server-Side (Python - Flask)

1. **Flask App Initialization:**
   - The Flask app is initialized, configured with a secret key, and set up with a destination directory for uploaded photos. A maximum file size is also defined.

2. **Static File Serving:**
   - A route is defined to serve uploaded image files, allowing clients to access images via their URLs.

3. **Image Upload Handling:**
   - The server handles image uploads through a dedicated route. Images are received in base64 format, decoded, and stored on the server. The image is then broadcasted to all connected clients using SocketIO.

4. **SocketIO Event Handling:**
   - The server handles the `message` event to print messages received from clients. Additionally, the `img` event broadcasts image filenames to all connected clients.

5. **Web Page Rendering:**
   - The root route renders the client-side HTML page, providing users with an interface to interact with the image upload functionality.

6. **Server Initialization:**
   - The server is initialized with SocketIO using an IPv4 address and port 80, enabling access from other devices on the same network.

#### Client-Side (HTML, JavaScript)

1. **HTML Template:**
   - The client-side HTML file includes an image upload form, success/failure alerts, and a container to display uploaded images.

2. **JavaScript Functions:**
   - JavaScript functions, such as `processFile` and `imageSend`, are defined to handle file input and initiate the image upload process on the client side.

### How to Use

1. Run the Flask server script on the specified IP address and port.
2. Access the web application in a browser at the provided URL.
3. Use the file input to select an image file for upload.
4. Initiate the upload process by clicking the "Upload" button.
5. Receive feedback messages indicating the success or failure of the image upload.

Ensure that the necessary dependencies, such as Flask and Flask-SocketIO, are installed before running the program. Additionally, confirm that the server's IP address and port are configured appropriately for network accessibility.
