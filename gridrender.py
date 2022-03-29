width = 50
height = 50
spaceBetweenPixels = 1

webMode = False
from os import system
try:
    from PIL import Image
except:
    print("PIL import failed, this is probably because the venv is not active!")
    input("press enter to continue in web mode")
    webMode = True

if(not webMode):
    #read from config file
    configLines = []
    configFile = open("config.txt", "r")
    addToConfigLines = ""
    addToConfigLines = configFile.read()
    configLines = addToConfigLines.split("\n")
    configFile.close()
    for line in configLines:
        if(line.split(" ")[0] == "forceWebMode"):
            if(line.split(" ")[-1] == "true"):
                webMode = True
                break
        if(line.split(" ")[0] == "Width"):
            width = int(line.split(" ")[-1])
        if(line.split(" ")[0] == "Height"):
            height = int(line.split(" ")[-1])
        if(line.split(" ")[0] == "PixelSpace"):
            spaceBetweenPixels = int(line.split(" ")[-1])

if (not webMode):
    imageNameList = ["no", "chesyon", "crimbo", "sample"]
    imageList = [r"no.png", r"chesyon.png", r"crimbo.png", r"sample.png"]
    
    def getRListForImage(image):
        #loads image and get a list of rgb values for each pixel
        pix_val = list(image.getdata())
        pix_val_flat = [x for sets in pix_val for x in sets]
        #filters list to only include every 1 of 3, which would be just the R value, which is all we need to tell if it's black or white
        pixelCounter = 0
        pixelResettingCounter = 0
        pixelsToRemove = []
        for pixel in pix_val_flat:
            if pixelResettingCounter != 0:
                pixelsToRemove.append(pixelCounter)
            pixelResettingCounter += 1
            if pixelResettingCounter == 3:
                pixelResettingCounter = 0
            pixelCounter += 1
        pixelsToRemove.reverse()
        for num in pixelsToRemove:
            del pix_val_flat[num]
        #sets any r value greater than 0 to 1, so the list should now only consist of 1's and 0s, kinda like binary actually
        for R in pix_val_flat:
            if R > 0:
                R = 1
        return pix_val_flat
    #load config below here


def clear():
    if webMode == False:
        system('cls')
    
grid = []

def gridInit(width, height):
    global grid
    grid = []
    widthCounter = 0
    heightCounter = 0
    while heightCounter != height:
        grid += [["b"]]
        heightCounter += 1
    for row in grid:
        widthCounter = 0
        while widthCounter != width:
            row += u"\u25A1"
            widthCounter += 1
        row += "\n"
        row.remove("b")

#while not in web mode, there will probably be a config file, which will have an option for custom size
if(webMode):
    if(input("type 'custom' for custom size, type anything else for default size").lower() == "custom"):
        width = int(input("width: "))
        height = int(input("height: "))
        spaceBetweenPixels = int(input("# of spaces between pixels: "))

gridInit(width, height)

# function to make sure end of row is still a new line indicator, row[-1] means the end of the current row
def refreshRowEnd():
    for row in grid:
        row[-1] = "\n"

#function to toggle the pixel at the selected coordinate on or off        
def setSinglePixel(x, y, on):
    try:
        if on:
            grid[y][x] = u"\u25A0"
        else:
            grid[y][x] = u"\u25A1"
    except:
        return ValueError("setSinglePixel failed")

# function that runs setSinglePixel for multiple coordinate pairs, currently unused
def setMultiplePixes(coordinates, on):
    for coord in coordinates:
        setSinglePixel([coord[0]], coord[1], on)

# runs setSinglePixel for all pixels in grid        
def setAllPixels(fillOrClear):
    currentRow = 0
    for row in grid:
        currentPixel = 0
        for pixel in row:
            setSinglePixel(currentPixel, currentRow, fillOrClear)
            currentPixel += 1
        currentRow += 1

# displays the current grid        
def render():
    refreshRowEnd()
    gridToRender = " " * spaceBetweenPixels
    for row in grid:
        for entry in row:
            gridToRender += entry
            gridToRender += " " * spaceBetweenPixels
    print(gridToRender)

clear()

if(not webMode):
#i don't feel like commenting each part of this, it's 12:30 am
    def loadImageIntoGrid(imageToUse):
        global grid
        currentPixel = 0
        currentPixelNoReset = 0
        currentRow = 0
        img = Image.open(imageToUse)
        ImgWidth, ImgHeight = img.size
        ImgPixelList = getRListForImage(img)
        if(height != ImgHeight):
            raise ValueError("image size does not match grid size! grid size: " + str(width) + "*" + str(height) + " image size: " + str(ImgWidth) + "*" + str(ImgHeight))
        if(width != ImgWidth):
            raise ValueError("image size does not match grid size! grid size: " + str(width) + "*" + str(height) + " image size: " + str(ImgWidth) + "*" + str(ImgHeight))
        for row in grid:
            currentPixel = 0
            for pixel in row:
                if pixel == "\n":
                    continue
                if ImgPixelList[currentPixelNoReset] > 0:
                    grid[currentRow][currentPixel] = u"\u25A0"
                else:
                    grid[currentRow][currentPixel] = u"\u25A1"
                currentPixel += 1
                currentPixelNoReset += 1
            currentRow += 1
    

clear()
while True:
    render()
    #ask user what they would like to do
    choice = input().lower()
    #pretty self explanatory
    if choice == "reset":
        clear()
        setAllPixels(False)
    elif choice == "fill":
        clear()
        setAllPixels(True)
    #literally just crashes the program because that way i don't have to re-enter the venv
    elif choice == "leave":
        raise ValueError("see you later!")
    #load an image from the image list at the top
    elif choice.split()[0] == "load":
        try:
            clear()
            if choice.split()[1] == "list":
                print(imageNameList)
                print("please pick an image from the list")
            elif choice.split()[1] in imageNameList:
                print("loaded " + choice.split()[1])
                loadImageIntoGrid(imageList[imageNameList.index(choice.split()[1])])
            else:
                print("invalid image, please use 'load list' for a list of images")
        except:
            clear()
            if(not webMode):
                print("invalid load input!")
            else:
                print("image loading does not work in web mode")
    elif choice == "init":
        gridInit(width, height)
    elif choice == "help":
        clear()
        print("welcome to chesyon's basic grid rendering system")
        print("help: display this")
        print("reset: set grid to every pixel off")
        print("fill: set grid to every pixel on")
        print("x y: toggle pixel power at selected coordinates")
        print("load list: display a list of images to load")
        print("load imgName: load the image by name")
        print("leave: produces an error, allows for easy program restart")
    elif True:
        #check if a coordinate pair was provided, return to input if not
        clear()
        try:
            tryVar = choice.split()[1]
        except:
            print("not enough info!")
            continue
        #if a on or off was included in the input, set the pixel to that state
        try:
            if choice.split()[2] == "off":
                choicePower = False
            elif choice.split()[2] == "on":
                choicePower = True
        # if a on or off was not specified, change the state of the pixel to the opposite of it's current state        
        except:
            try:
                if grid[int(choice.split()[1])][int(choice.split()[0])] == u"\u25A1":
                    choicePower = True
                if grid[int(choice.split()[1])][int(choice.split()[0])] == u"\u25A0":
                    choicePower = False
            #should only occur if coords are wrong
            except:
                print("invalid coords")
                continue
        #actually changes the pixel
        finally:
            setSinglePixel(int(choice.split()[0]), int(choice.split()[1]), choicePower)
