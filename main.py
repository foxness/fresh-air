import glob

filename = glob.glob('*.xml')[0]

with open(filename, 'r', encoding = 'utf8') as myfile:
    fileraw = myfile.read()

print(fileraw[:50])