import os
import numpy as np
from stl import mesh

# === Set your deformation scales here ===
scale1 = -1.0       # absolute deformation scale of the first STL
scale2 = 1.0      # absolute deformation scale of the second STL
output_scale = 0.0  # absolute deformation scale for the output (can be negative)
# ========================================

def main():
    # Find STL files in current directory
    stl_files = [f for f in os.listdir('.') if f.lower().endswith('.stl')]
    if len(stl_files) < 2:
        print("Error: Less than two STL files found in the current directory.")
        return
    stl_files.sort()

    stl_path_a, stl_path_b = stl_files[:2]
    print(f"Using STL files: {stl_path_a} (scale={scale1}) and {stl_path_b} (scale={scale2})")
    print(f"Output model deformation scale: {output_scale}")

    # Load meshes
    mesh_a = mesh.Mesh.from_file(stl_path_a)
    mesh_b = mesh.Mesh.from_file(stl_path_b)

    # Check shape
    if mesh_a.vectors.shape != mesh_b.vectors.shape:
        print("Error: The two STL files have different mesh connectivity or number of triangles.")
        return

    # Avoid division by zero
    if np.isclose(scale1, scale2):
        print("Error: scale1 and scale2 must be different.")
        return

    # Solve linear model: M(s) = U + s * D
    # Use both inputs so we don't assume scale1 != 0
    D = (mesh_a.vectors - mesh_b.vectors) / (scale1 - scale2)  # unit deformation field per scale = 1
    U = mesh_a.vectors - scale1 * D                             # undeformed geometry (s = 0)

    # Output at desired absolute deformation scale (supports negative scales)
    output_vectors = U + output_scale * D

    # Save STL
    new_mesh = mesh.Mesh(np.zeros(mesh_a.vectors.shape[0], dtype=mesh.Mesh.dtype))
    new_mesh.vectors = output_vectors
    out_name = "output_model.stl"
    new_mesh.save(out_name)
    print(f"Output mesh saved as: {out_name}")

if __name__ == "__main__":
    main()
