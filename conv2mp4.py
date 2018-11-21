import subprocess
import os.path
import shlex

def run():

    # completed_video= os.path.join(save_path, filename)
    filename = os.path.join('media', 'charliedetected')
    # filename = 'media/charliedetected'

    #Conversion to usable file format
    print("Converting to mp4")
    from subprocess import CalledProcessError
    command = shlex.split("MP4Box -add {f}.h264 {f}.mp4".format(f=filename))
    output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    print("Completed conv2mp4.py")
    # print(output)

    #delete recorded files
    # os.remove(filename+'.h264')
