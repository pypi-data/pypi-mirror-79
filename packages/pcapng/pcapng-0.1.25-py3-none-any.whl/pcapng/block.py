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
"""Serialize & deserialze PCAPNG blocks.

See:  https://pcapng.github.io/pcapng/
"""

#todo add header docstring to all

from __future__ import print_function

import struct

import pcapng
import pcapng.linktype          as linktype
import pcapng.mrt               as mrt
import pcapng.option            as option
import pcapng.pen
import pcapng.util              as util
from   pcapng.util              import to_bytes

#todo think about how to handle a block of packets
#todo look at "docopt" usage -> cmdopts processing

#todo add docstrings for all classes
#todo add docstrings for all constructurs
#todo add docstrings for all methods

#-----------------------------------------------------------------------------
util.assert_python2()    #todo make work for python 2.7 or 3.3 ?
#-----------------------------------------------------------------------------

BYTE_ORDER_MAGIC    = 0x1A2B3C4D

CUSTOM_MRT_ISIS_BLOCK_OPT = option.CustomStringCopyable( pcapng.pen.BROCADE_PEN, 'EMBEDDED_MRT_ISIS_BLOCK')

#todo read must find mandatory SHB at beginning
    #todo global byte-order starts off undefined; is reset by each SHB
    #todo read_*_block must detect & handle any endian data (per SHB)
#todo need generic read_block(raw bytes) method
#todo need generic read_next_block(file_ptr) method
    #todo read_block_hdr(file_ptr),  block_hdr_unpack
    #todo read_block_body(file_ptr), block_body_unpack
#todo must skip any unrecognized blocks version: (major,minor) > current
#todo convert read result to object

#-----------------------------------------------------------------------------

#todo maybe create a SectionBlock object with SHB, IDB, options, EPBs, SPBs, etc ?

def strip_header( packed_bytes ): #todo use for all unpack()
    "Utility function to strip Block type_code & total_len from packed bytes, returning all three. "
    util.assert_block32_length( packed_bytes )
    (type_code, total_len, byte_order_magic_found) = struct.unpack('=LLL', packed_bytes[:12])
    #todo if SHB:
    #todo   parse BOM-found;  set global endian;  re-parse fields, verify OK
    assert total_len <= len(packed_bytes)
    stripped_bytes = packed_bytes[8:]
    return (type_code, total_len, stripped_bytes)

class Block:
    "Superclass for all PCAPNG blocks"
    BLOCK_UNKNOWN = 9999

    def __init__(self, type_code, content):
        self.type_code    = type_code
        self.content = content

    def to_map(self):           return util.select_keys(self.__dict__, ['type_code'] )
    def __repr__(self):         return str( self.to_map() )
    def __eq__(self, other):    return self.to_map() == other.to_map()
    def __ne__(self, other):    return (not __eq__(self,other))

class SectionHeaderBlock:
    "Serialize & deserialze a PCAPNG Section Header Block"
    SPEC_CODE = 0x0A0D0D0A
    MAJOR_VERSION   = 1
    MINOR_VERSION   = 0
    block_head_encoding = '=LLLHHq'     #todo need determine endian on read
    block_tail_encoding = '=L'          #todo need determine endian on read

    UNPACK_DISPATCH_TABLE = util.dict_merge_all( [
        option.Comment.dispatch_entry(),
        option.CustomStringCopyable.dispatch_entry(),
        option.CustomBinaryCopyable.dispatch_entry(),
        option.CustomStringNonCopyable.dispatch_entry(),
        option.CustomBinaryNonCopyable.dispatch_entry(),
        option.ShbHardware.dispatch_entry(),
        option.ShbOs.dispatch_entry(),
        option.ShbUserAppl.dispatch_entry()
    ] )

    @staticmethod
    def is_shb_option(obj):
        "Internal method to validate legal SHB options"
        result = (  isinstance(obj, option.Comment) |
                    isinstance(obj, option.CustomOption) |
                    isinstance(obj, option.ShbOption) )
        return result

    def __init__(self, options_lst=[]):
        "Creates an SHB object with the specified options"
        for opt in options_lst:
            assert self.is_shb_option(opt)
        self.options_lst = options_lst

    def to_map(self):
        "Converts an SHB object to a map representation"
        base_map = {    'SPEC_CODE':            self.SPEC_CODE,
                        'SHB_MAJOR_VERSION':    self.MAJOR_VERSION,
                        'SHB_MINOR_VERSION':    self.MINOR_VERSION, }
        result = util.dict_merge( base_map, util.select_keys(self.__dict__, ['options_lst']) )
        return result
    def __repr__(self):         return str( self.to_map() )
    def __eq__(self, other):    return self.to_map() == other.to_map()
    def __ne__(self, other):    return (not __eq__(self,other))

    @staticmethod
    def dispatch_entry(): return { SectionHeaderBlock.SPEC_CODE : SectionHeaderBlock.unpack }

    def pack(self):    #todo data_len
        "Serialize a SHB object into packed bytes"
        options_bytes     = option.pack_all(self.options_lst)
        section_len       = -1        #todo unused at present; must pre-accum all blocks if want to use

        block_total_len  = ( 4 +      # block type
                             4 +      # block total length
                             4 +      # byte order magic
                             2 + 2 +  # major version + minor version
                             8 +      # section length
                             len(options_bytes) +
                             4 )      # block total length
        packed_bytes = ( struct.pack( self.block_head_encoding, self.SPEC_CODE, block_total_len,
                                     BYTE_ORDER_MAGIC, self.MAJOR_VERSION, self.MINOR_VERSION, section_len) +
                         options_bytes +
                         struct.pack( self.block_tail_encoding, block_total_len ))
        return packed_bytes

    @staticmethod
    def unpack(block_bytes):      #todo verify block type & all fields
        "Deserialize a SHB object from packed bytes"
        util.assert_type_bytes(block_bytes)
        ( block_type, block_total_len, byte_order_magic, major_version, minor_version,
                section_len ) = struct.unpack( SectionHeaderBlock.block_head_encoding, block_bytes[:24] )
        (block_total_len_end,) = struct.unpack( SectionHeaderBlock.block_tail_encoding, block_bytes[-4:])
        assert block_type       == SectionHeaderBlock.SPEC_CODE
        assert byte_order_magic == BYTE_ORDER_MAGIC
        assert major_version    == SectionHeaderBlock.MAJOR_VERSION
        assert minor_version    == SectionHeaderBlock.MINOR_VERSION
        assert block_total_len  == block_total_len_end == len(block_bytes)
        # section_len currently ignored
        options_bytes = block_bytes[24:-4]
        options_lst = option.unpack_all(SectionHeaderBlock.UNPACK_DISPATCH_TABLE, options_bytes)
        result_obj = SectionHeaderBlock(options_lst)
        return result_obj

class InterfaceDescBlock:
    "Serialize & deserialze a PCAPNG Interface Description Block"
    SPEC_CODE = 0x01
    block_head_encoding = '=LLHHL'
    block_tail_encoding = '=L'

    UNPACK_DISPATCH_TABLE = util.dict_merge_all( [
        option.Comment.dispatch_entry(),
        option.CustomStringCopyable.dispatch_entry(),
        option.CustomBinaryCopyable.dispatch_entry(),
        option.CustomStringNonCopyable.dispatch_entry(),
        option.CustomBinaryNonCopyable.dispatch_entry(),
        option.IdbName.dispatch_entry(),
        option.IdbDescription.dispatch_entry(),
        option.IdbIpv4Addr.dispatch_entry(),
        option.IdbIpv6Addr.dispatch_entry(),
        option.IdbMacAddr.dispatch_entry(),
        option.IdbEuiAddr.dispatch_entry(),
        option.IdbSpeed.dispatch_entry(),
        option.IdbTsResol.dispatch_entry(),
        option.IdbTZone.dispatch_entry(),
        option.IdbFilter.dispatch_entry(),
        option.IdbOs.dispatch_entry(),
        option.IdbFcsLen.dispatch_entry(),
        option.IdbTsOffset.dispatch_entry(),
    ] )

    @staticmethod
    def is_idb_option(obj):
        "Internal method to validate legal IDB options"
        result = (  isinstance(obj, option.Comment) |
                    isinstance(obj, option.CustomOption) |
                    isinstance(obj, option.IdbOption) )
        return result

    def __init__(self, link_type=linktype.LINKTYPE_ETHERNET, #todo temp testing default
                 options_lst=[]):
        "Creates an IDB object with the specified options"
        #todo need test valid linktype
        for opt in options_lst:
            assert self.is_idb_option(opt)
        self.options_lst    = options_lst
        self.link_type      = link_type
        self.reserved       = 0    # spec req zeros
        self.snaplen        = 0    # 0 => no limit

    def to_map(self):
        "Converts an IDB object to a map representation"
        return util.select_keys(self.__dict__, ['link_type', 'options_lst', 'snaplen' ])
    def __repr__(self):         return str( self.to_map() )
    def __eq__(self, other):    return self.to_map() == other.to_map()
    def __ne__(self, other):    return (not __eq__(self,other))

    @staticmethod
    def dispatch_entry(): return { InterfaceDescBlock.SPEC_CODE : InterfaceDescBlock.unpack }

    def pack(self):
        "Serialize a IDB object into packed bytes"
        options_bytes   = option.pack_all( self.options_lst )
        util.assert_type_bytes( options_bytes )
        util.assert_block32_length( options_bytes )
        block_total_len =   (  4 +         # block type
                               4 +         # block total length
                               2 + 2 +     # linktype + reserved
                               4 +         # snaplen
                               len(options_bytes) +
                               4 )         # block total length
        packed_bytes = ( struct.pack( self.block_head_encoding, self.SPEC_CODE,
                                      block_total_len, self.link_type, self.reserved, self.snaplen) +
                         options_bytes +
                         struct.pack( self.block_tail_encoding, block_total_len ))
        return packed_bytes

    @staticmethod
    def unpack(block_bytes):      #todo verify block type & all fields
        "Deserialize a IDB object from packed bytes"
        util.assert_type_bytes(block_bytes)
        ( block_type, block_total_len, link_type, reserved, snaplen ) = struct.unpack( InterfaceDescBlock.block_head_encoding,
                                                                                       block_bytes[:16] )
        (block_total_len_end,) = struct.unpack( InterfaceDescBlock.block_tail_encoding, block_bytes[-4:] )
        assert block_type       == InterfaceDescBlock.SPEC_CODE
        assert block_total_len  == block_total_len_end == len(block_bytes)
        assert reserved         == 0
        assert snaplen          == 0
        options_bytes = block_bytes[16:-4]
        options_lst = option.unpack_all(InterfaceDescBlock.UNPACK_DISPATCH_TABLE, options_bytes)
        result_obj = InterfaceDescBlock( link_type, options_lst )
        return result_obj

class SimplePacketBlock:
    "Serialize & deserialze a PCAPNG Simple Packet Block"
    SPEC_CODE = 0x03
    head_encoding = '=LLL'
    tail_encoding = '=L'

    def __init__(self, pkt_data):
        "Creates an SPB object"
        self.pkt_data = to_bytes(pkt_data)        #todo is list & tuple & str ok?

    def to_map(self):
        "Converts an SPB object to a map representation"
        return util.select_keys(self.__dict__, ['pkt_data'] )
    def __repr__(self):         return str( self.to_map() )
    def __eq__(self, other):    return self.to_map() == other.to_map()
    def __ne__(self, other):    return (not __eq__(self,other))

    @staticmethod
    def dispatch_entry(): return { SimplePacketBlock.SPEC_CODE : SimplePacketBlock.unpack }

    def pack(self):
        "Serialize an SPB object into packed bytes"
        pkt_data_pad     = util.block32_pad_bytes(self.pkt_data)
        original_pkt_len = len(self.pkt_data)
        pkt_data_pad_len = len(pkt_data_pad)
        block_total_len = ( 4 +      # block type
                            4 +      # block total length
                            4 +      # original packet length
                            pkt_data_pad_len +
                            4 )      # block total length
        block_bytes = (struct.pack(self.head_encoding, self.SPEC_CODE, block_total_len, original_pkt_len) +
                       pkt_data_pad +
                       struct.pack(self.tail_encoding, block_total_len))
        return block_bytes

    @staticmethod
    def unpack(block_bytes):      #todo verify block type & all fields
        "Deserialize an SPB object from packed bytes"
        util.assert_type_bytes(block_bytes)
        (block_type, block_total_len, original_pkt_len) = struct.unpack( SimplePacketBlock.head_encoding, block_bytes[:12] )
        (block_total_len_end,) = struct.unpack( SimplePacketBlock.tail_encoding, block_bytes[-4:] )
        assert block_type       == SimplePacketBlock.SPEC_CODE
        assert block_total_len  == block_total_len_end == len( block_bytes )
        pkt_data    = block_bytes[12 : (12 + original_pkt_len)]
        result_obj  = SimplePacketBlock( pkt_data )
        return result_obj

class EnhancedPacketBlock:
    "Serialize & deserialze a PCAPNG Enhanced Packet Block"
    SPEC_CODE = 0x06
    head_encoding = '=LLLLLLL'
    tail_encoding = '=L'

    UNPACK_DISPATCH_TABLE = util.dict_merge_all( [
        option.Comment.dispatch_entry(),
        option.CustomStringCopyable.dispatch_entry(),
        option.CustomBinaryCopyable.dispatch_entry(),
        option.CustomStringNonCopyable.dispatch_entry(),
        option.CustomBinaryNonCopyable.dispatch_entry(),
        option.EpbFlags.dispatch_entry(),
        option.EpbHash.dispatch_entry(),
        option.EpbDropCount.dispatch_entry()
    ] )

    @staticmethod
    def is_epb_option(obj):
        "Internal method to validate legal EPB options"
        result = (  isinstance(obj, option.Comment) |
                    isinstance(obj, option.CustomOption) |
                    isinstance(obj, option.EpbOption) )
        return result

    def __init__(self, interface_id, pkt_data_captured, pkt_data_orig_len=None, options_lst=[],
                        timestamp=None ):
        """Creates an EPB object. If 'timestamp' is not supplied, uses the current UTC time in the
        default format (uint64 microseconds since unix epoch). User-supplied timestamp must also be
        in this format unless IDB options uses option.IdbTsResol to specify alternate."""
        util.assert_uint32( interface_id )  #todo verify args in all fns
        pkt_data_captured = to_bytes( pkt_data_captured )        #todo is list & tuple & str ok?
        if pkt_data_orig_len is None:
            pkt_data_orig_len = len(pkt_data_captured)
        else:
            util.assert_uint32(pkt_data_orig_len)
            assert len(pkt_data_captured) <= pkt_data_orig_len
        util.assert_type_list( options_lst )   #todo check type on all fns
        for opt in options_lst:
            assert self.is_epb_option(opt)
        if timestamp is None:
            time_utc_micros = util.curr_time_utc_micros()
        else:
            time_utc_micros = timestamp

        self.interface_id       = interface_id
        self.pkt_data_captured  = pkt_data_captured
        self.pkt_data_orig_len  = pkt_data_orig_len
        self.options_lst        = options_lst
        self.time_utc_micros    = time_utc_micros

    def to_map(self):
        "Converts an EPB object to a map representation"
        return util.select_keys( self.__dict__, [
            'interface_id', 'pkt_data_captured', 'pkt_data_orig_len', 'options_lst',
            'time_utc_micros' ] )

    def __repr__(self):         return str( self.to_map() )
    def __eq__(self, other):    return self.to_map() == other.to_map()
    def __ne__(self, other):    return (not __eq__(self,other))

    @staticmethod
    def dispatch_entry(): return { EnhancedPacketBlock.SPEC_CODE : EnhancedPacketBlock.unpack }

    def pack(self):
        "Serialize an EPB object into packed bytes"
        #todo make all arg validation look like this (in order, at top)
        pkt_data_pad                = util.block32_pad_bytes(self.pkt_data_captured)
        pkt_data_captured_len       = len(self.pkt_data_captured)
        pkt_data_captured_pad_len   = len(pkt_data_pad)
        options_bytes               = option.pack_all(self.options_lst)
        block_total_len = ( 4 +      # block type
                            4 +      # block total length
                            4 +      # interface id
                            4 +      # timestamp - high
                            4 +      # timestamp - low
                            4 +      # captured packet length
                            4 +      # original packet length
                            pkt_data_captured_pad_len +
                            len(options_bytes) +
                            4 )      # block total length
        (timestamp_high, timestamp_low) = util.uint64_split32( self.time_utc_micros )
        packed_bytes = (struct.pack( self.head_encoding, self.SPEC_CODE, block_total_len, self.interface_id,
                                     timestamp_high, timestamp_low, pkt_data_captured_len,
                                     self.pkt_data_orig_len) +
                        pkt_data_pad +
                        options_bytes +
                        struct.pack( self.tail_encoding, block_total_len ))
        return packed_bytes

    @staticmethod
    def unpack(packed_bytes):
        "Deserialize an EPB object from packed bytes"
        util.assert_type_bytes(packed_bytes)
        (block_type, block_total_len, interface_id, timestamp_high, timestamp_low,
                pkt_data_captured_len, pkt_data_orig_len) = struct.unpack( EnhancedPacketBlock.head_encoding, packed_bytes[:28] )
        (block_total_len_end,) = struct.unpack( EnhancedPacketBlock.tail_encoding, packed_bytes[-4:])
        time_utc_micros = util.uint64_join32( timestamp_high, timestamp_low )
        assert block_type           == EnhancedPacketBlock.SPEC_CODE      #todo verify block type & all fields, all fns
        assert block_total_len      == block_total_len_end == len(packed_bytes)
        assert pkt_data_captured_len <= pkt_data_orig_len

        pkt_data_captured_pad_len   = util.block32_ceil_num_bytes(pkt_data_captured_len)
        block_bytes_stripped        = packed_bytes[28:-4]
        pkt_data                    = block_bytes_stripped[:pkt_data_captured_len]
        options_bytes               = block_bytes_stripped[pkt_data_captured_pad_len:]
        options_lst                 = option.unpack_all( EnhancedPacketBlock.UNPACK_DISPATCH_TABLE, options_bytes )
        result_obj                  = EnhancedPacketBlock( interface_id, pkt_data, pkt_data_orig_len, options_lst,
                                                           timestamp=time_utc_micros  )
        return result_obj

# custom format really needs a content_length field!
#todo make subclasses like options:  CustomBlockCopyable CustomBlockNonCopyable
class CustomBlock:
    "Serialize & deserialze a PCAPNG Custom Block"
    head_encoding = '=LLL'
    tail_encoding = '=L'

    UNPACK_DISPATCH_TABLE = util.dict_merge_all( [
        option.Comment.dispatch_entry(),
        option.CustomStringCopyable.dispatch_entry(),
        option.CustomBinaryCopyable.dispatch_entry(),
        option.CustomStringNonCopyable.dispatch_entry(),
        option.CustomBinaryNonCopyable.dispatch_entry()
    ] )

    @staticmethod
    def is_custom_block_option(obj):
        "Internal method to validate legal custom block options"
        result = (  isinstance(obj, option.Comment) |
                    isinstance(obj, option.CustomOption) )
        return result

    def __init__(self, block_type, pen_val, content, options_lst=[] ):
        "Creates a Custom Block object"
        pcapng.pen.assert_valid_pen( pen_val )
        for opt in options_lst:
            assert self.is_custom_block_option(opt)
        self.block_type     = block_type
        self.pen_val        = pen_val
        self.content        = content
        self.options_lst    = options_lst

    #todo define these for all blocks
    def to_map(self):
        "Converts a CB object to a map representation"
        return util.select_keys(self.__dict__, ['block_type', 'pen_val', 'content', 'options_lst'] )
    def __repr__(self):         return str( self.to_map() )
    def __eq__(self, other):    return self.to_map() == other.to_map()
    def __ne__(self, other):    return (not __eq__(self,other))

    def pack(self):
        """Serialize an CB object into packed bytes. NOTE: We are required to use
        Length-Value (LV) encoding for the custom content so that any options may also be recovered."""
        content_bytes = util.block32_lv_bytes_pack(to_bytes(self.content))
        options_bytes = option.pack_all( self.options_lst )
        block_total_len = 16 + len(content_bytes) + len(options_bytes)

        packed_bytes = ( struct.pack( self.head_encoding, self.block_type, block_total_len, self.pen_val ) +
                         content_bytes +
                         options_bytes +
                         struct.pack( self.tail_encoding, block_total_len ))
        return packed_bytes

#todo make subclasses like options:  CustomBlockCopyable CustomBlockNonCopyable
class CustomBlockCopyable(CustomBlock):
    "Serialize & deserialze a PCAPNG Custom Block - Copyable"
    SPEC_CODE = 0x00000BAD
    def __init__(self, pen_val, content, options_lst=[] ):
        "Creates an CBC object"
        CustomBlock.__init__(self, self.SPEC_CODE, pen_val, content, options_lst )

    @staticmethod
    def dispatch_entry(): return { CustomBlockCopyable.SPEC_CODE : CustomBlockCopyable.unpack }

    @staticmethod
    def unpack(packed_bytes):      #todo verify block type & all fields
        "Deserialize a CBC object from packed bytes"
        util.assert_type_bytes(packed_bytes)
        ( block_type, block_total_len, pen_val ) = struct.unpack( CustomBlock.head_encoding, packed_bytes[:12] )
        (block_total_len_end,)                   = struct.unpack( CustomBlock.tail_encoding, packed_bytes[-4:] )
        assert (block_type == CustomBlockCopyable.SPEC_CODE)
        assert pen_val == pcapng.pen.BROCADE_PEN
        assert block_total_len == block_total_len_end == len(packed_bytes)
        block_bytes_stripped = packed_bytes[12:-4]
        (content_bytes, options_bytes) = util.block32_lv_bytes_unpack_rolling(block_bytes_stripped)
        options_lst = option.unpack_all(CustomBlock.UNPACK_DISPATCH_TABLE, options_bytes)
        result_obj = CustomBlockCopyable( pen_val, content_bytes, options_lst )
        return result_obj

class CustomBlockNonCopyable(CustomBlock):
    "Serialize & deserialze a PCAPNG Custom Block - NonCopyable"
    SPEC_CODE = 0x40000BAD
    def __init__(self, pen_val, content, options_lst=[] ):
        "Creates a CBNC object"
        CustomBlock.__init__(self, self.SPEC_CODE, pen_val, content, options_lst )

    @staticmethod
    def dispatch_entry(): return { CustomBlockNonCopyable.SPEC_CODE : CustomBlockNonCopyable.unpack }

    @staticmethod
    def unpack(packed_bytes):      #todo verify block type & all fields
        "Deserialize a CBNC object from packed bytes"
        util.assert_type_bytes(packed_bytes)
        ( block_type, block_total_len, pen_val ) = struct.unpack( CustomBlock.head_encoding, packed_bytes[:12] )
        (block_total_len_end,)                   = struct.unpack( CustomBlock.tail_encoding, packed_bytes[-4:] )
        assert (block_type == CustomBlockNonCopyable.SPEC_CODE)
        assert pen_val == pcapng.pen.BROCADE_PEN
        assert block_total_len == block_total_len_end == len(packed_bytes)
        block_bytes_stripped = packed_bytes[12:-4]
        (content_bytes, options_bytes) = util.block32_lv_bytes_unpack_rolling(block_bytes_stripped)
        options_lst = option.unpack_all(CustomBlock.UNPACK_DISPATCH_TABLE, options_bytes)
        result_obj = CustomBlockNonCopyable( pen_val, content_bytes, options_lst )
        return result_obj

#-----------------------------------------------------------------------------
class CustomMrtIsisBlock:
    "Creates an ISIS MRT block and wraps it in a custom pcapng block"
    "Serialize & deserialze a PCAPNG ISIS MRT Block"
    cmib_options = [CUSTOM_MRT_ISIS_BLOCK_OPT]      # unique identifier for this block type

    def __init__(self, pkt_data):
        "Creates an ISIS MRT Block object"
        self.pkt_data = to_bytes(pkt_data)

    def pack(self):
        "Serialize a ISIS MRT Block object into packed bytes"
        cust_blk = CustomBlockCopyable( pcapng.pen.BROCADE_PEN,
                                mrt.mrt_isis_block_pack( self.pkt_data ), self.cmib_options )
        return cust_blk.pack()

    @staticmethod
    def unpack(packed_bytes):
        "Deserialize a ISIS MRT Block object from packed bytes"
        util.assert_type_bytes(packed_bytes)
        cbc_obj = CustomBlockCopyable.unpack(packed_bytes)
        assert cbc_obj.block_type   == CustomBlockCopyable.SPEC_CODE
        assert cbc_obj.pen_val      == pcapng.pen.BROCADE_PEN
        assert cbc_obj.options_lst  == CustomMrtIsisBlock.cmib_options
        mrt_info = mrt.mrt_isis_block_unpack( cbc_obj.content )
        return mrt_info

#-----------------------------------------------------------------------------
#todo make a BlockList class?

UNPACK_DISPATCH_TABLE = util.dict_merge_all( [
    SectionHeaderBlock.dispatch_entry(),
    InterfaceDescBlock.dispatch_entry(),
    SimplePacketBlock.dispatch_entry(),
    EnhancedPacketBlock.dispatch_entry(),
    CustomBlockCopyable.dispatch_entry(),
    CustomBlockNonCopyable.dispatch_entry(),
] )

def unpack_dispatch( packed_bytes ):
    "Invokes the proper parsing function given the packed bytes for a PCAPNG block."
    (blk_type, blk_total_len, stripped_bytes) = strip_header( packed_bytes )
    dispatch_fn = UNPACK_DISPATCH_TABLE[ blk_type ]
    if (dispatch_fn != None):
        result =  dispatch_fn( packed_bytes )
        return result
    else:
        #todo exception?
        # raise Exception( 'unpack_dispatch(): unrecognized block blk_type={}'.format(blk_type))
        #
        print( 'warning - Block.unpack_dispatch(): unrecognized Block={}'.format( blk_type )) #todo log
        return Block( Block.BLOCK_UNKNOWN, packed_bytes )

def pack_all( blk_lst ):
    "Given a list of PCAPNG blocks, converts all to packed bytes and concatenates the result"
    util.assert_type_list(blk_lst)
    cum_result = ''
    for blk in blk_lst:
        cum_result += blk.pack()
    return cum_result

def segment_all(raw_bytes):
    """Given concatenated packed bytes for PCAPNG blocks, returns a list of packed bytes for
    individual block segments"""
    util.assert_type_bytes(raw_bytes)
    util.assert_block32_length(raw_bytes)
    blk_segments = []
    while ( 0 < len(raw_bytes) ):
        assert 8 <= len(raw_bytes)
        (blk_type, blk_total_len, unused) = strip_header( raw_bytes )
        assert blk_total_len <= len(raw_bytes)
        blk_bytes             = raw_bytes[ :blk_total_len  ]
        raw_bytes_remaining   = raw_bytes[  blk_total_len: ]
        blk_segments.append( blk_bytes )
        raw_bytes = raw_bytes_remaining
    return blk_segments

def unpack_all(packed_bytes):
    """Given concatenated packed bytes for PCAPNG blocks, returns a list of PCAPNG block objects"""
    result = []
    blk_segments = segment_all( packed_bytes )
    for blk_bytes in blk_segments:
        new_blk = unpack_dispatch( blk_bytes )
        print( '411  new_blk=', new_blk)
        result.append(new_blk)
    return result



