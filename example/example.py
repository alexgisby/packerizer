#
# Example of how to use the Python client library
# with the crushr.json in this directory.
#

from crushr.Client import Client

myClient = Client("./example")
# myClient.serve_compressed(False)

print myClient.css("homepage") # Will output the array of files to display
print myClient.js("homepage") # As will this

print ""
