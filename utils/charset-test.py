import sys
import tdl


def main(path):

    tdl.set_font(path, greyscale=True, altLayout=True)

    root_console = tdl.init(20, 20, title='Rougelike Tutorial Game')
    while not tdl.event.is_window_closed():
        for o in range(200):
            x, y = o % 20, o // 20
            root_console.draw_char(x, y, chr(o))
            #root_console.draw_char(1, 1, chr(24))
            tdl.flush()


if __name__ == '__main__':
    
    path = sys.argv[1]
    main(path)
