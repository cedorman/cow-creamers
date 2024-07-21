#
# Python script that checks for all the images
#

from html.parser import HTMLParser
from os import listdir, walk
from os.path import isfile, join

# List of image references from the html pages
# list_of_img_refs = []
list_of_img_refs = {}


def isImage(imgref):
    """ Determine if a string is an image, which in our case means that
    it ends with jpg, JPG, png, or gif """
    if (imgref.endswith("JPG")):
        return True
    if (imgref.endswith("jpg")):
        return True
    if (imgref.endswith("gif")):
        return True
    if (imgref.endswith("png")):
        return True
    return False


def get_img_ref_from_attrs(attrs, filename):
    """ the attributes of an html tag come in a list.  We want
        either the src or the href. For example, a tag may be:
        <img src="advertising/elsiecopies1r.jpg" alt="elsie copies" width="200">
        attrs is now:
             [('src', 'advertising/elsiecopies1r.jpg'),
              ('alt', 'elsie copies'),
              ('width', '200')]
        And we want the src one.
        """

    for attr in attrs:
        if attr[0] == 'src':
            if isImage(attr[1]):
                list_of_img_refs[attr[1]] = filename

        if attr[0] == 'href':
            if isImage(attr[1]):
                list_of_img_refs[attr[1]] = filename


class CowHTMLParser(HTMLParser):

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def handle_starttag(self, tag, attrs):
        if tag.startswith("img"):
            get_img_ref_from_attrs(attrs, filename)

        if tag.startswith("a"):
            get_img_ref_from_attrs(attrs, filename)

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

    def error(self, message):
        pass


def get_files_from_dir(dirname, type=None):
    """ This gets all the files in a directory, and optionally limits to
        a particular type of file """
    images = [filename for filename in listdir(dirname) if isfile(join(dirname, filename))]

    if type is not None:
        images = [filename for filename in images if filename.endswith(type)]

    return images


# Get all the html files.
htmlfiles = get_files_from_dir(".", "html")


# Go through all the html files
for filename in htmlfiles:

    # Go through the file and get the list of images, will get added to list_of_img_refs.  
    file = open(filename, "r")
    line = file.readline()
    parser = CowHTMLParser(filename)
    while line:
        parser.feed(line)
        line = file.readline()
    file.close()

# Turn the list into a set, which will remove all repeats
refSet = set(list_of_img_refs.keys())
# print(" All image refences from HTML files: "+ str(len(refSet)))
# print(refSet)
# print()

# Go through all the images in all the directories
images = []
for root, dirs, files in walk("."):
    for name in files:
        fullname = join(root, name)[2:]
        # print("file " + join(root, name) + "   " + fullname)
        if isImage(fullname):
            images.append(fullname)

imageSet = set(images)
# print(" All image from all directories : " + str(len(imageSet)))

# Compare them.
imgSetCopy = set(imageSet)
imgSetCopy = imgSetCopy.difference(refSet)
print(" Images in the image directory that are NOT in the html: " + str(len(imgSetCopy)))
print(str(imgSetCopy))
print()

refSetCopy = set(refSet)
refSetAsList = list(refSetCopy.difference(imageSet))
refSetAsList.sort()
print(" Images in the html that are NOT in the image directory: " + str(len(refSetAsList)))
print(str(refSetAsList))
for img in refSetAsList:
    print(f"\t{img:20}  from {list_of_img_refs[img]}")
print()
