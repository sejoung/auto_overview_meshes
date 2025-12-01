from typing import List

import unreal

from utils import _log, _warn


# ─────────────────────────────────────────────────────────
# StaticMesh 목록 수집
# ─────────────────────────────────────────────────────────
def list_static_mesh_assets(root: str) -> List[unreal.AssetData]:
    arm = unreal.AssetRegistryHelpers.get_asset_registry()
    flt = unreal.ARFilter(
        package_paths=[unreal.Name(root)],
        recursive_paths=True,
        class_paths=[unreal.StaticMesh.static_class().get_class_path_name()]
    )
    return arm.get_assets(flt)


# ─────────────────────────────────────────────────────────
# 뷰포트 카메라 기준 위치 가져오기
# ─────────────────────────────────────────────────────────
def get_camera_origin_and_yaw(offset_cm: float = 300.0):
    cam_loc, cam_rot = unreal.EditorLevelLibrary.get_level_viewport_camera_info()
    fwd = cam_rot.get_forward_vector()
    origin = cam_loc + fwd * offset_cm
    yaw = cam_rot.yaw
    return origin, yaw


# ─────────────────────────────────────────────────────────
# 그리드 배치
# ─────────────────────────────────────────────────────────
def auto_place_from_folder(folder: str,
                           use_camera_as_origin: bool = True,
                           spacing_cm: float = 200.0,
                           per_row: int = 5):
    """
    folder: '/Game/...' 경로의 StaticMesh들을 전부 레벨에 그리드로 배치.
    use_camera_as_origin: True면 뷰포트 카메라 앞에서 시작, False면 월드 (0,0,0) 기준.
    spacing_cm: 그리드 간격
    per_row: 한 줄에 배치할 개수
    """
    if not folder.startswith("/Game"):
        _warn(f"[AutoOverViewMeshes] Folder must start with /Game: {folder}")
        return

    ads = list_static_mesh_assets(folder)
    if not ads:
        _warn(f"[AutoOverViewMeshes] No StaticMeshes under {folder}")
        return

    ads = sorted(ads, key=lambda a: str(a.asset_name).lower())
    _log(f"[AutoOverViewMeshes] Found {len(ads)} StaticMeshes in {folder}")

    # 배치 시작 위치
    if use_camera_as_origin:
        origin, base_yaw = get_camera_origin_and_yaw(offset_cm=300.0)
    else:
        origin = unreal.Vector(0.0, 0.0, 0.0)
        base_yaw = 0.0

    # 간단한 그리드 배치
    row = 0
    col = 0

    spawned = []

    for idx, ad in enumerate(ads):
        sm = ad.get_asset()
        if not isinstance(sm, unreal.StaticMesh):
            continue

        # 그리드 좌표 → 월드 좌표
        x = col * spacing_cm
        y = row * spacing_cm

        loc = unreal.Vector(origin.x + x, origin.y + y, origin.z)
        rot = unreal.Rotator(0.0, base_yaw, 0.0)

        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.StaticMeshActor, loc, rot
        )
        if not actor:
            _warn(f"[AutoOverViewMeshes] Failed to spawn actor for {ad.get_object_path_string()}")
            continue

        smc = actor.static_mesh_component
        smc.set_static_mesh(sm)
        smc.set_mobility(unreal.ComponentMobility.MOVABLE)

        # 이름/라벨 정리
        actor.set_actor_label(str(ad.asset_name), mark_dirty=True)

        spawned.append(actor)

        # 다음 그리드 위치
        col += 1
        if col >= per_row:
            col = 0
            row += 1

    _log(f"[AutoOverViewMeshes] Spawned {len(spawned)} StaticMeshActors.")


def auto_place_from_selected_folder(folder):
    """
    콘텐츠 브라우저에서 선택된 폴더 기준으로 배치.
    """
    _log(f"[AutoOverViewMeshes] Using folder: {folder}")
    auto_place_from_folder(folder)
