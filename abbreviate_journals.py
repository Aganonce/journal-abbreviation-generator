# Author: James Flamino (2021)

import string
import spacy
import re
import sys
import yaml

nlp = spacy.load('en_core_web_sm')
missing_abbrevs = []
missing_journals = []

with open("abbreviations/abbrevs.yml", "r") as stream:
    try:
        abbrev_map = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        sys.exit()

def contains_number(value):
    for character in value:
        if character.isdigit():
            return True
    return False

def abbreviate_journal(res):
    if res.lower() == 'plos one':
        return 1

    if res.lower() == 'science':
        return 1

    if res.lower() == 'nature':
        return 1

    if 'arxiv' in res.lower():
        return 1

    for i in res:
        if i in '!"#$%\'()*,-./;<=>?@[]^_`{|}~':
            return 0

    if res.lower() == 'proceedings of the national academy of sciences':
        return 'Proc. Natl. Acad. Sci. U.S.A.'
    
    res = re.sub(r'[^\w\s]','',res)
    res = res.replace('&', '').replace('\\', '')
    doc = nlp(res)

    token_list = []
    for token in doc:
        if token.pos_ != 'ADP' and token.pos_ != 'DET' and token.pos_ != 'CCONJ' and token.pos_ != 'PRON':
            token_list.append(token.text)

    final_list = []
    for token in token_list:
        token_cap = token.capitalize()
        if len(token) > 1:
            if token_cap in abbrev_map:
                token = abbrev_map[token_cap]
            else:
                if not contains_number(token):
                    missing_abbrevs.append(token.capitalize())
            final_list.append(token)
        else:
            if token.isalnum():
                final_list.append(token)

    output = ' '.join(final_list)
    output = output.strip()

    return output

if __name__ == '__main__':
    # PARAMETERS
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    else:
        print('ERROR: This program requires one command line argument: fname')
        sys.exit()

    fname_list = fname.split('.')
    oname = '.'.join(fname_list[:-1]) + '_abbrev.' + fname_list[-1]
    print('\033[1mSaving abbreviated file to:\033[0m', oname)

    w = open(oname, 'w')
    with open(fname, 'r') as ins:
        for line in ins:
            line = line.rstrip('\n')
            line = line.strip()
            if 'title' in line and 'journal' in line:
                res = re.findall(r'journal=\{.*?\}', line)[0]
                res = res.replace('journal={', '').replace('}', '')
                abbrev_res = abbreviate_journal(res)
                if abbrev_res != 0 and abbrev_res != 1:
                    line = line.replace(res, abbrev_res)
                    w.write(line + '\n')
                else:
                    if abbrev_res == 0:
                        w.write(line + '\n')
                        missing_journals.append(res)
                    elif abbrev_res == 1:
                        w.write(line + '\n')

            else:
                if line[:7] == 'journal' or line[:9] == 'booktitle':
                    if '{' in line and '}' in line:
                        res = re.findall(r'\{.*?\}', line)[0]
                        res = res.replace('{', '').replace('}', '')
                    elif '"' in line:
                        res = re.findall(r'"([^"]*)"', line)[0]
                        res = res.replace('"', '')
                    abbrev_res = abbreviate_journal(res)
                    if abbrev_res != 0 and abbrev_res != 1:
                        if line[:7] == 'journal':
                            w.write('  journal={' + abbrev_res + '},\n')
                        elif line[:9] == 'booktitle':
                            w.write('  booktitle={' + abbrev_res + '},\n')
                    else:
                        if abbrev_res == 0:
                            w.write('  ' + line + '\n')
                            missing_journals.append(res)
                        elif abbrev_res == 1:
                            w.write('  ' + line + '\n')
                else:
                    if len(line) > 0:
                        if line[0] == '@' or line[0] == '}':
                            w.write(line + '\n')
                        else:
                            w.write('  ' + line + '\n')
                    else:
                        w.write('\n')
    w.close()

    print('===================================================')
    print('\033[1mWords that do not have abbreviations (update YAML):\033[0m')
    missing_abbrevs = set(missing_abbrevs)
    for item in missing_abbrevs:
        print(item)
    print('===================================================')
    print('\033[1mJournals that could not be properly abbreviated:\033[0m')
    missing_journals = set(missing_journals)
    for item in missing_journals:
        period_count = item.count('.')
        if period_count > 1:
            has_other_punctuation = False
            new_item = item.replace('.', '')
            for i in new_item:
                if i in string.punctuation:
                    has_other_punctuation = True
            if not has_other_punctuation:
                print(item, '\033[1m(This journal may already be abbreviated.)\033[0m')
            else:
                print(item)
        else:
            print(item)
    print('===================================================')