import sys
import subprocess

def remove_comments(filename):    
    inputstring = ""
    with open(filename, "r") as f:
        for line in f:
            inputstring = "%s%s" % (inputstring, line)

    awk_cmd = "awk -F';' '{ print $1 }'"
    process = subprocess.Popen(awk_cmd, shell=True,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    out, err = process.communicate(inputstring)
    errcode = process.returncode

    return str(out)

if __name__ == "__main__":

    print remove_comments(sys.argv[1])
    
