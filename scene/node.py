from typing import Optional, Callable
from core.matrix import Matrix4
from scene.transform import Transform
from scene.mesh import Mesh

class SceneNode:
    def __init__(self,
                 mesh: Optional[Mesh] = None,
                 transform: Optional[Transform] = None):
        self.mesh = mesh
        self.transform = transform if transform is not None else Transform()
        self.children: list[SceneNode] = []
        
    def add_child(self, node: 'SceneNode') -> None:
        self.children.append(node)
        
    def remove_child(self, node: 'SceneNode') -> None:
        self.children.remove(node)
        
    def traverse(
        self,
        parent_matrix: Matrix4,
        callback: Callable[['SceneNode', Matrix4], None]
    ) -> None:

        local_matrix = self.transform.matrix()
        world_matrix = parent_matrix @ local_matrix

        callback(self, world_matrix)

        for child in self.children:
            child.traverse(world_matrix, callback)
            
# Quick test block
if __name__ == "__main__":
    from core.matrix import Matrix4
    from core.vector import Vector3
    from scene.mesh import Mesh
    from core.quaternion import Quaternion
    import math

    # Build a simple scene: root -> child
    root = SceneNode()
    # Child with a cube mesh, positioned at (2, 0, 0)
    cube_mesh = Mesh.create_cube(1.0)
    transform = Transform(position=Vector3(2, 0, 0))
    child = SceneNode(mesh=cube_mesh, transform=transform)
    root.add_child(child)

    # Callback to print node info
    def print_node(node, world_mat):
        mesh_info = f"Mesh triangles: {len(node.mesh.faces)}" if node.mesh else "No mesh"
        print(f"{mesh_info}, World Matrix:\n{world_mat.to_array()}\n")

    # Traverse with identity as the starting parent matrix
    root.traverse(Matrix4.identity(), print_node)