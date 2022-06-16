import Geom
import ifcopenshell
import ifcopenshell.geom 
import ifcopenshell.util
import ifcopenshell.util.element
from ifcopenshell.util.selector import Selector
import numpy as np
import bcf
import bcf.v2.bcfxml
import json

def define_offset(bauteilTyp):
    with open("map_bcf.json", "r") as file:
        map_bcf = json.loads(file.read())
    get_offset = tuple(map_bcf[bauteilTyp])
    offset = np.array(get_offset)
    return offset

def export_bcfxml(aoi_bb,bcf_filename,filename):

    selector = Selector()
    model = ifcopenshell.open(filename)
    bcfxml = bcf.v2.bcfxml.BcfXml()
    bcfxml.new_project()
    bcfxml.project.name = "NewName"
    ueberbau = selector.parse(model, '.IfcBuildingElementProxy [Name *= "Ueberbau"]')[0]
    zmin_ueberbau = Geom.bounding_box_center(ueberbau).Z()
    xmin_ueberbau = Geom.bounding_box_center(ueberbau).X()
    ymin_ueberbau = Geom.bounding_box_center(ueberbau).Y()


    for i in aoi_bb:
        schadenObjekt = i.Name
        bauteilTyp = i.Description
        aoi_bb_position = Geom.bounding_box_center(i)
        if aoi_bb_position.Z() > zmin_ueberbau:
            z = 3
        else:
            z = -3
        if aoi_bb_position.X() > xmin_ueberbau:
            x = 3
        else:
            x = -3
        if aoi_bb_position.Y() > ymin_ueberbau:
            y = 3
        else:
            y = -3
        if "Widerlager_Wand_Hinten" in str(bauteilTyp):
            versatz = np.array((5,0,0))
        elif "Widerlager_Wand_Vorne" in str(bauteilTyp):
            versatz = np.array((-5,0,0))
        else:
            versatz =  np.array((x,y,z))
        bcfxml.edit_project()
        topic = bcf.v2.data.Topic()
        topic.title = schadenObjekt
        topic.description = bauteilTyp
        topic = bcfxml.add_topic(topic)
        viewpoint = bcf.v2.data.Viewpoint()
        viewpoint.perspective_camera = bcf.v2.data.PerspectiveCamera()
        position = np.array((aoi_bb_position.X(),aoi_bb_position.Y(),aoi_bb_position.Z()))
        point = position + versatz 
        viewpoint.perspective_camera.camera_view_point.x = point[0]
        viewpoint.perspective_camera.camera_view_point.y = point[1]
        viewpoint.perspective_camera.camera_view_point.z = point[2]
        mat = get_track_to_matrix(point, position)
        viewpoint.perspective_camera.camera_direction.x = mat[0][2] * -1
        viewpoint.perspective_camera.camera_direction.y = mat[1][2] * -1
        viewpoint.perspective_camera.camera_direction.z = mat[2][2] * -1
        viewpoint.perspective_camera.camera_up_vector.x = mat[0][1]
        viewpoint.perspective_camera.camera_up_vector.y = mat[1][1]
        viewpoint.perspective_camera.camera_up_vector.z = mat[2][1]
        viewpoint.components = bcf.v2.data.Components()
        viewpoint.components.visibility = bcf.v2.data.ComponentVisibility()
        viewpoint.components.visibility.default_visibility = True
        viewpoint.snapshot = get_viewpoint_snapshot(viewpoint, mat)
        bcfxml.add_viewpoint(topic, viewpoint)
        if i == 0:
            bcfxml.save_project(bcf_filename)
        else:
            bcfxml.save_project(bcf_filename)

def get_viewpoint_snapshot(viewpoint, mat):
    return None  # Possible to overload this function in a GUI application if used as a library

def get_track_to_matrix(camera_position, target_position):
    camera_direction = camera_position - target_position
    camera_direction = camera_direction / np.linalg.norm(camera_direction)
    camera_right = np.cross(np.array([0.0, 0.0, 1.0]), camera_direction)
    camera_right = camera_right / np.linalg.norm(camera_right)
    camera_up = np.cross(camera_direction, camera_right)
    camera_up = camera_up / np.linalg.norm(camera_up)
    rotation_transform = np.zeros((4, 4))
    rotation_transform[0, :3] = camera_right
    rotation_transform[1, :3] = camera_up
    rotation_transform[2, :3] = camera_direction
    rotation_transform[-1, -1] = 1
    translation_transform = np.eye(4)
    translation_transform[:3, -1] = -camera_position
    look_at_transform = np.matmul(rotation_transform, translation_transform)
    return np.linalg.inv(look_at_transform)