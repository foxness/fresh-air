import glob
import datetime
from decimal import *

def pr(a):
    print(repr(a))

def listy(a):
    for b in a:
        print(b)

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
    useless = ['protocol', 'subject', 'toa', 'sc_toa', 'service_center', 'status', 'read', 'locked', 'sub_id', 'type', 'readable_date']

    s = [sms.copy() for sms in smses]
    for sms in s:
        for field in useless:
            sms.pop(field)
    
    return s

def epoch_to_date(epoch):
    if epoch == '0':
        return None

    timestamp = int(epoch) / 1000
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).astimezone()

def parsed_dates(sms):
    sms = sms.copy()

    sms['date'] = epoch_to_date(sms['date'])
    sms['date_sent'] = epoch_to_date(sms['date_sent'])

    return sms

def parse_dates(smses):
    return [parsed_dates(sms) for sms in smses]

# def parse_string_date(date):
#     day, month, year = [int(a) for a in date.split('.')]
#     return {'day': day, 'month': month, 'year': year + 2000}

# def parse_string_time(time):
#     hour, minute = [int(a) for a in time.split(':')]
#     return {'hour': hour, 'minute': minute}

# def get_datetime(date, time):
#     d = parse_string_date(date)
#     t = parse_string_time(time)
#     return datetime.datetime(d['year'], d['month'], d['day'], t['hour'], t['minute'])

def get_transactions(smses):
    transactions = [sms for sms in smses if sms['address'] == '900']
    
    secret = get_secret()
    for t in transactions:
        split = t['body'].split(' ')
        if split[0] == 'VISA' + secret:
            t['visa'] = True
            
            del split[0] # delete visa
            if split[0][2] == '.':
                t['datefirst'] = True

                del split[0] # delete date
            else:
                t['datefirst'] = False
            
            if split[0][0].isdigit():
                t['notime'] = False

                del split[0] # delete time
            else:
                t['notime'] = True

                if split[0] == 'возврат':
                    t['vozvrat'] = True

                    t['type'] = 'возврат'

                    del split[:2]

                    t['amount'] = parse_money(split[0])

                    del split[0]
                    
                    t['balance'] = parse_money(split[-1])

                    del split[-2:]

                    t['service'] = ' '.join(split)
                else:
                    t['vozvrat'] = False

                    service_count = 5 if split[0] == 'оплата' else 4
                    t['service'] = ' '.join(split[:service_count])
                    t['type'] = 'оплата'

                    del split[:service_count]

                    t['amount'] = parse_money(split[0])
                    t['balance'] = parse_money(split[-1])

        else:
            t['visa'] = False

    return transactions

def parse_money(money):
    return Decimal(money[:-1])

def get_secret():
    with open('secret', 'r', encoding = 'utf8') as myfile:
        return myfile.read().strip()

def main():
    fileraw = get_raw_file()
    smses = get_smses(fileraw)
    smses = dictionarify_smses(smses)
    smses = strip(smses)
    smses = parse_dates(smses)
    transactions = get_transactions(smses)

    bodies = [t['body'] for t in transactions if t['visa'] and t['datefirst'] and not t['notime']]
    # frequency_analysis(types)

    listy(bodies[:])

main()