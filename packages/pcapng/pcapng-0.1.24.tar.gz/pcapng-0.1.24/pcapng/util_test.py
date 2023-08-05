# Copyright 2017 Brocade Communications Systems, Inc
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import pytest
import struct
import pcapng.util as util
from   pcapng.util import to_bytes, str_to_bytes

def test_block32_pad_len():
    assert 0 == util.block32_ceil_num_bytes(0)

    assert 4 == util.block32_ceil_num_bytes(1)
    assert 4 == util.block32_ceil_num_bytes(2)
    assert 4 == util.block32_ceil_num_bytes(3)
    assert 4 == util.block32_ceil_num_bytes(4)

    assert 8 == util.block32_ceil_num_bytes(5)
    assert 8 == util.block32_ceil_num_bytes(6)
    assert 8 == util.block32_ceil_num_bytes(7)
    assert 8 == util.block32_ceil_num_bytes(8)

def test_pad_to_len():
    with pytest.raises(AssertionError): util.pad_bytes([1, 2, 3, 4], 3)
    with pytest.raises(AssertionError): util.pad_bytes('superlong', 3)

    assert to_bytes( 'superlong' + chr(0)*23 ) == util.pad_bytes('superlong', 32)
    assert to_bytes( [0, 0, 0, 0] ) == util.pad_bytes([          ], 4)
    assert to_bytes( [1, 0, 0, 0] ) == util.pad_bytes([1, ], 4)
    assert to_bytes( [1, 2, 0, 0] ) == util.pad_bytes([1, 2], 4)
    assert to_bytes( [1, 2, 3, 0] ) == util.pad_bytes([1, 2, 3], 4)
    assert to_bytes( [1, 2, 3, 4] ) == util.pad_bytes([1, 2, 3, 4], 4)

    assert to_bytes( [9, 9, 9, 9] ) == util.pad_bytes([          ], 4, 9)
    assert to_bytes( [1, 9, 9, 9] ) == util.pad_bytes([1, ], 4, 9)
    assert to_bytes( [1, 2, 9, 9] ) == util.pad_bytes([1, 2], 4, 9)
    assert to_bytes( [1, 2, 3, 9] ) == util.pad_bytes([1, 2, 3], 4, 9)
    assert to_bytes( [1, 2, 3, 4] ) == util.pad_bytes([1, 2, 3, 4], 4, 9)

def test_pad_to_block32():
    assert to_bytes( [                      ] ) == util.block32_pad_bytes([])
    assert to_bytes( [1, 0, 0, 0            ] ) == util.block32_pad_bytes([1])
    assert to_bytes( [1, 2, 0, 0            ] ) == util.block32_pad_bytes([1, 2])
    assert to_bytes( [1, 2, 3, 0            ] ) == util.block32_pad_bytes([1, 2, 3])
    assert to_bytes( [1, 2, 3, 4            ] ) == util.block32_pad_bytes([1, 2, 3, 4])
    assert to_bytes( [1, 2, 3, 4, 5, 0, 0, 0] ) == util.block32_pad_bytes([1, 2, 3, 4, 5])
    assert to_bytes( [1, 2, 3, 4, 5, 6, 0, 0] ) == util.block32_pad_bytes([1, 2, 3, 4, 5, 6])
    assert to_bytes( [1, 2, 3, 4, 5, 6, 7, 0] ) == util.block32_pad_bytes([1, 2, 3, 4, 5, 6, 7])
    assert to_bytes( [1, 2, 3, 4, 5, 6, 7, 8] ) == util.block32_pad_bytes([1, 2, 3, 4, 5, 6, 7, 8])

    util.assert_block32_length([                      ])
    util.assert_block32_length([1, 2, 3, 4])
    util.assert_block32_length([1, 2, 3, 4, 5, 6, 7, 8])
    with pytest.raises(AssertionError): util.assert_block32_length([1])
    with pytest.raises(AssertionError): util.assert_block32_length([1, 2])
    with pytest.raises(AssertionError): util.assert_block32_length([1, 2, 3])

def test_block32_bytes_pack():
    def assert_block32_bytes_packing( data_bytes ):
        orig = to_bytes( data_bytes )
        extra_bytes = to_bytes('dummy-start') + orig + to_bytes('dummy-end')
        unpacked, remaining = util.block32_lv_bytes_unpack_rolling(
            util.block32_lv_bytes_pack(orig) + extra_bytes )
        assert unpacked  == orig
        assert remaining == extra_bytes
    assert_block32_bytes_packing( '' )
    assert_block32_bytes_packing( 'a' )
    assert_block32_bytes_packing( 'go' )
    assert_block32_bytes_packing( 'ray' )
    assert_block32_bytes_packing( 'Doh!' )
    assert_block32_bytes_packing( 'How do you like me now?' )
    for i in range(23):
        assert_block32_bytes_packing( range(i) )

def test_block32_labelled_bytes_pack():
    block_label = util.curr_time_utc_secs()
    def assert_block32_labelled_bytes_packing( data_bytes ):
        orig = to_bytes( data_bytes )
        extra_bytes = to_bytes('dummy-start') + orig + to_bytes('dummy-end')
        label, unpacked, remaining = util.block32_tlv_bytes_unpack_rolling(
            util.block32_tlv_bytes_pack(block_label, orig) + extra_bytes )
        assert label     == block_label
        assert unpacked  == orig
        assert remaining == extra_bytes
    assert_block32_labelled_bytes_packing( '' )
    assert_block32_labelled_bytes_packing( 'a' )
    assert_block32_labelled_bytes_packing( 'go' )
    assert_block32_labelled_bytes_packing( 'ray' )
    assert_block32_labelled_bytes_packing( 'Doh!' )
    assert_block32_labelled_bytes_packing( 'How do you like me now?' )
    for i in range(13):
        assert_block32_labelled_bytes_packing( range(i) )

#-----------------------------------------------------------------------------

def test_types():
    util.assert_type_str('')
    util.assert_type_str('a')
    util.assert_type_str('abc')

    util.assert_type_list( [] )
    util.assert_type_list( [1] )
    util.assert_type_list( [1,2,3,] )

    util.assert_type_dict( {} )
    util.assert_type_dict( {'a':1} )
    util.assert_type_dict( {'a':1, 'b':2} )

    with pytest.raises(AssertionError): util.assert_type_str( None )
    with pytest.raises(AssertionError): util.assert_type_str( [1] )
    with pytest.raises(AssertionError): util.assert_type_str( {'a':1} )

    with pytest.raises(AssertionError): util.assert_type_list( None )
    with pytest.raises(AssertionError): util.assert_type_list( 'a' )
    with pytest.raises(AssertionError): util.assert_type_list( {'a':1} )

    with pytest.raises(AssertionError): util.assert_type_dict( None )
    with pytest.raises(AssertionError): util.assert_type_dict( 'a' )
    with pytest.raises(AssertionError): util.assert_type_dict( [1] )


def test_uint8():
    for ub in range(256):
        util.assert_uint8(ub)
    with pytest.raises(AssertionError): util.assert_uint8(  -1 )
    with pytest.raises(AssertionError): util.assert_uint8( 256 )

def test_int8():
    for sb in range(-128,127):
        util.assert_int8(sb)
    with pytest.raises(AssertionError): util.assert_int8( -129 )
    with pytest.raises(AssertionError): util.assert_int8(  128 )

def test_bytearray():
    util.assert_type_bytearray( bytearray( [1,2,255] ))
    with pytest.raises(AssertionError): util.assert_type_bytearray( list( [1,2,255] ) )
    with pytest.raises(AssertionError): util.assert_type_bytearray( 'abc' )

def test_to_bytes():
    assert 'abc' == to_bytes( 'abc' )
    assert 'abc' == to_bytes( [97,98,99] )
    if util.is_python2():
        assert str( 'abc' ) == to_bytes( 'abc' )
    if util.is_python3():
        assert bytes( [97,98,99] ) == to_bytes( [97,98,99] )

def test_str_to_bytes():
    assert to_bytes( [97,98,99] ) == str_to_bytes( 'abc' )

def test_fibonacci_list():
    assert util.fibonacci_list(0) ==  []
    assert util.fibonacci_list(1) ==  [0]
    assert util.fibonacci_list(2) ==  [0, 1]
    assert util.fibonacci_list(3) ==  [0, 1, 1]
    assert util.fibonacci_list(4) ==  [0, 1, 1, 2]
    assert util.fibonacci_list(5) ==  [0, 1, 1, 2, 3]      #todo verify test
    assert util.fibonacci_list(6) ==  [0, 1, 1, 2, 3, 5]
    assert util.fibonacci_list(7) ==  [0, 1, 1, 2, 3, 5, 8]
    assert util.fibonacci_list(8) ==  [0, 1, 1, 2, 3, 5, 8, 13]
    assert util.fibonacci_list(9) ==  [0, 1, 1, 2, 3, 5, 8, 13, 21]

#todo need test fibo_list_signed

def test_assert_rel_equal():
    util.assert_rel_equal( 1000, 1001, digits=1 )
    util.assert_rel_equal( 1000, 1001, digits=2 )
    util.assert_rel_equal( 1000, 1001, digits=2.5 )
    with pytest.raises(AssertionError):
        util.assert_rel_equal( 1000, 1001, digits=3.5 )
        util.assert_rel_equal( 1000, 1001, digits=4 )
        util.assert_rel_equal( 1000, 1001, digits=5 )

def test_dict_merge():
    assert { "a":1, 'b':2        } == util.dict_merge(       {'a':1}, {'b':2}            )
    assert { "a":1, 'b':2, 'c':3 } == util.dict_merge_all( [ {'a':1}, {'b':2}, {'c':3} ] )

def test_even_odd():
    assert util.is_even(2)
    assert util.is_even(4)
    assert util.is_even(6)

    assert util.is_odd(3)
    assert util.is_odd(5)
    assert util.is_odd(7)

def test_str_to_intvec():
    assert util.str_to_intvec('123456')     == [12, 34, 56]
    assert util.str_to_intvec('420001')     == [42, 0, 1]
    assert util.str_to_intvec('123456', 3)  == [123, 456]

def test_uint64_split32():
    def assert_round_trip(orig):
        (high32, low32) = util.uint64_split32( orig )
        result = util.uint64_join32(high32, low32)
        assert result == orig
    for x in util.fibonacci_range( pow(2,50) ):
        assert_round_trip(x)


def test_xxx():
    xx1 = struct.pack(   '!hhl', 1, 2, 3 )  # h='short', l='long'
    xx2 = struct.unpack( '!hhl', xx1 )      # ! => network byte order (big-endian)
    assert xx1 == '\x00\x01\x00\x02\x00\x00\x00\x03'
    assert xx2 == ( 1, 2, 3 )
    assert '\x00\x00\x00\x00\x00\x00\x00\x05' == struct.pack( '!q', 5 )
    assert '\x00\x00\x00\x05'                 == struct.pack( '!l', 5 )
    assert '\x00\x05'                         == struct.pack( '!h', 5 )

    assert 3 == len( [ 1, 2, 3] )
    assert (3, 140000) == util.split_float(3.14)
    assert (3, 141593) == util.split_float(3.141592654)

    assert 'abc'             == util.chrList_to_str(['a', 'b', 'c'])

def test_time():
    time_tst = 123.456789
    util.test_time_utc_set( 123.456789 )
    util.assert_rel_equal(time_tst, util.curr_time_utc(), digits=9)
    assert abs(123456789 - util.curr_time_utc_micros()) <= 1
    assert abs(123456 - util.curr_time_utc_millis()) <= 1
    assert abs(123 - util.curr_time_utc_secs()) <= 1

    (secs,usecs) = util.curr_utc_timetuple()
    assert 123    == secs
    assert abs(456789 - usecs) <= 1
    util.test_time_utc_unset()

    util.test_time_utc_set(123456)
    assert '0x0001e240' == util.curr_time_utc_secs_hexstr()
    util.test_time_utc_unset()

def test_quot():
    assert [0,0,0, 1,1,1, 2,2,2] == map( lambda x:util.quot(x,3), range(9) )

def test_mod():
    assert [0,1,2, 0,1,2, 0,1,2] == map( lambda x:util.mod(x,3), range(9) )

def test_take():
    def generate_ints(N):
        for i in range(N):
            yield i
    gen_vals = generate_ints(99)
    lst_vals = [0,1,2,3,4,5,6,7,8,9]
    assert ( [0,1,2,3,4] == util.take( 5, gen_vals )
                         == util.take( 5, lst_vals ))

