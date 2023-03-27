from flask import Flask, render_template, request, redirect, url_for, g
import speech_recognition as sr
import os

#Crete a new instance Flask class
app = Flask(__name__)

# Home
@app.route('/')
def index():
    status = ' '
    return render_template('index.html', status=status)

@app.route('/record', methods=['POST'])
def record():
    # create a recognizer object
    r = sr.Recognizer()
    # use the default microphone as the audio source
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)        
        audio = r.listen(source)#, timeout=5)
    with open('audio.wav', 'wb') as f:
        f.write(audio.get_wav_data())
    return redirect(url_for('transcribe'))   

#Audio uploader
@app.route('/upload', methods=['POST'])
def upload():
    #requiest the file name
    f = request.files['file']
    #save the audio file
    f.save('audio.wav')
    return redirect(url_for('transcribe'))  
    #return 'File uploaded successfully'

@app.route('/transcribe')
def transcribe():
    #create a new recognizer instance
    r = sr.Recognizer()
    #use the audio uploaded as a source
    with sr.AudioFile('audio.wav') as source:
        audio = r.record(source)
        try:    
            #audio to text    
            text = r.recognize_google(audio)
       # write the text to a file
            with open("output.txt", "w") as file:
                file.write(text)            
            return render_template('index.html', text=text)
        
        except sr.UnknownValueError:
            text="Could not understand you"
            return render_template('index.html', text=text)

        except sr.RequestError as e:
            text = "Could not request results from Google Speech Recognition service; {0}".format(e)    
            return render_template('index.html', text=text)
    
if __name__ == '__main__':
    app.run(debug=True)

