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
import pcapng.linktype
import pcapng.block
import pcapng.option
import pcapng.mrt
import pcapng.util
from   pcapng.util import to_bytes, str_to_bytes


def test_mrt_block():
    pcapng.util.test_time_utc_set(123.456789)
    blk_bytes = pcapng.mrt.mrt_block_pack(2, 3, range(1, 6))
    blk_dict  = pcapng.mrt.mrt_block_unpack(blk_bytes)
    pcapng.util.assert_type_bytes(  blk_bytes )
    pcapng.util.assert_type_dict( blk_dict )
    assert blk_dict[ 'time_secs'    ] == 123
    assert blk_dict[ 'mrt_type'     ] == 2
    assert blk_dict[ 'mrt_subtype'  ] == 3
    assert blk_dict[ 'content'      ] == to_bytes( [1, 2, 3, 4, 5] )
    pcapng.util.test_time_utc_unset()

def test_mrt_block_ext():
    pcapng.util.test_time_utc_set(123.456789)
    blk_bytes = pcapng.mrt.mrt_block_extended_pack(4, 5, range(1, 8))
    blk_dict  = pcapng.mrt.mrt_block_extended_unpack(blk_bytes)
    pcapng.util.assert_type_bytes(  blk_bytes )
    pcapng.util.assert_type_dict( blk_dict )
    assert blk_dict[ 'time_secs'    ] == 123
    assert blk_dict[ 'time_usecs'   ] == 456789
    assert blk_dict[ 'mrt_type'     ] == 4
    assert blk_dict[ 'mrt_subtype'  ] == 5
    assert blk_dict[ 'content'      ] == to_bytes( [1, 2, 3, 4, 5, 6, 7] )
    pcapng.util.test_time_utc_unset()

def test_isis_block():
    pcapng.util.test_time_utc_set(123.456789)
    blk_bytes = pcapng.mrt.mrt_isis_block_pack( range(1, 6))
    blk_dict  = pcapng.mrt.mrt_isis_block_unpack(blk_bytes)
    assert blk_dict[ 'time_secs'    ] == 123
    assert blk_dict[ 'mrt_type'     ] == pcapng.mrt.ISIS
    assert blk_dict[ 'mrt_subtype'  ] == 0
    assert blk_dict[ 'content'      ] == to_bytes( [1, 2, 3, 4, 5] )
    pcapng.util.test_time_utc_unset()

def test_isis_block_ext():
    pcapng.util.test_time_utc_set(123.456789)
    blk_bytes = pcapng.mrt.mrt_isis_block_extended_pack( range(1, 8))
    blk_dict  = pcapng.mrt.mrt_isis_block_extended_unpack(blk_bytes)
    assert blk_dict[ 'time_secs'    ] == 123
    assert blk_dict[ 'time_usecs'   ] == 456789
    assert blk_dict[ 'mrt_type'     ] == pcapng.mrt.ISIS_ET
    assert blk_dict[ 'mrt_subtype'  ] == 0
    assert blk_dict[ 'content'      ] == to_bytes( [1, 2, 3, 4, 5, 6, 7] )
    pcapng.util.test_time_utc_unset()


