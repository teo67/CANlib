src_dir = '../src/'
constants_path = f'{src_dir}constants.h'
can_lib_c_path = f'{src_dir}CANlib.c'
can_lib_h_path = f'{src_dir}CANlib.h'
enum_segments_path = f'{src_dir}enum_segments.h'
structs_path = f'{src_dir}structs.h'
can_lib_c_base_path = 'templates/CANlib_c.template'


def coord(*args, prefix=True):
    '''
    Returns the proper format for global names.
    '''

    if prefix:
        args = ('CANlib', ) + args

    return '_'.join(args)


def ifndef(name):
    '''
    Return a string for beginning the
    #ifndef ...
    #define ...
    <code>
    #endif // ... procedure.
    '''
    return '#ifndef {0}\n#define {0}\n\n'.format(name)


def endif(name):
    '''
    Return a string for ending the
    #ifndef ...
    #define ...
    <code>
    #endif // ... procedure.
    '''
    return '\n#endif // {0}\n'.format(name)


'''A template dict to define assignment within a `key`.'''
templ = {
    'enum': '\t{} = {},\n',
    'define': '#define {} {}\n',
}
