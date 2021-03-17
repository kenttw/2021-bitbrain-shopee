# from nltk.tokenize import wordpunct_tokenize, word_tokenize
# import nltk
# nltk.download('punkt')

import re

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


def get_fuzzy_pairs(sub_text, ner):
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

            score = fuzz.ratio(nt, st)
            if nt.startswith(st):
                score += 20
            # print(st,'===>',score)
            if score > max_score:
                match_st = st
                max_score = score

        r.append((nt, match_st, max_score))

    s_index = -1  # = ner_split.index(r)

    final_result = []
    for i in range(len(r)):
        label, text, score = r[i]

        if score >= 60:
            s_index = sub_text_split.index(text)
            final_result.append(s_index)
            break

    sr = []

    for label, text, score in r:

        if score < 60:
            sr.append((label, None))
        else:
            sr.append((label, text))

    final_result.append(sr)

    return final_result


def get_range_kent(ner, text):
    """


    :param ner: label string 完整的 sting 且先不要經過 tokenizer
    :param text: raw string 完整的 sting 且先不要經過 tokenizer
    :return: 回傳 (start, end) 以 character 單位
    """
    # basic tokenizer
    # ner = prepare_text(ner)
    label = ner
    # text_split = prepare_text(text)

    cc = genCC(text)
    max_score = -1
    target_str = ''
    for ci in cc:
        new_score = fuzz.ratio(label, ci)

        if new_score > max_score:
            max_score = new_score
            target_str = ci
    # try:
    # print(target_str)
    start = text.index(target_str)
    end = start + len(target_str)
    return (start, end)



def find_sub_list(sl,l,exclude=None):
    sll=len(sl)

    if exclude != None:
        for i in range(exclude[0],exclude[1]):
            l[i] = 'XXXXXXXXXXX'

    for ind in (i for i,e in enumerate(l) if e==sl[0]):
        if l[ind:ind+sll]==sl:
            return ind,ind+sll-1


def get_bio_tagging_string(text, street, poi):
    """
    LABELS = ['O', 'B-STREET', 'I-STREET', 'B-POI', 'I-POI']

    :param text: 完整的 sting 且先不要經過 tokenizer
    :param street: training data 中的 street label
    :param poi: training data 中 poi label
    :return: BIO Tagging Sting
    """

    p_start, p_end, s_start, s_end = get_bio_tagging_range(text, street, poi)

    text_splits = prepare_text(text)

    BIO = ["O"] * len(text_splits)
    exclude = None
    if p_start != None:

        p_splits = prepare_text(text[p_start:p_end])

        start,end = find_sub_list(p_splits,text_splits)

        BIO[start] = "B-POI"

        for i in range(start+1,end):
            BIO[i] = "I-POI"

        exclude = (start, end)

    if s_start != None:
        s_splits = prepare_text(text[s_start:s_end])

        start_2,end_2 = find_sub_list(s_splits,text_splits,exclude=exclude)


        if p_start != None:
            set1 = set(range(start, end))
            set2 = set(range(start_2, end_2))

            if len(set1.intersection(set2))!=0 :
                print("Error At:",street,"==>",poi,"==>",text,)
                print(p_start, p_end, s_start, s_end)
                print(start,end,start_2,end_2)
            assert len(set1.intersection(set2))==0

        BIO[start_2] = "B-STREET"

        for i in range(start_2 + 1, end_2):
            BIO[i] = "I-STREET"



    return BIO


def get_bio_tagging_range(text, street, poi):
    """
    取得 stree and poi 在句子中的 range

    :param text:
    :param street:
    :param poi:
    :return:  (poi start, poi end, street start, street end)，以 character 為單位
    """
    if street != None and poi != None:
        # POI first
        p_start, p_end = get_range_kent(poi, text)

        p_len = p_end - p_start

        sub_text_1 = text[0:p_start]
        sub_text_2 = text[p_end:]

        # 判斷在前面還是後面
        if len(sub_text_1) > len(sub_text_2):

            s_start, s_end = get_range_kent(street, sub_text_1)
        else:
            s_start, s_end = get_range_kent(street, sub_text_2)
            s_start += p_end
            s_end += p_end

        return (p_start, p_end, s_start, s_end)
    elif street == None:
        p_start, p_end = get_range_kent(poi, text)
        return (p_start, p_end, None, None)
    elif poi == None:
        s_start, s_end = get_range_kent(street, text)
        return (None, None, s_start, s_end)




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
        for j in range(i + 1, len(ss) + 1):
            # print(ss[i:j])

            temp_str = ss[i]

            for h in range(i + 1, j):
                if ss[h] in """-.,&[]()\"'""":
                    if (temp_str + ss[h]) in raw:
                        temp_str += ss[h]
                    elif (temp_str + " " + ss[h]) in raw:
                        temp_str += " " + ss[h]
                else:
                    if temp_str + " " + ss[h] in raw:
                        temp_str = temp_str + " " + ss[h]
                    else:
                        temp_str = temp_str + ss[h]
            cc.append(temp_str)

            # cc.append( " ".join(ss[i:j]))
    return cc
