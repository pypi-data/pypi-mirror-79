from inoft_vocal_engine.permissions.permission_model import PermissionModel

project_diagrams_nodes_read_all = PermissionModel(
    expression="{requester_account_id}:{account_project_id}:diagrams:nodes:read:all",
    display_name="project_diagrams_nodes_read_all", description="Fait des trucs cool"
)
project_diagrams_nodes_update_all = PermissionModel(
    expression="{requester_account_id}:{account_project_id}:diagrams:nodes:update:all",
    display_name="project_diagrams_nodes_update_all", description="lel"
)
project_diagrams_nodes_add_all = PermissionModel(
    expression="{requester_account_id}:{account_project_id}:diagrams:nodes:add:all",
    display_name="project_diagrams_nodes_add_all", description=""
)
project_diagrams_nodes_remove_all = PermissionModel(
    expression="{requester_account_id}:{account_project_id}:diagrams:nodes:remove:all",
    display_name="project_diagrams_nodes_remove_all", description=""
)
