import glob
import datetime

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

def strip(smses):
    useless = ['protocol', 'subject', 'toa', 'sc_toa', 'service_center', 'status', 'read', 'locked', 'sub_id', 'type']

    s = [sms.copy() for sms in smses]
    for sms in s:
        for field in useless:
            sms.pop(field)
    
    return s

def get_transactions(smses):
    transactions = [sms for sms in smses if sms['address'] == '900']
    return transactions

def epoch_to_date(epoch):
    timestamp = int(epoch) / 1000
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).astimezone()

def parsed_dates(sms):
    sms = sms.copy()

    sms['date'] = epoch_to_date(sms['date'])
    sms['date_sent'] = epoch_to_date(sms['date_sent'])

    return sms

def parse_dates(smses):
    return [parsed_dates(sms) for sms in smses]

def main():
    fileraw = get_raw_file()
    smses = get_smses(fileraw)
    smses = dictionarify_smses(smses)
    smses = strip(smses)
    # smses = parse_dates(smses)
    # transactions = get_transactions(smses)

    # types = [sms['locked'] for sms in smses]
    # frequency_analysis(types)

    # pr(transactions[:2])

main()