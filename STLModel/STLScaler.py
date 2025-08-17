import os
import numpy as np
from stl import mesh

# === Set your scaling factor here ===
scale_factor = 3.0

def scale_stl(input_path, output_path, factor):
    # Load mesh
    model = mesh.Mesh.from_file(input_path)

    # Apply scaling about the origin (0,0,0)
    model.vectors *= factor

    # Save the scaled mesh
    model.save(output_path)
    print(f"Scaled STL saved as: {output_path}")


def main():
    # Find the first STL in the current directory
    stl_files = [f for f in os.listdir('.') if f.lower().endswith('.stl')]
    if not stl_files:
        print("Error: No STL files found in the current directory.")
        return

    stl_files.sort()
    input_stl = stl_files[0]
    output_stl = f"scaled_{input_stl}"

    print(f"Scaling {input_stl} by factor {scale_factor} about the origin...")
    scale_stl(input_stl, output_stl, scale_factor)


if __name__ == "__main__":
    main()
