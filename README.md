# image-with-text
Displays black and white pictures with Unicode. Currently a small project.

I'm new to github and I realized that I probably shouldn't include the entire lib, so you'll have to make a venv and install PIL manually.

Anyways...
Using unicode, black and white pictures can be displayed through text. Right now it's just black and white, but I'll be adding gray soon. It can also load images (if you add their names to the script). It also includes a web mode, because I coded some of this on online-python.com. Web mode does not use the config file, and it disables image loading. It can be manually enable in the config.

Some bugs include:
* Invalid sizes (as in putting words where numbers should be) will cause an error.
* There is something similar with custom sizes in web mode.
* Images will sometimes not load if the pixel depth is too low, typically 24 works.

Feel free to make pull requests since I really don't know what I'm doing. Also you can just dm me on discord, I'm pretty active on there.
