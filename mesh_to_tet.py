# Copyright (c) 2020 NVIDIA Corporation

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""Convert a .mesh file (fTetWild format) to .tet (IsaacGym format)."""

import argparse
import numpy as np
import os

parser = argparse.ArgumentParser("mesh to tet parser")
parser.add_argument("mesh_file", type=str, help="path to .mesh file to be converted")
parser.add_argument("--tet_file", type=str, help="path to output .tet file")
args = parser.parse_args()

mesh_file = args.mesh_file
if not os.path.exists(mesh_file) or os.path.splitext(mesh_file)[-1] != ".mesh":
    raise ValueError("mesh file not found or has incorrect extension!")
tet_file = args.tet_file
if tet_file is None:
    tet_file = os.path.splitext(mesh_file)[0] + ".tet"

# Define input and output file names
with open(mesh_file, "r") as f:
    mesh_lines = f.read().splitlines()

# Parse .mesh file
vertices_start = mesh_lines.index('Vertices')
num_vertices = mesh_lines[vertices_start + 1]
vertices = mesh_lines[vertices_start + 2:vertices_start + 2
                      + int(num_vertices)]

tetrahedra_start = mesh_lines.index('Tetrahedra')
num_tetrahedra = mesh_lines[tetrahedra_start + 1]
tetrahedra = mesh_lines[tetrahedra_start + 2:tetrahedra_start + 2
                        + int(num_tetrahedra)]

print(f"Mesh has {num_vertices} Vertices and {num_tetrahedra} Tetrahedra")

# Write to tet output
with open(tet_file, "w") as f:
    f.write("# Tetrahedral mesh generated using mesh_to_tet.py\n\n")
    f.write(f"# {num_vertices} vertices\n")
    for v in vertices:
        f.write(f"v {v}\n")
    f.write(f"\n# {num_tetrahedra} tetrahedra\n")
    for t in tetrahedra:
        t_line = " ".join(map(str, np.array(t.split(" ")[:-1], dtype=np.uint64) - 1))
        f.write(f"t {t_line}\n")
