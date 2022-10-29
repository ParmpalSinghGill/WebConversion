import requests
from flask import Flask,abort,render_template,request,redirect,url_for,send_from_directory
from werkzeug.utils import secure_filename
import os,random,string
from FileConveriosn import M3U8ToMp4,outPutFolder
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER,exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
@app.route('/')
def index():
    filelink=request.args.get("filelink")
    return render_template('Manage.html',filelink=filelink)

def removeDirectory(dir):
    for f in os.listdir(dir):
        os.remove(dir+"/"+f)
    os.rmdir(dir)

@app.route('/Download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory=outPutFolder,path="", filename=filename)


@app.route('/upload',methods = ['GET','POST'])
def upload_file():
    if request.method =='POST':
        files = request.files.getlist('file')
        if files:
            folder="".join(random.choices(string.ascii_letters,k=8))
            folder=request.form.get("filename",folder).replace(" ","_")
            folder=os.path.join(app.config['UPLOAD_FOLDER'],folder)
            if os.path.exists(folder): shutil.rmtree(folder)
            os.makedirs(folder,exist_ok=True)
            for file in files:
                filename = folder+"/"+secure_filename(file.filename.split("/")[-1])
                file.save(filename)
            mp4file=M3U8ToMp4(folder)
            print(mp4file)
            mp4file=request.base_url.replace("upload","")+mp4file
            print(mp4file)
            removeDirectory(folder)
            return redirect(url_for('index')+"?filelink="+mp4file)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run("0.0.0.0",debug = True)
