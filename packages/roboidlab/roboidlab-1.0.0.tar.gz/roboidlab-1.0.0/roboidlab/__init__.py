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

from roboidlab.line_recorder import HamsterRecorder
from roboidlab.q_game import QGame
from roboidlab.grid import *

__version__ = "1.0.0"

__all__ = ["record_hamster", "create_grid_world", "create_grid_hamster", "create_grid_hamster_s", "q_game_hamster", "q_game_hamster_s"]

def record_hamster(file_path):
    HamsterRecorder().start(file_path)

def create_grid_world(grid_robot):
    return GridWorld(grid_robot)

def create_grid_hamster():
    return GridHamster()

def create_grid_hamster_s():
    return GridHamsterS()

def q_game_hamster():
    QGame().start(GridHamster())

def q_game_hamster_s():
    QGame().start(GridHamsterS())
