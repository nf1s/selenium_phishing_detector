import json
jsonFile = open('links.json', 'r')
data = json.load(jsonFile)
jsonFile.close()

link_array = []

for index in data:
    link_array.append(index['url'])

print (len(link_array))
