#
# Python script that checks for all the images
#

from html.parser import HTMLParser
from os import listdir, walk
from os.path import isfile, join
import difflib

# List of image references from the html pages
dict_of_img_refs = {}


def get_files_from_dir(dirname, type=None):
    """Get all the files in a directory, optionally limit to a suffix."""
    images = [filename for filename in listdir(dirname) if isfile(join(dirname, filename))]

    if type is not None:
        images = [filename for filename in images if filename.endswith(type)]

    return images

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


def get_img_ref_from_attrs(attrs, filename, line):
    """The attributes of an html tag come in a list.  We want
       either the src or the href. For example, a tag may be:
       <img src="advertising/elsiecopies1r.jpg" alt="elsie copies" width="200">
       attrs is now:
            [('src', 'advertising/elsiecopies1r.jpg'),
             ('alt', 'elsie copies'),
             ('width', '200')]
       And we want the src one.
       """
    for attr in attrs:
        if attr[0] in ['src', 'href']:
            if isImage(attr[1]):
                dict_of_img_refs[attr[1]] = (filename, line)


class CowHTMLParser(HTMLParser):

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def handle_starttag(self, tag, attrs):
        line, offset = self.getpos()
        if tag.startswith("img") or tag.startswith("a"):
            get_img_ref_from_attrs(attrs, filename, line)

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

    def error(self, message):
        pass

# ----------------------------------------------------------------------
# Get list of all image references 
# ----------------------------------------------------------------------
# Get all the html files.
htmlfiles = get_files_from_dir(".", "html")

# Go through all the html files
for filename in htmlfiles:

    # Go through the file and get the list of images, add to dict_of_img_refs
    with open(filename, "r") as file:
        line = file.readline()
        parser = CowHTMLParser(filename)
        while line:
            parser.feed(line)
            line = file.readline()

# Get all html image reference names as a set
refSet = set(dict_of_img_refs.keys())

# ----------------------------------------------------------------------
# Get all the images in all the directories
# ----------------------------------------------------------------------
images = []
for root, dirs, files in walk("."):
    for name in files:
        fullname = join(root, name)[2:]
        if isImage(fullname):
            images.append(fullname)
imageSet = set(images)

# ----------------------------------------------------------------------
# Get diffs
# ----------------------------------------------------------------------
# List all images without a refenence in the html
imgSetWithoutRef = set(imageSet).difference(refSet)
print(f"Images in the image directory that are NOT in the html: {len(imgSetWithoutRef)}")
# for imgWithoutRef in imgSetWithoutRef:
#     print(f"\t{imgWithoutRef}")
# print()

# List all references in html, not in image directories
refSetWithoutImage = sorted(list(set(refSet).difference(imageSet)))
print(f"Images in the html that are NOT in the image directory: {len(refSetWithoutImage)}")
for img in refSetWithoutImage:

    # See if we can find a file with the right suffix
    matches = difflib.get_close_matches(img, imageSet)
    best_match = matches[0] if matches else None
    
    print(f"\t{img:20}  from {dict_of_img_refs[img][0]}:{dict_of_img_refs[img][1]}   Try {best_match}")
