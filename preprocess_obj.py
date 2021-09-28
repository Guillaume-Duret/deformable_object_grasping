import trimesh as tr
import os

masses = {
        'bar_clamp': 18.5,
        'book': 34.8,
        'bowl': 15.7,
        'cat': 9.9,
        'cube_3cm': 3.0,
        'endstop_holder': 16.3,
        'engine_part': 28.6,
        'fan_extruder': 7.4,
        'gearbox': 7.4,
        'large_marker': 3.2,
        'mount1': 10.4,
        'mug': 20.2,
        'nozzle': 6.3,
        'part1': 6.8,
        'part3': 13.6,
        'pawn': 18.6,
        'pear': 6.5,
        'pipe_connector': 23.5,
        'sardines': 11.2,
        'sulfur_neutron': 7.0,
        'vase': 13.1,
        'yoda': 20.4 
        }

def write_urdf(
    obj_name,
    obj_mass,
    obj_path,
    output_folder,
):
    content = open("resources/urdf.template").read()
    content = content.replace("NAME", obj_name)
    content = content.replace("MASS", "%f" % obj_mass)
    content = content.replace("MEAN_X", "0.0")
    content = content.replace("MEAN_Y", "0.0")
    content = content.replace("MEAN_Z", "0.0")
    content = content.replace("SCALE", "1.0")
    content = content.replace("COLLISION_OBJ", obj_path)
    content = content.replace("GEOMETRY_OBJ", obj_path)

    obj_msh = tr.load(obj_path)
    obj_msh.density = obj_mass / obj_msh.volume
    mat_int = obj_msh.moment_inertia
    content = content.replace("IXX", "%e" % mat_int[0][0])
    content = content.replace("IXY", "%e" % mat_int[0][1])
    content = content.replace("IXZ", "%e" % mat_int[0][2])
    content = content.replace("IYY", "%e" % mat_int[1][1])
    content = content.replace("IYZ", "%e" % mat_int[1][2])
    content = content.replace("IZZ", "%e" % mat_int[2][2])

    urdf_path = os.path.abspath(
        os.path.join(output_folder, obj_name + ".urdf")
    )
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    open(urdf_path, "w").write(content)
    return urdf_path

def add_object(obj_name):
    urdf_path = write_urdf(
        obj_name,
        masses[obj_name] / 1000,
        "dexgrasp_data/object_meshes/%s.obj" % obj_name,
        "examples/%s" % obj_name
    )

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('obj_name')
    args = parser.parse_args()

    add_object(args.obj_name)
