# Transcribe50rs
Transcribe50rs is a tool for easy transcription and simultaneous translation of speech. I designed it in the first place to provide real-time captioning for my course - [CS50 RS](https://youtube.com/playlist?list=PLqmOcP5Wx0OSqo7OI3lEHrAWReshCPdad). Because the course is taught in Ukrainian, potential English-speaking viewers of the live stream would benefit from having English captions.
## The implementation
The idea behind this tool is to have it running on the same computer as [OBS](https://obsproject.com/) and output translation into a file. As OBS supports text overlays with its source being a text file, one can set up a `Text(GDI+)` source in OBS and point it to the created `transcription.txt` file, creating near real-time live stream captioning.
## How to use
After setting up your virtual environment and running `pip install -r requirements.txt`, you can run `transcribe.py`. You will be prompted to select your preferred input mic from the list of available ones, after which the program will create a `transcription.txt` file in its root directory. 
Open OBS and create a new `Text(GDI+)` source in your scene. Check the `Read from file` box and point to your `transcription.txt`. I also recommend checking `Use Custom Text Extends` box so you can set the text to wrap.
