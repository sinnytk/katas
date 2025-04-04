from cell_to_num import cell_to_num

def test_cell_to_num():
    assert(cell_to_num('A')) == 0
    assert(cell_to_num('B')) == 1
    assert(cell_to_num('C')) == 2
    assert(cell_to_num('Z')) == 25

    assert(cell_to_num('AA')) == 26
    assert(cell_to_num('AB')) == 27
    assert(cell_to_num('BA')) == 52
    assert(cell_to_num('BB')) == 53
    assert(cell_to_num('ZA')) == 676
    assert(cell_to_num('ZZ')) == 701

    assert(cell_to_num('AAA')) == 702
    assert(cell_to_num('AAB')) == 703
    assert(cell_to_num('ZZA')) == 18252
    assert(cell_to_num('ZZZ')) == 18277




