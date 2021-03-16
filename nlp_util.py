from nltk.tokenize import wordpunct_tokenize, word_tokenize
import nltk
import re
nltk.download('punkt')

# from transformers import BertTokenizer
# MODEL_NAME = 'indobenchmark/indobert-large-p1'
# tokenizer_bert = BertTokenizer.from_pretrained(MODEL_NAME)

# isnar, s.h. & rekan ===> isn s.h. & rekan, somba opu 76
poi_label = 'isnar, s.h. & rekan'
raw_address = 'isn s.h. & rekan, somba opu 76'


from fuzzywuzzy import fuzz

def prepare_text(text):
    text = re.sub(r'([a-z0-9]+)', r' \1 ', text)
    text = text.strip()
    text = re.split('\s+', text)
    return text


def get_fuzzy_pairs(sub_text,ner):

    if type(sub_text) == list:
        sub_text_split = sub_text
        ner_split = ner
    else:

        ner_split = prepare_text(ner)
        sub_text_split = prepare_text(sub_text)
    r = []
    for nt in ner_split:
        # print(nt,end=' ')
        max_score = -1
        match_st = ''
        for st in sub_text_split:

            score = fuzz.ratio(nt,st)
            if nt.startswith(st):
                score += 20
            # print(st,'===>',score)
            if score > max_score:
                match_st = st
                max_score = score


        r.append((nt,match_st,max_score))

    s_index = -1 #= ner_split.index(r)

    final_result = []
    for i in range(len(r)):
        label,text, score = r[i]

        if score > 60:
            s_index = sub_text_split.index(text)
            final_result.append(s_index)
            break

    sr = []

    for label, text, score in r:


        if score < 60 :
            sr.append((label,None))
        else:
            sr.append((label,text))

    final_result.append(sr)


    return final_result


def _get_range_kent(ner,text):
    # basic tokenizer
    # ner = prepare_text(ner)
    label = ner
    text_split = prepare_text(text)


    cc = genCC(text_split,text)
    max_score = -1
    target_str = ''
    for ci in cc:
        new_score = fuzz.ratio(label, ci)

        if new_score > max_score :
            max_score = new_score
            target_str = ci
    # try:
    print(target_str)
    start = raw.index(target_str)
    end = start + len(target_str)
    return (start,end)





def _get_range(ner, text):
    history = []
    for idx in range(len(text) - len(ner) + 1):
        score = 0

        pointer = idx
        for l in ner:
            if l.startswith(text[pointer]):
                pointer += 1
                score += 1

        start = idx
        end = pointer
        if score == len(ner):
            return (start, end)

        history.append((score, start, end))

    if not history:
        start = 0
        end = len(text)
        return (start, end)
    _, start, end = sorted(history)[-1]
    return (start, end)

def get_bio_tagging(text, street, poi):
    len_text = len(text)
    bio = ['O'] * len_text

    pairs = []
    if street is not None:
        pairs.append((street, 'STREET'))
    if poi is not None:
        pairs.append((poi, 'POI'))

    for ner, name in pairs:
        if ner is not None:
            len_ner = len(ner)
            for i in range(len_text - len_ner + 1):
                start, end = _get_range(ner, text)

                bio[start] = f'B-{name}'
                for j in range(start + 1, end):
                    bio[j] = f'I-{name}'

    return bio


def genCC(raw):
    # ss = word_tokenize(raw_address,)
    # ss = wordpunct_tokenize(raw_address)
    # ss = tokenizer_bert.tokenize(raw_address)
    # ss = raw_address.split(" ")
    ss = prepare_text(raw)
    # becasue ss have been tokenized
    cc = []
    # print(ss)
    for i in range(len(ss)):
        for j in range(i+1,len(ss)+1):
            # print(ss[i:j])

            temp_str = ss[i]

            for h in range(i+1,j):
                if ss[h] in """-.,&[]()\"'""":
                    if (temp_str + ss[h]) in raw : temp_str+= ss[h]
                    elif (temp_str + " " + ss[h]) in raw : temp_str+= " "+ss[h]
                else:
                    if temp_str + " " + ss[h] in raw : temp_str = temp_str + " " + ss[h]
                    else: temp_str = temp_str + ss[h]
            cc.append(temp_str)

            # cc.append( " ".join(ss[i:j]))
    return cc



# label,raw = "hanief sembilan mtr -h", "kuripan hanief semb mtr -h, gajah mada, 58112"
# print(get_fuzzy_pairs(label,raw))
#
#
# raw = " ".join(['a', 'b', 'c', 'd'])
# label = " ".join(['ba', '-', 'cc'])
# print(get_fuzzy_pairs(label,raw))




# # cahaya lestari toko ===> kra raya, no b 88 cahaya lest toko, rw 5 kramat
# raw = 'kra raya, no b 88 cahaya lest toko, rw 5 kramat'
# label = 'cahaya lestari toko'
# print(_get_range(ner=label, text=raw))
# print(_get_range_kent(ner=label, text=raw))
#
#
# label,raw = "plot ab tour & travel", "plot ab tour & tra brawi, kasihan"
# print(_get_range(ner=label, text=raw))
# print(_get_range_kent(ner=label, text=raw))
#
#
#
# label,raw = "hanief sembilan mtr -h", "kuripan hanief semb mtr -h, gajah mada, 58112"
# print(_get_range(ner=label, text=raw))
# print(_get_range_kent(ner=label, text=raw))