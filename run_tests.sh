unixname="$(uname -s)"

if [ "${unixname:0:5}" == "MINGW" ]; then
    python -m unittest discover . "*_test.py"
else
    python3 -m unittest discover . "*_test.py"
fi
