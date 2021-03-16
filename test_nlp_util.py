import nlp_util

def testGC():
    raw_address = 'isn s.h. & rekan, somba opu 76'
    result = nlp_util.genCC(raw_address)
    print(result)
    assert result



def test_get_bio_tagging():
    poi_label = 'isnar, s.h. & rekan'
    raw_address = 'isn s.h. & rekan, somba opu 76'
    result = nlp_util.get_bio_tagging(raw_address,None,poi_label )
    print(result)
    assert result


