import glob

def pr(a):
    print(repr(a))

def get_raw_file():
    filename = glob.glob('*.xml')[0]

    with open(filename, 'r', encoding = 'utf8') as myfile:
        return myfile.read()

def get_smses(fileraw):
    filelines = fileraw.split('\n')
    smses = [get_sms(line) for line in filelines]
    smses = [a for a in smses if a != None]
    return smses

def get_sms(line):
    line = line.strip()

    if not line.startswith('<sms '):
        return None
    
    line = line[5:-3]
    return line

def main():
    fileraw = get_raw_file()
    smses = get_smses(fileraw)

    print(repr(smses[:3]))

main()