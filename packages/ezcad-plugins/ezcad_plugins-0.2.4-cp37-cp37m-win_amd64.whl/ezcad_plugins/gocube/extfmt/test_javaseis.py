# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import sys
sys.path.append('.')  # current directory
sys.path.append('../..')  # ezcad_plugins
sys.path.append(r'C:\Users\xinfa\Documents\code\pieseis')

import os
os.environ['data_io/javaseis'] = 'True'

from javaseis import load_cube

fn = r"C:\Users\xinfa\Documents\test\synth.js"

dob = load_cube(fn)

print('done')
