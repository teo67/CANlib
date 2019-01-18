import sys
sys.path.append('ParseCAN')
import ParseCAN
from common import can_lib_h_path, templ, coord, ifndef, endif, is_multplxd, frame_handler


def write_declare(frame, name_prepends, fw, *args):
    fw('DECLARE({})\n'.format(coord(name_prepends, frame.name, prefix=False)))


def write(can, output_path=can_lib_h_path):
    header_name = '_PACK_UNPACK_H'

    with open(output_path, 'w') as f:
        fw = f.write

        # Setup file
        fw(ifndef(header_name))

        # Includes
        fw(
            '#include <stdint.h>' '\n'
            '#include <stdbool.h>' '\n'
            '#include "structs.h"' '\n'
            '#include "static_can.h"' '\n\n'
        )

        # Universal message forms (independent of bus)
        uni = ['CAN_ERROR_MSG', 'CAN_UNKNOWN_MSG']

        # Begin enumerating from the universal forms onward
        # Every time we assign to an enum, we'll increment beg
        # so as to avoid return value equalities between different bus
        idx = 0
        for msgt in uni:
            fw(templ['define'].format(msgt, idx))
            idx += 1

        fw('\n')

        # Create forms enum for each bus
        for bus in can.bus:
            fw('typedef enum {\n')

            # First frame needs to start at 2, the rest will follow
            first_frame = True
            for msg in bus.frame:
                if is_multplxd(msg):
                    for frame in msg.frame:
                        fw('\t' + coord(bus.name, msg.name, frame.name))
                        if first_frame:
                            fw(' = 2')
                        first_frame = False
                        fw(',\n')
                else:
                    fw('\t' + coord(bus.name, msg.name))
                    if first_frame:
                        fw(' = 2')
                    first_frame = False
                    fw(',\n')

            fw('} ' + '{}_T;\n\n'.format(coord(bus.name)))

            fw('{}_T CANlib_Identify_{}(Frame* frame);'.format(coord(bus.name), coord(bus.name, prefix=False)) + '\n\n')

        # Write DECLARE statements
        for bus in can.bus:
            for msg in bus.frame:
                frame_handler(msg, bus.name, write_declare, fw)

        fw('\n')

        fw(endif(header_name))