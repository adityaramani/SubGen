import subprocess
def extract_audio (file_path):

    subprocess.run(["ffmpeg", "-i" , file_path ,"-f" ,"mp3","-ab","192000","-vn" ,"../tmp/1.mp3"])
    



