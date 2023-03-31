from flask import Flask, render_template, request, redirect, url_for, send_file
import speech_recognition as sr
import os

#Crete a new instance Flask class
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('./audio.wav', 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')

        return render_template('index.html', request="POST")
    else:
        return render_template("index.html")

#Audio uploader
@app.route('/upload', methods=['POST'])
def upload():
    #requiest the file name
    f = request.files['file']
    #save the audio file
    f.save("./audio.wav")
    print ('Audio file uploaded')
    return render_template('index.html', uploadedName=f.filename)
    #return redirect(url_for('transcribe'))  
    #return 'File uploaded successfully'

@app.route('/download')
def download_file():
    path = "./static/output.txt"   
    return send_file(path, as_attachment=True)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    #create a new recognizer instance
    r = sr.Recognizer()
    #use the audio uploaded as a source
    with sr.AudioFile('./audio.wav') as source:
        audio = r.record(source)
        try:    
            #audio to text    
            text = r.recognize_google(audio)
       # write the text to a file
            with open("./static/output.txt", "w") as file:
                file.write(text)
                os.remove('./audio.wav')            
            return render_template('index.html', text=text)
        
        except sr.UnknownValueError:
            text="Could not understand you. Try Again!"
            os.remove('./audio.wav')  
            return render_template('index.html', text=text)

        except sr.RequestError as e:
            text = "Could not request results from Google Speech Recognition service; {0}".format(e)    
            os.remove('./audio.wav')  
            return render_template('index.html', text=text)
    
if __name__ == '__main__':
    app.run()
#    app.run(debug=True)