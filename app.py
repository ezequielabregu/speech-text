from flask import Flask, render_template, request, redirect, url_for, send_file, session
import speech_recognition as sr
import os
import multiprocessing

#Crete a new instance Flask class
app = Flask(__name__)
app.secret_key = 'your_secret_key'

long_running_process = None
result = None

server_path = ""#"/var/www/html/apps/speech_text/"
audio_path = server_path + "audio.wav"
text_path = server_path + "output.txt"

selected_option = [""]

@app.route('/submit-option', methods=['POST'])
def submit_option():
    data = request.get_json()
    global selected_option
    selected = (data['selectedOption'])
    selected_option[0] = selected
    session["selected"] = "69"
    print(selected_option[0])
    # Do something with the selected option
    return 'selected_option'

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        f = request.files['audio_data']
        with open(audio_path, 'wb') as audio:
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
    f.save(audio_path)
    print ('Audio file uploaded')
    return render_template('index.html', uploadedName=f.filename)
    #return redirect(url_for('transcribe'))  
    #return 'File uploaded successfully'

@app.route('/download')
def download_file():
    path = text_path   
    return send_file(path, as_attachment=True)

@app.route('/start-process')
def start_process():
    global long_running_process
    long_running_process = multiprocessing.Process(target=transcribe, args=(selected_option))
    long_running_process.start()
    return redirect(url_for('processing'))

@app.route('/processing')
def processing():
    return render_template('processing.html')

@app.route('/result')
def result():
    with open(text_path, 'r', encoding='utf-8') as file:
        text = file.read()
        return render_template('result.html', text=text)

@app.route('/transcribe')
def check_process():
    global long_running_process
    # Check if the long-running task has completed
    if long_running_process and long_running_process.is_alive():
        return "processing"
    else:
        return "completed"

def transcribe(selected_option):
    #print ("selected option" + str(selected_option))
    #create a new recognizer instance
    r = sr.Recognizer()
    #use the audio uploaded as a source
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
        try: 
            #audio to text    
            text = r.recognize_google(audio, language=str(selected_option))#, language=dropdown())
       # write the text to a file
            with open(text_path, "w", encoding='utf-8') as file:
                file.write(text)
                os.remove(audio_path)            
            return True
            #return render_template('index.html', text=text)
        
        except sr.UnknownValueError:
            text="Could not understand you. Try Again!"
            os.remove(audio_path)  
            return False
            #return render_template('index.html', text=text)

        except sr.RequestError as e:
            text = "Could not request results; {0}".format(e)    
            os.remove(audio_path)  
            return False
            #return render_template('index.html', text=text)



if __name__ == '__main__':
#    app.run(host="0.0.0.0", port=5000)
#    app.run()
    app.run(debug=True)