# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

#: Default atom style.
ATOM_STYLE = {
    'symbol': 'disc',
    'size': 5,
    'coloring': 1,  # 1: single, 2: varying
    'edge_width': 0,
    'edge_color': (255, 0, 0, 255),
    'face_color': (255, 0, 0, 255),
    'opacity': 255,
}

GEOMETRY_TYPES = ['Point', 'Line', 'Tsurface', 'Gsurface', 'Cube', 'Label']

point_in_polygon_use_mpltpath = False
point_in_polygon_use_shapely = False


def copy_property(treebase, from_object, from_prop, to_object, to_prop):
    """Copy property.

    :param treebase: DataTreeBase object
    :type treebase: object
    :param from_object: source object
    :type from_object: str
    :param from_prop: source property
    :type from_prop: str
    :param to_object: destination object
    :type to_object: str
    :param to_prop: destination property
    :type to_prop: str
    """
    source_object = treebase.object_data[from_object]
    dest_object = treebase.object_data[to_object]

    # TODO
    # warn to/from object geom diff, cancel
    # warn from object property not exist
    # warn to object prop exist, overwrite?

    # if source_object.geometry_type in [
    #     'Point', 'Line', 'Tsurface', 'Gsurface', 'Cube']:

    key = source_object.prop_array_key
    array = source_object.prop[from_prop][key]
    clip = source_object.prop[from_prop]['colorClip']
    gradient = source_object.prop[from_prop]['colorGradient']
    # add to data object
    dest_object.add_property(to_prop, array=array, clip=clip,
                             gradient=gradient)
    # add to data tree
    treebase.add_object_property(dest_object, to_prop)
