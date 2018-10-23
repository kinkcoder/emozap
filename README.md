
## Installation and usage:

Follow the instructions below, then move a webcam capturing application to the top left of the screen, and main.py will take continous screenshots of that corner (640x480), scale the pictures down and send it to the Docker server. It displays the FPS, detected emotion and estimated time until the zap.


```
# Open two terminals

# In the first terminal,
git clone https://gitlab.com/void4/emozap.git
cd emozap
git clone https://gitlab.com/void4/face_classification.git
cd face_classification
# Build the docker image
docker build -t emozap .
# Run the docker image as container, redirect internal 8084 port to external 4000
docker run emozap -p 4000:8084 emozap

# In the second terminal
cd emozap
# Install all required Python libraries
pip install -r requirements.txt
# Run the program
python main.py
```

### Further Docker documentation
https://docs.docker.com/get-started/part2/#build-the-app
