import mdl
from display import *
from matrix import *
from draw import *

"""======== first_pass( commands ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)

  Should set num_frames and basename if the frames
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  ==================== """
def first_pass( commands ):

    name = ''
    num_frames = 1
    basename_here = False
    frames_here = False
    vary_here = False

    for command in commands:
        c = command['op']
        args = command['args']

        if c == "frames":
            num_frames = int(args[0])
            frames_here = True
        elif c == "basename":
            name = args[0]
            basename_here = True
        elif c == "vary":
            vary_here = True

    if (vary_here and not frames_here):
        exit()

    if (frames_here and not basename_here):
        print("Using basename \"default\"...")
        name = 'default'

    return (name, num_frames)

"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a separate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value.
  ===================="""
def second_pass( commands, num_frames ):
    frames = [ {} for i in range(int(num_frames)) ]

    for command in commands:
        c = command['op']
        args = command['args']
        if c == 'vary':
            name = command['knob']
            start_frame = int(args[0])
            end_frame = int(args[1])
            start_value = args[2]
            end_value = args[3]
            step = (end_value - start_value)/(end_frame - start_frame)

            for i in range(start_frame, end_frame+1):
                frames[i][name] = start_value + ((i - start_frame)*(end_value - start_value))/(end_frame - start_frame)

    return frames


def run(filename):
    """
    This function runs an mdl script
    """
    is_texture = False
    # figure out some sort of way to convert texture
    # into texture_pixels = { (u,v) : (R,G,B) } form
    # add a boolean is_texture that is true if we do this
        # texture TEXTURE.png added as a command
        # is_texture = True
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print( "Parsing failed.")
        return
    print("COMMANDS")
    for command in commands:
        print(command)
    print("SYMBOLS")
    for symbol in symbols:
        print(symbol, symbols[symbol])

    if 'TEXTURE' in symbols.keys():
        is_texture = True
        texture_dict = symbols['TEXTURE'][1]

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    (name, num_frames) = first_pass(commands)
    frames = second_pass(commands, num_frames)
    if num_frames > 1:
        is_anim = True
    else:
        is_anim = False

    for i in range(num_frames):
        if is_anim:
            print("FRAME %d" % (i))
        tmp = new_matrix()
        ident( tmp )

        stack = [ [x[:] for x in tmp] ]
        screen = new_screen()
        zbuffer = new_zbuffer()
        tmp = []
        step_3d = 100
        consts = ''
        coords = []
        coords1 = []

        for command in commands:
            print(command)
            c = command['op']
            args = command['args']
            knob_value = 1
            if 'knob' in command.keys() and command['knob'] is not None:
                knob_value = frames[i][command['knob']]
                # print("current knob_value = %f" % (knob_value))

            if c == 'box':
                if command['constants']:
                    reflect = command['constants']
                    # texture = command['texture']
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                # if there is a texture, apply it here
                if is_texture and command['texture']:
                    print("there is a texture...")
                    # print("texture[COORDS]:", texture_dict)
                    # print("texture[TYPE]:", command['texture'])
                    texture = [texture_dict, command['texture']]
                    draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect, texture)
                else:
                    print("there is NO texture...")
                    draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'sphere':
                if command['constants']:
                    reflect = command['constants']
                add_sphere(tmp,
                           args[0], args[1], args[2], args[3], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'torus':
                if command['constants']:
                    reflect = command['constants']
                add_torus(tmp,
                          args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'line':
                add_edge(tmp,
                        args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_lines(tmp, screen, zbuffer, color)
                tmp = []
            elif c == 'move':
                tmp = make_translate(knob_value*args[0], knob_value*args[1], knob_value*args[2])
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':
                tmp = make_scale(knob_value*args[0], knob_value*args[1], knob_value*args[2])
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                theta = knob_value*args[1] * (math.pi/180)
                if args[0] == 'x':
                    tmp = make_rotX(theta)
                elif args[0] == 'y':
                    tmp = make_rotY(theta)
                else:
                    tmp = make_rotZ(theta)
                matrix_mult( stack[-1], tmp )
                stack[-1] = [ x[:] for x in tmp]
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                display(screen)
            elif c == 'save':
                save_extension(screen, args[0])
            # end operation loop
        if is_anim:
            save_extension(screen, "./anim/"+name+"%03d" % (i))
    if is_anim:
        make_animation(name)
