# Part of the ROBOID project - http://hamster.school
# Copyright (C) 2016 Kwang-Hyun Park (akaii@kw.ac.kr)
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General
# Public License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA

from roboid import *
from pynput.keyboard import Listener, Key
import pandas as pd


class HamsterRecorder:
    _STATE_IDLE = 0
    _STATE_MOVE = 1

    def __init__(self):
        self._pressed_key = None
        self._usage()

    def _on_keyboard_released(self, key):
        if hasattr(key, 'char'): self._pressed_key = key.char
        else: self._pressed_key = key

    def _usage(self):
        print('Press space key to move/stop')
        print('Press s key to save')
        print('Press ESC key to quit')
        print()

    def start(self, file_path='./data.csv'):
        Listener(on_release=self._on_keyboard_released).start()
        
        left_floors = []
        left_wheels = []
        right_wheels = []
        state = HamsterRecorder._STATE_IDLE
        hamster = Hamster()

        while True:
            if state == HamsterRecorder._STATE_IDLE:
                if self._pressed_key == Key.space:
                    state = HamsterRecorder._STATE_MOVE
            elif state == HamsterRecorder._STATE_MOVE:
                diff = (left_floor - 50) * 0.5
                left_wheel = 30 + diff
                right_wheel = 30 - diff
                hamster.wheels(left_wheel, right_wheel)
                left_floors.append(hamster.left_floor())
                left_wheels.append(left_wheel)
                right_wheels.append(right_wheel)
                
                if self._pressed_key == Key.space:
                    hamster.stop()
                    state = HamsterRecorder._STATE_IDLE
            
            left_floor = hamster.left_floor()
            if self._pressed_key == 's':
                df = pd.DataFrame({'left_floor': left_floors,
                                   'left_wheel': left_wheels,
                                   'right_wheel': right_wheels})
                df.to_csv(file_path, index=False)
                print('Saved to', file_path)
            elif self._pressed_key == Key.esc:
                break

            self._pressed_key = None
            wait(20)
        
        hamster.dispose()
