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
    
    sms = line[5:-3]
    return sms

def dictionarify_smses(smses):
    return [dictionarify(sms) for sms in smses]

def dictionarify(sms):
    index = 0
    dictionarified = {}
    
    while True:
        eqindex = sms.find('=', index)
        fieldname = sms[index:eqindex]
        quotemark = sms[eqindex + 1]
        quoteindex = sms.find(quotemark, eqindex + 2)
        fieldvalue = sms[eqindex + 2:quoteindex]
        dictionarified[fieldname] = fieldvalue
        index = quoteindex + 2

        if index >= len(sms):
            break
    
    return dictionarified

def frequency_analysis(somelist):
    freq = {}

    for elem in somelist:
        if elem not in freq:
            freq[elem] = 0
        
        freq[elem] += 1
    
    for key in sorted(freq.keys(), key = lambda k: -freq[k]):
        print("{} : {}".format(key, freq[key]))

def main():
    fileraw = get_raw_file()
    smses = get_smses(fileraw)
    smses = dictionarify_smses(smses)

    types = [sms['contact_name'] for sms in smses]
    frequency_analysis(types)
    # print(repr(smses[0]))

    # for s in smses:
    #     if 'toa' not in s:
    #         pr(s)
    #         a = 1

main()