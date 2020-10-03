from pico2d import *

running = True
frame_interval = 0.05

def quit():
    global running
    running = False

def run(state):
    global running
    global current_state

    current_state = state

    open_canvas()
    current_state.enter()

    while running:
        #event handling
        evts = get_events()
        for e in evts:
            current_state.handle_event(e)

        #update
        current_state.update()

        #game rendering
        clear_canvas()
        current_state.draw()
        update_canvas()
#     for jelly in jellys:
#           jelly.draw()
        delay(frame_interval)

    close_canvas()

def change(state):
    global current_state
    current_state.exit()
    current_state = state
    current_state.enter()

def run_main():
    import sys
    main_module = sys.modules['__main__']
    run(main_module)