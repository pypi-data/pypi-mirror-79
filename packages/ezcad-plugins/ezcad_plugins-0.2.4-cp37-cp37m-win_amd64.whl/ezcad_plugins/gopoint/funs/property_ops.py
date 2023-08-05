# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import numpy as np
from datetime import datetime
from ezcad.utils.plotting import default_gradient, \
    make_colormap_from_gradient, make_colormap_from_gradient_vispy
from ezcad.utils.envars import LMT_LST_DELTA


def add_property(dob, prop_name, array=None, clip=None, gradient=None,
    save=True):
    """Add a property to an object.

    :param dob: the host data object
    :type dob: object
    :param prop_name: the property name
    :type prop_name: str
    :param array: the property data array
    :type array: array
    :param clip: the clip values for plot, [min, max]
    :type clip: list
    :param gradient: the color gradient for plot, for example,
      :const:`~ezcad.utils.plotting.default_gradient`
    :type gradient: dict
    :param save: need save or not
    :type save: bool
    """
    if array is None:
        if dob.prop_array_key == 'array1d':
            array = np.zeros(dob.vertexes['xyz'].shape[0])
        elif dob.prop_array_key == 'array2d':
            array = np.zeros(dob.gridz['array'].shape)
        elif dob.prop_array_key == 'array3d':
            NIL = int(dob.dict_vidx['IL_AMNT'])
            NXL = int(dob.dict_vidx['XL_AMNT'])
            NDP = int(dob.dict_vidx['DP_AMNT'])
            array = np.zeros((NIL, NXL, NDP), dtype='float32')
        else:
            raise ValueError('Unknown value')

    dob.prop[prop_name] = {dob.prop_array_key: array}
    timestamp = datetime.now()
    dob.prop[prop_name]['arrayLMT'] = timestamp
    if save:
        dob.prop[prop_name]['arrayLST'] = timestamp - LMT_LST_DELTA
    else:
        dob.prop[prop_name]['arrayLST'] = timestamp + LMT_LST_DELTA

    dob.set_clip(prop_name, clip=clip)
    dob.set_gradient(prop_name, gradient=gradient)
    dob.make_colormap(prop_name)

    # Do NOT make one per property. Use one and update it with
    # the current property. This way is easier for add and remove item
    # to and from the viewer, as compared to one item per property.
    # self.prop[prop_name]['section_number'] = {}


def set_clip(dob, prop_name, clip=None):
    """Set the clip of an object.

    :param dob: the host data object
    :type dob: object
    :param prop_name: the property name
    :type prop_name: str
    :param clip: the clip values for plot, [min, max]
    :type clip: list
    """
    if clip is None:  # initialize
        prop_array = dob.prop[prop_name][dob.prop_array_key]
        # clipMin = np.amin(prop_array) # type <class 'numpy.float32'>
        # clipMax = np.amax(prop_array) # type <class 'numpy.float32'>
        # # This conversion to native python type matters to sqlite.
        # clipMin = np.asscalar(clipMin) # type <class 'float'>
        # clipMax = np.asscalar(clipMax) # type <class 'float'>
        # clip = [clipMin, clipMax] # percentile 0 and 100
        # When initialize, default clip 1% and 99% for plotting.
        p1 = np.percentile(prop_array, 1)
        p99 = np.percentile(prop_array, 99)
        clip = [p1, p99]
    dob.prop[prop_name]['colorClip'] = clip


def set_gradient(dob, prop_name, gradient=None):
    """Set the color gradient of an object.

    :param dob: the host data object
    :type dob: object
    :param prop_name: the property name
    :type prop_name: str
    :param gradient: the color gradient for plot, for example,
      :const:`~ezcad.utils.plotting.default_gradient`
    :type gradient: dict
    """
    if gradient is None:  # initialize
        gradient = default_gradient
    dob.prop[prop_name]['colorGradient'] = gradient


def make_colormap(dob, prop_name):
    """Make colormap for a property of an object.
    Colormap is important for Point; it is used in both 2D and 3D plot.

    :param dob: the host data object
    :type dob: object
    :param prop_name: the property name
    :type prop_name: str
    """
    gradient = dob.prop[prop_name]['colorGradient']
    clip = dob.prop[prop_name]['colorClip']

    # Gsurface has no atom_style, thus this condition.
    # TODO move this part to set_gradient()
    # if hasattr(dob, 'atom_style'):
    #     alpha = dob.atom_style['opacity']
    #     set_gradient_alpha(gradient, alpha)

    cmap = make_colormap_from_gradient(clip, gradient)
    dob.prop[prop_name]['colormap'] = cmap
    cmap_vs = make_colormap_from_gradient_vispy(gradient)
    dob.prop[prop_name]['colormap_vs'] = cmap_vs

    if dob.geometry_type == 'Cube':
        lut = cmap.getLookupTable(start=clip[0], stop=clip[1], nPts=256)
        dob.prop[prop_name]['colorLut'] = lut
        # myprint('lut =', lut)
        # myprint('lut type =', type(lut)) # class numpy.ndarray
        # myprint('lut shape =', lut.shape) # (256,3)

        # Create lut from scratch
        # lut = np.zeros((256,3), dtype=np.ubyte)
        # lut[:,0] = 255
        # lut[:,1] = 255 - np.arange(256)
        # lut[:,2] = 255 - np.arange(256)


def set_current_property(dob, prop_name=None, update_plots=False):
    """Set the current property of an object.

    :param dob: the host data object
    :type dob: object
    :param prop_name: the property name
    :type prop_name: str
    :param update_plots: update plots or not
    :type update_plots: bool
    """
    if prop_name is None:  # initialize
        prop_name = list(dob.prop.keys())[0]
    dob.current_property = prop_name
    if update_plots:
        dob.update_plots_by_prop()
