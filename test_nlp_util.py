import nlp_util

def testGC():
    raw_address = 'isn s.h. & rekan, somba opu 76'
    result = nlp_util.genCC(raw_address)
    print(result)
    assert result

def test_get_range_kent():


def test_get_bio_tagging():
    poi_label = 'isnar, s.h. & rekan'
    raw_address = 'isn s.h. & rekan, somba opu 76'
    result = nlp_util.get_bio_tagging(raw_address,None,poi_label )
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