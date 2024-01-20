from flask import Flask, render_template, send_from_directory, request
from flask_socketio import SocketIO
import base64
import os

# Globaali Flask-palvelimen ilmentymä, konfiguraatio ja SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
MAX_BUFFER_SIZE = 50 * 1000 * 1000  # Tiedoston max. koko 50 MB
socketio = SocketIO(app, max_http_buffer_size=MAX_BUFFER_SIZE)
# Globaali muuttuja, jolla estetään samannimisten kuvien luonti.
num = 1

# Luo 'uploads' kansio, jos ei ole olemassa.
def create_uploads_folder():
    uploads_folder = 'uploads'
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)
        print("Directory '% s' created" % uploads_folder) 

create_uploads_folder()

# Polku, josta saadaan kuvan osoite (url).
@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

# Polku /upload.
# Tässä käsitellään POST -pyyntö eli kuva, sen tallennus ja vienti
# socketio:n avulla web-sivulle.
@app.route('/upload', methods=['POST'])
def clientside():
    global num
    # POST -pyynnössä otetaan vastaan kuva base64 muodossa, puretaan se
    # ja erotellaan siitä kuva ja sen nimi.
    try:
        data = request.form["data"]
        name = request.form["name"]
        # Tulostetaan palvelimen konsoliin, että kuva on tulossa.
        print(f'incoming image: {name}')
        # Puretaan base64 data.
        imgdata = base64.b64decode(data)
        file = str(name)
        # Tiedoston polku filename.
        filename = f'uploads/{num}{file}'
        num += 1
        with open(filename, 'wb') as f:
            f.write(imgdata)
            f.close()
        # Kuvan lähetys web-sivulle.
        socketio.emit('img', {'result': filename}, broadcast=True)
    except:
        return "Error", 400
    finally:
        return "OK", 200

# Juuripolku sivulle, josta kuvat voi lähettää ja nähdä.
# Renderöidään client.html sivu asiakkaalle.
@app.route('/', methods=['GET'])
def index():
    return render_template("client.html")

# Käsitellään asiakaspuolelta tulevat socketio viestit
# ja tulostetaan ne konsoliin.
@socketio.on('message')
def handle_message(data):
    print('received message: ' + str(data))

# Ohjelman käynnistys. Käytetään IPv4 osoitetta, jotta päästään sivulle
# käsiksi myös muilla laitteilla samassa verkossa, esim. puhelimella.
if __name__ == '__main__':
   socketio.run(app, host="192.168.0.106", port=80)
   