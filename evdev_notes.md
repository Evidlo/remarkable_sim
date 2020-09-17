- [event docs](https://www.kernel.org/doc/Documentation/input/multi-touch-protocol.txt)

codes resolved with python evdev

    dict(evdev.resolve_ecodes_dict({3: [0, 1, 24, 25, 26, 27]}))
    
# evdev Message Structure
- https://stackoverflow.com/questions/23480741/obtaining-evdev-event-code-from-raw-bytes

- 4 byte unsigned integer - seconds
- 4 byte unsigned integer - microseconds
- 2 byte unsigned integer - type
- 2 byte unsigned integer - code
- 4 byte signed integer - value

# Coordinate Systems

  Stylus          Touch         TKinter
+---------+    +---------+    +---------+
| x       |    |       y |    | +---x   |
| |       |    |       | |    | |       |
| |       |    |       | |    | |       |
| +--- y  |    |   x---+ |    | y       |
+---------+    +---------+    +---------+
|o   o   o|    |o   o   o|    |o   o   o|
+---------+    +---------+    +---------+

# evdev Event Files and Codes

## event0 - Stylus
- type 0 - ev_sync
- type 1 - ev_key
  - code [code #] - [name] - [desc] - [range]
  - code 320 - toolpen - -
  - code 321 - toolrubber - -
  - code 330 - touch - -
  - code 331 - stylus - -
  - code 332 - stylus2 - -
- type 3 - ev_abs - absolute
  - code 0 - abs_x - xpos - (0: bottom, 20967: top)
  - code 1 - abs_y - ypos - (0: left, 15725: right)
  - code 24 - abs_pressure - (0, 4095)
  - code 25 - abs_distance - distance between pen and surface - (0: lowered, ~100: raised)
  - code 26 - abs_tilt_x - (-6300: pen flat pointing up, 6300: pen flat pointing down)
  - code 27 - abs_tilt_y - (-6300: pen flat pointing right, 6300: pen flat pointing left

## event1 - Touch
- type 0 - ev_sync
- type 1 - ev_key
- type 3 - ev_abs
  - code 25 - abs_mt_distance - unused?
  - code 47 - abs_mt_slot - multitouch position number (see protocol example B in docs)
  - code 48 - abs_mt_touch_major - touch size major axis - needs further study {4: pointer touch, 24: thumb touch}
  - code 49 - abs_mt_touch_minor - touch size minor axis - 
  - code 52 - abs_mt_orientation - touch orientation
  - code 53 - abs_mt_position_x - xpos - (0: right side, 767: left side)
  - code 54 - abs_mt_position_y - ypos - (0: bottom, 1023: top
  - code 57 - abs_mt_tracking_id - press/release
    - value=X - increments by +1 with each press
    - value=-1 - release
  - code 58 - abs_mt_pressure - not really pressure but contact area - {30: very light touch, 90: typical touch during swipe, 150: thumb on screen}
  
## event2 - Buttons
- type 0 - ev_sync
- type 1 - ev_key
  - code 102 - home - middle button
    - value 1 - press
    - value 0 - release
  - code 105 - left - left button
  - code 106 - right - right button
  - code 116 - power - suspend button
  - code 143 - wakeup - unused?


