import trimesh
import pyrender
import numpy as np
import os
import imageio


class Preprocess:
    def render_gltf_with_rotations(self, gltf_path, output_dir, image_cnt):
        os.makedirs(output_dir, exist_ok=True)

        # Rotation angles (in degrees)
        angles = [0, 45, 90, 135, 180, 225, 270, 315]

        scene = trimesh.load(gltf_path)
        bounding_box = scene.bounds
        center = (bounding_box[0] + bounding_box[1]) / 2.0
        scene.apply_translation(-center)

        # Determine the bounding sphere parameters to place the camera correctly
        bounding_sphere_radius = np.linalg.norm(bounding_box[1] - bounding_box[0]) / 2.0

        # Setting up the renderer scene
        render_scene = pyrender.Scene()
        model_nodes = []
        for name, mesh in scene.geometry.items():
            pyrender_mesh = pyrender.Mesh.from_trimesh(mesh)
            node = render_scene.add(pyrender_mesh)
            model_nodes.append(node)

        light = pyrender.DirectionalLight(color=np.ones(3), intensity=3.0)
        render_scene.add(light, pose=np.eye(4))

        yfov = np.pi / 3.0  # Field of view
        camera_distance = bounding_sphere_radius / np.sin(yfov / 2) * 1.5  # Slightly further back
        camera = pyrender.PerspectiveCamera(yfov=yfov)

        # All the camera positions
        camera_pose = np.array([
            [1.0, 0.0, 0.0, 0.0],  # Camera is looking at the center
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, camera_distance],
            [0.0, 0.0, 0.0, 1.0]
        ])
        render_scene.add(camera, pose=camera_pose)

        rotation_planes = [
            (1, 0, 0),  #X-axis
            (0, 1, 0),  #Y-axis
            (0, 0, 1)   #Z-axis
        ]

        renderer = pyrender.OffscreenRenderer(viewport_width=800, viewport_height=600)

        # Rotating and rendering
        frame_index = image_cnt 
        for plane in rotation_planes:
            for angle in angles:
                rotation_matrix = trimesh.transformations.rotation_matrix(
                    np.radians(angle), plane
                )

                # Apply rotation to all model nodes
                for node in model_nodes:
                    # Combine rotation with the original pose
                    original_pose = render_scene.get_pose(node)
                    new_pose = np.dot(rotation_matrix, original_pose)
                    render_scene.set_pose(node, pose=new_pose)

                color, _ = renderer.render(render_scene)

                output_path = os.path.join(output_dir, f'{frame_index}.png')
                imageio.imwrite(output_path, color)

                frame_index += 1

        renderer.delete()
        render_scene.clear()