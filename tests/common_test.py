import unittest
import unittest.mock as mock

import MilestoneTrigger.common as common

class TestMakeOrdinal(unittest.TestCase):
    def test_zeros(self):
        assert common.make_ordinal(0) == '0th'
        assert common.make_ordinal(40) == '40th'
        assert common.make_ordinal(110) == '110th' 
        assert common.make_ordinal(2090) == '2090th'

    def test_ones(self):
        assert common.make_ordinal(1) == '1st'
        assert common.make_ordinal(51) == '51st'
        assert common.make_ordinal(101) == '101st'
        assert common.make_ordinal(10001) == '10001st'

    def test_twos(self):
        assert common.make_ordinal(2) == '2nd'
        assert common.make_ordinal(62) == '62nd'
        assert common.make_ordinal(502) == '502nd'
        assert common.make_ordinal(3002) == '3002nd'

    def test_threes(self):
        assert common.make_ordinal(3) == '3rd'
        assert common.make_ordinal(73) == '73rd'
        assert common.make_ordinal(603) == '603rd'
        assert common.make_ordinal(4003) == '4003rd'

    def test_werids(self):
        assert common.make_ordinal(11) == '11th'
        assert common.make_ordinal(12) == '12th'
        assert common.make_ordinal(13) == '13th'
        assert common.make_ordinal(1012) == '1012th'

    def test_highers(self):
        assert common.make_ordinal(104) == '104th'
        assert common.make_ordinal(25) == '25th'
        assert common.make_ordinal(666) == '666th'
        assert common.make_ordinal(87) == '87th'
        assert common.make_ordinal(908) == '908th'
        assert common.make_ordinal(1019) == '1019th'
        
        
if __name__ == 'main':
    unittest.main()