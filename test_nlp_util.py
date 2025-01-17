import nlp_util

def testGC():
    raw_address = 'isn s.h. & rekan, somba opu 76'
    result = nlp_util.genCC(raw_address)
    print(result)
    assert result


def test_getPair():
    # label, raw = "hanief sembilan mtr -h", "kuripan hanief semb mtr -h, gajah mada, 58112"
    # print(getPair(label, raw))

    raw = " ".join(['a', 'b', 'c', 'd'])
    label = " ".join(['ba', '-', 'cc'])
    assert nlp_util.get_fuzzy_pairs(raw, label) == [1, [('ba', 'b'), ('-', None), ('cc', 'c')]]

    raw = " ".join(['b', '-', 'c', 'd'])
    label = " ".join(['ba', 'cc'])
    assert nlp_util.get_fuzzy_pairs(raw, label) == [0, [('ba', 'b'), ('cc', 'c')]]

    raw = ['a', 'b', 'c', 'd']
    label = ['ba', 'cc']
    assert nlp_util.get_fuzzy_pairs(raw, label) == [1, [('ba', 'b'), ('cc', 'c')]]


def test_get_range_kent():

    label,raw = "hanief sembilan mtr -h", "kuripan hanief semb mtr -h, gajah mada, 58112"
    result = nlp_util.get_range_kent(label,raw)
    print(result)
    assert raw[result[0]:result[1]] == 'hanief semb mtr -h'

def test_get_bio_tagging_range():
    print("")
    # case 1:
    poi,street,raw = "toko bb kids", "raya samb gede", "xxx raya. sa-mb gede, 299 toko bb k&ids yyy",
    p_start,p_end,s_start,s_end = nlp_util.get_bio_tagging_range(raw,street,poi)
    print("case1")
    print("POI==>", raw[p_start:p_end])
    assert raw[p_start:p_end] == 'toko bb k&ids'
    print("Street==>", raw[s_start:s_end])
    assert raw[s_start:s_end] =='raya. sa-mb gede'

    # case 2:
    poi,street,raw = "toko bb kids", "raya samb gede", " toko bb kids, raya samb gede, 299",
    p_start,p_end,s_start,s_end = nlp_util.get_bio_tagging_range(raw,street,poi)
    print("case2")
    print("POI==>", raw[p_start:p_end])
    print("Street==>", raw[s_start:s_end])


    # case 3:
    poi,street,raw = "toko bb kids", "raya samb gede", "aaa toko bb kids, raya samb gede, 299",
    p_start,p_end,s_start,s_end = nlp_util.get_bio_tagging_range(raw,street,poi)
    print("case3")
    print("POI==>", raw[p_start:p_end])
    print("Street==>", raw[s_start:s_end])


    poi,street,raw = "tahu jontor bung tomo ", "bung tomo",  "tahu jon bung tomo bung tomo, sungai keledang samarinda seberang"
    p_start,p_end,s_start,s_end = nlp_util.get_bio_tagging_range(raw,street,poi)
    print("case4")
    print("POI==>", raw[p_start:p_end])
    print("Street==>", raw[s_start:s_end])

    poi,street,raw = '',"citra yuda iv  peru depok", "raya. sa-mb gede, 299 toko bb k&ids yyy"
    p_start,p_end,s_start,s_end = nlp_util.get_bio_tagging_range(raw,street,poi)
    print("case5")
    print("POI==>", raw[p_start:p_end])
    print("Street==>", raw[s_start:s_end])


    print("")
    # case 6:
    poi,street,raw = "toko bb kids", "raya samb gede", "xxx raya. sa-mb gede, 299 toko bb k&ids yyy",
    p_start,p_end,s_start,s_end = nlp_util.get_bio_tagging_range(raw,street,'')
    print("case6")
    assert  p_start == None

    print("Street==>", raw[s_start:s_end])
    assert raw[s_start:s_end] =='raya. sa-mb gede'

    print("")
    # case 7:
    poi,street,raw = "toko bb kids", "raya samb gede", "xxx raya. sa-mb gede, 299 toko bb k&ids yyy",
    p_start,p_end,s_start,s_end = nlp_util.get_bio_tagging_range(raw,'',poi)
    print("case7")
    print("POI==>", raw[p_start:p_end])
    assert raw[p_start:p_end] == 'toko bb k&ids'

    assert s_start==None


    poi, street, raw = 'sd neg 12 anggrek', '', 'sd negeri 12 anggrek'
    p_start,p_end,s_start,s_end = nlp_util.get_bio_tagging_range(raw,street,poi)
    print("case8")
    print("POI==>", raw[p_start:p_end])
    # print("Street==>", raw[s_start:s_end])
    assert s_start == None

def test_get_bio_tagging_string():
    print("")
    # case 1:
    poi, street, raw = "toko bb kids", "raya samb gede", "xxx raya. sa-mb gede, 299 toko bb k&ids yyy",
    BIO = nlp_util.get_bio_tagging_string(raw, street, poi)
    print(BIO)


    print("")
    poi,street,raw = None,"citra yuda iv  peru depok", "raya. sa-mb gede, 299 toko bb k&ids yyy"
    BIO = nlp_util.get_bio_tagging_string(raw, street, poi)
    print(BIO)

    poi,street,raw = "lapangan futsal sukaluyu", "tang", "xxx raya. sa-mb gede, 299 toko bb k&ids yyy"
    BIO = nlp_util.get_bio_tagging_string(raw, street, poi)
    print(BIO)


    poi,street,raw = "lapangan futsal sukaluyu", "tang", "xxx raya. sa-mb gede, 299 toko bb k&ids yyy"
    BIO = nlp_util.get_bio_tagging_string(raw, None, poi)
    print(BIO)

    poi,street,raw = "lapangan futsal sukaluyu", "tang", "xxx raya. sa-mb gede, 299 toko bb k&ids yyy"
    BIO = nlp_util.get_bio_tagging_string(raw, None, None)
    print(BIO)

def test_find_sub_list():
    print("")
    poi,street,raw = "tahu jontor bung tomo ", "bung tomo",  "tahu jon bung tomo bung tomo, sungai keledang samarinda seberang"
    p_start, p_end, s_start, s_end = nlp_util.get_bio_tagging_range(raw, street, poi)

    text_splits = nlp_util.prepare_text(raw) #['tahu', 'jon', 'bung', 'tomo', 'bung', 'tomo', ',', 'sungai', 'keledang', 'samarinda', 'seberang']
    p_splits = nlp_util.prepare_text(raw[p_start:p_end])
    start, end = nlp_util.find_sub_list(p_splits, text_splits)

    s_splits = nlp_util.prepare_text(raw[s_start:s_end])

    start_2, end_2 = nlp_util.find_sub_list(s_splits, text_splits, (start,end))

    set1 = set(range(start, end))
    set2 = set(range(start_2, end_2))
    print(start,end,start_2,end_2)

    assert len(set1.intersection(set2))==0