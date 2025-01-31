import subprocess

import numpy as np
from svgpathtools import (
    Arc,
    CubicBezier,
    Line,
    Path,
    QuadraticBezier,
    parse_path,
)


def apply_projective_transform(pt, H):
    x, y = pt.real, pt.imag
    vec = np.array([x, y, 1])
    xp, yp, wp = H @ vec
    return complex(xp / wp, yp / wp)


def transform_path(path, H):
    new_segments = []
    for seg in path:
        if isinstance(seg, Line):
            new_segments.append(
                Line(
                    apply_projective_transform(seg.start, H),
                    apply_projective_transform(seg.end, H),
                )
            )
        elif isinstance(seg, CubicBezier):
            new_segments.append(
                CubicBezier(
                    apply_projective_transform(seg.start, H),
                    apply_projective_transform(seg.control1, H),
                    apply_projective_transform(seg.control2, H),
                    apply_projective_transform(seg.end, H),
                )
            )
        elif isinstance(seg, QuadraticBezier):
            new_segments.append(
                QuadraticBezier(
                    apply_projective_transform(seg.start, H),
                    apply_projective_transform(seg.control, H),
                    apply_projective_transform(seg.end, H),
                )
            )
        elif isinstance(seg, Arc):
            # Arcs are hard; fallback to line
            new_segments.append(
                Line(
                    apply_projective_transform(seg.start, H),
                    apply_projective_transform(seg.end, H),
                )
            )
    return Path(*new_segments)


def compute_projective_transform(src_pts, dst_pts):
    A = []
    B = []
    for zs, zd in zip(src_pts, dst_pts):
        x, y = zs.real, zs.imag
        xp, yp = zd.real, zd.imag
        A.append([x, y, 1, 0, 0, 0, -x * xp, -y * xp])
        A.append([0, 0, 0, x, y, 1, -x * yp, -y * yp])
        B.append(xp)
        B.append(yp)
    A = np.array(A)
    B = np.array(B)
    h = np.linalg.solve(A, B)
    H = np.append(h, 1).reshape(3, 3)
    return H


# ---------------------------------------------------------
# Everything above this point, courtesy of ChatGPT.
# Everything below, written by me for my specific use case.
# ---------------------------------------------------------


# This path describes the shape of a corner piece on a face of a kilominx.
BASE_CORNER_PATH = parse_path("M 310 0 L 460 115 L 310 290 L 160 115 Z")


def get_paths_for_template_face():
    """
    Take piece types above, and apply a series of transformations (rotation, translation,
    and scale) so that we end up with 5x SVG paths each for corners and edges, and the one
    for the center piece.

    This gives us hardcoded paths which we can later transform manually.
    """

    # Based on some experimentation in a test SVG, when putting these paths for the mega pieces
    # onto a 300px-per-edge pentagon centered at (310,310), the following transforms give us
    # what we need.
    #
    # scale(0.9, 0.9)
    # translate(31, 12) for a corner
    # translate(40, 20) for an edge

    paths = []

    for angle in [0, 72, 144, 216, 288]:
        # Apply the transformations to each segment and generate a new path for the corner
        paths.append(
            Path(
                *[
                    (
                        segment.scaled(0.9)
                        .translated((31 + 12j))
                        .rotated(angle, 310 + 310j)
                    )
                    for segment in list(BASE_CORNER_PATH)
                ]
            )
        )

    return paths


def transform_to_target_pentagon(target_pentagon_coords, paths):
    """
    For a given set of coordinates representing the 5 vertices of a target pentagon:

    1. Calculates a 3D perspective transformation matrix between that target, and a hardcoded
       source pentagon.

    2. Applies that perspective transformation to all the paths that were passed in

    3. Returns the transformed paths
    """
    source_pentagon_coords = [(310, 0), (603, 215), (491, 559), (128, 559), (16, 215)]
    H = compute_projective_transform(
        src_pts=[complex(x, y) for x, y in source_pentagon_coords[:4]],
        dst_pts=[complex(x, y) for x, y in target_pentagon_coords[:4]],
    )

    return [transform_path(path, H) for path in paths]


def round_svg_path(path_str, radius=10):
    path_without_final_line = Path(*list(path)[:-1])
    path_d = path_without_final_line.d() + " Z"

    result = subprocess.run(
        ["node", "round.js", f'"{path_d}"', str(radius)],
        capture_output=True,
        text=True,
        check=True,
        cwd="C:\\Users\\Wes\\dev\\cubersio_v2\\frontend\\src\\scripts",
    )
    return result.stdout.strip()


def _render_as_svg_path_xml(path_d, color):
    return f'<path d="{path_d}" fill="var(--color-{color})" />'


if __name__ == "__main__":
    # Get the SVG paths for all pieces on a "template" face of the megaminx.
    template_face_paths = get_paths_for_template_face()

    # These sets of coordinates are the vertices of the pentagonal faces on an
    # isometric projection of a dodecahedron.
    target_pentagon_coords = [
        [(246, 125), (471, 256), (420, 509), (168, 530), (63, 301)],
        [(267, 16), (463, 63), (591, 196), (471, 256), (246, 125)],
        [(591, 196), (604, 379), (512, 557), (420, 509), (471, 256)],
        [(420, 509), (512, 557), (353, 596), (160, 584), (168, 530)],
        [(12, 264), (63, 301), (168, 530), (160, 584), (70, 429)],
        [(267, 16), (246, 125), (63, 301), (12, 264), (130, 107)],
    ]

    # For each face on the isometric projection, transform the SVG paths for the pieces
    # on the template face onto that face on the projection.
    projection_face_paths = [
        transform_to_target_pentagon(target, template_face_paths)
        for target in target_pentagon_coords
    ]

    for face, params in zip(
        projection_face_paths,
        [
            ("white", 10),
            ("green", 5),
            ("purple", 5),
            ("yellow", 3),
            ("blue", 2),
            ("red", 3),
        ],
    ):
        print()
        color, radius = params
        print("<g>")
        for path in face:
            rounded_path_d = round_svg_path(path, radius)
            print("  " + _render_as_svg_path_xml(rounded_path_d, color))
        print("</g>")
