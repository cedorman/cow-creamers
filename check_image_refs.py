#
# Python script that checks for all the images
#

from html.parser import HTMLParser
from os import listdir
from os.path import isfile, join

list_of_img_refs = []


def get_img_ref_from_attrs(attrs):
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
        if attr[0]== 'src':
            list_of_img_refs.append(attr[1])

        if attr[0] == 'href':
            list_of_img_refs.append(attr[1])


class CowHTMLParser(HTMLParser):
    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag.startswith("img"):
            get_img_ref_from_attrs(attrs)

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass


def get_images_from_dir(dirname, type=None):
    """ This gets all the files in a directory, and optionally limits to
        a particular type of file """
    images = [filename for filename in listdir(dirname) if isfile(join(dirname, filename))]

    if type is not None:
        images = [filename for filename in images if filename.endswith(type)]

    return images


# Get all the html files.
htmlfiles = get_images_from_dir(".", "html")
print( htmlfiles )


# Got through all the html files
for filename in htmlfiles:

    # clear out the list of images
    list_of_img_refs = []

    # Go through the file and get the list of images
    file = open(filename, "r")
    line = file.readline()
    parser = CowHTMLParser()
    while line:
        parser.feed(line)
        line = file.readline()
    file.close()
    print(list_of_img_refs)

    # Get the list of images in the directory
    basename = (filename.split("."))[0]
    print(basename)
    imagesjpg = get_images_from_dir(basename, "jpg")
    imagesjpg.extend(get_images_from_dir(basename, "JPG"))
    if (imagesjpg is not None):
        imagesjpg = [str(basename) + "/" + str(filename) for filename in imagesjpg]
    print(imagesjpg)

    # Compare them.
    refSet = set(list_of_img_refs)
    refSet = refSet.difference(imagesjpg)
    print(" Images in the html that are NOT in the image directory: " + str(refSet))

    imgSet = set(imagesjpg)
    imgSet = imgSet.difference(list_of_img_refs)
    print(" Images in the image directory that are NOT in the html: " + str(imgSet))

