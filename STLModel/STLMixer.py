import os
import numpy as np
from stl import mesh

def main():
    # Find STL files in current directory
    stl_files = [f for f in os.listdir('.') if f.lower().endswith('.stl')]
    if len(stl_files) < 2:
        print("Error: Less than two STL files found in the current directory.")
        return
    stl_files.sort()

    stl_path_a, stl_path_b = stl_files[:2]
    print(f"Using STL files: {stl_path_a} and {stl_path_b}")

    # Load meshes
    mesh_a = mesh.Mesh.from_file(stl_path_a)
    mesh_b = mesh.Mesh.from_file(stl_path_b)

    # Check that they have the same shape
    if mesh_a.vectors.shape != mesh_b.vectors.shape:
        print("Error: The two STL files have different mesh connectivity or number of triangles.")
        return

    # Average corresponding vertices by index (neutralization)
    undeformed_vectors = (mesh_a.vectors + mesh_b.vectors) / 2

    # Create a new mesh and save it
    new_mesh = mesh.Mesh(np.zeros(mesh_a.vectors.shape[0], dtype=mesh.Mesh.dtype))
    new_mesh.vectors = undeformed_vectors

    out_name = "undeformed.stl"
    new_mesh.save(out_name)
    print(f"Undeformed mesh saved as: {out_name}")

if __name__ == "__main__":
    main()
