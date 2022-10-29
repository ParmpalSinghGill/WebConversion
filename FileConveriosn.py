import os
import mimetypes

outPutFolder="static/OUTPUT/"
os.makedirs(outPutFolder,exist_ok=True)

def getTextFile(files):
    for f in files:
        try:
            open(f).read()
            return f
        except:
            pass

def BuildM3U8File(filepath,processedFile="Processed.m3u8"):
    files = [filepath + f for f in os.listdir(filepath)]
    textfile = getTextFile(files)
    # otherfiles = sorted([(int(f.split("/")[-1]), f) for f in files if f != textfile])
    # otherfiles = [f[0] for f in otherfiles]
    print(textfile)
    with open(textfile) as f:
        data = f.readlines()

    processedData = []
    for d in data:
        if "https" in d:
            processedData.append(d.split("/")[-1].split("-")[1] + "\n")
        else:
            processedData.append(d)

    with open(filepath + processedFile, "w") as f:
        f.writelines(processedData)

def makeMp4FileFromM3U8(mp38file,mp4file):
    # ffmpeg -allowed_extensions ALL -i Processed.m3u8 -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 file.mp4
    basecommand="ffmpeg -allowed_extensions ALL -i {} -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 {}"
    command=basecommand.format(mp38file,mp4file)
    os.system(command)

def M3U8ToMp4(filepath):
    if filepath[-1]!="/": filepath+="/"
    BuildM3U8File(filepath,"Processed.m3u8")
    outputfile=outPutFolder+filepath.split("/")[-2]+".mp4"
    makeMp4FileFromM3U8(filepath+"Processed.m3u8",outputfile)
    return outputfile


if __name__ == '__main__':
    filepath="uploads/keNcxkTu"
    M3U8ToMp4(filepath)


