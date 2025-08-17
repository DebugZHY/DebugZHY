import struct
import math
import os


def ensure_output_dir(directory):
    """Create output directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_stl_header(f, num_triangles):
    """Write STL header."""
    header = b"Generated STL file for academic testing" + b"\0" * 41
    f.write(header)
    f.write(struct.pack('<I', num_triangles))


def write_triangle(f, v1, v2, v3):
    """Write a triangle to STL file."""
    edge1 = [v2[i] - v1[i] for i in range(3)]
    edge2 = [v3[i] - v1[i] for i in range(3)]
    normal = [
        edge1[1] * edge2[2] - edge1[2] * edge2[1],
        edge1[2] * edge2[0] - edge1[0] * edge2[2],
        edge1[0] * edge2[1] - edge1[1] * edge2[0]
    ]
    length = math.sqrt(sum(n * n for n in normal))
    normal = [n / length for n in normal] if length > 0 else [0, 0, 1]
    for n in normal:
        f.write(struct.pack('<f', n))
    for vertex in [v1, v2, v3]:
        for coord in vertex:
            f.write(struct.pack('<f', coord))
    f.write(struct.pack('<H', 0))


def rotate_vertex(vertex, angle):
    """Rotate a vertex around the z-axis by a given angle."""
    x, y, z = vertex
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)
    x_rot = cos_theta * x - sin_theta * y
    y_rot = sin_theta * x + cos_theta * y
    return [x_rot, y_rot, z]


def create_deformed_beam_stl(filename, length=100, section_size=10, num_parts=10, amplitude=10, rotation_angle=0.1):
    """Create a deformed beam with a sine wave shape (bowing) and rotation applied to the cross-section."""
    # Calculate the size of each part along the beam's length
    part_length = length / num_parts
    half_section_size = section_size / 2

    # Generate the beam vertices and create the sections
    vertices = []
    for i in range(num_parts):
        z_offset = i * part_length

        # Define the four corners of the square section with deformed x-coordinate (lateral deformation)
        v0 = [half_section_size, half_section_size, z_offset]  # v0
        v1 = [-half_section_size, half_section_size, z_offset]  # v1
        v2 = [-half_section_size, -half_section_size, z_offset]  # v2
        v3 = [half_section_size, -half_section_size, z_offset]  # v3

        # Apply sine wave deformation (lateral deformation)
        v0[0] += amplitude * math.sin(z_offset / length * 2 * math.pi)  # Apply deformation to x
        v1[0] += amplitude * math.sin(z_offset / length * 2 * math.pi)
        v2[0] += amplitude * math.sin(z_offset / length * 2 * math.pi)
        v3[0] += amplitude * math.sin(z_offset / length * 2 * math.pi)

        # Apply rotation deformation (rotate around the z-axis)
        angle = rotation_angle * z_offset  # Rotation angle increases along the length of the beam
        v0 = rotate_vertex(v0, angle)
        v1 = rotate_vertex(v1, angle)
        v2 = rotate_vertex(v2, angle)
        v3 = rotate_vertex(v3, angle)

        vertices.append(v0)
        vertices.append(v1)
        vertices.append(v2)
        vertices.append(v3)

    # Create triangles for each part of the beam
    triangles = []
    for i in range(num_parts - 1):
        # Get the indices of the current and next part
        start = i * 4

        # Front face (v0, v1, v4), (v1, v5, v4)
        triangles.append([vertices[start], vertices[start + 1], vertices[start + 4]])
        triangles.append([vertices[start + 1], vertices[start + 5], vertices[start + 4]])

        # Top face (v1, v2, v5), (v2, v6, v5)
        triangles.append([vertices[start + 1], vertices[start + 2], vertices[start + 5]])
        triangles.append([vertices[start + 2], vertices[start + 6], vertices[start + 5]])

        # Bottom face (v2, v3, v6), (v3, v7, v6)
        triangles.append([vertices[start + 2], vertices[start + 3], vertices[start + 6]])
        triangles.append([vertices[start + 3], vertices[start + 7], vertices[start + 6]])

        # Back face (v3, v0, v7), (v0, v4, v7)
        triangles.append([vertices[start + 3], vertices[start], vertices[start + 7]])
        triangles.append([vertices[start], vertices[start + 4], vertices[start + 7]])

    # Add end faces for the first and last parts
    # First part (front face)
    start = 0
    triangles.append([vertices[start + 1], vertices[start], vertices[start + 2]])
    triangles.append([vertices[start + 2], vertices[start], vertices[start + 3]])

    # Last part (back face)
    start = (num_parts - 1) * 4
    triangles.append([vertices[start], vertices[start + 1], vertices[start + 2]])
    triangles.append([vertices[start], vertices[start + 2], vertices[start + 3]])

    # Write the STL file
    with open(filename, 'wb') as f:
        write_stl_header(f, len(triangles))
        for triangle in triangles:
            write_triangle(f, *triangle)


# --- Main: Create output folder and STL files ---
output_dir = "Sample STL"
ensure_output_dir(output_dir)

# Create deformed beam STL file (lateral deformation + rotation)
create_deformed_beam_stl(os.path.join(output_dir, 'Torsional.stl'))

print("STL file for the deformed beam (lateral sine deformation + rotational deformation) created successfully!")
