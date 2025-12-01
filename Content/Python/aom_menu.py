import unreal

from placement import auto_place_from_selected_folder
from utils import _log


@unreal.uclass()
class PlacementOptions(unreal.Object):
    start_row = unreal.uproperty(int)
    per_row = unreal.uproperty(int)
    spacing_cm = unreal.uproperty(float)


def _get_selected_content_path() -> str:
    selected_path = unreal.EditorUtilityLibrary.get_current_content_browser_path()
    if selected_path:
        _log(f"selected content path: {selected_path}")
        return str(selected_path)
    else:
        raise Exception("NOT FOUND PATH")


def _get_placement_options():
    # 임시 객체 생성
    obj = PlacementOptions()
    obj.start_row = 0
    obj.per_row = 5
    obj.spacing_cm = 1000.0

    # DetailsView 옵션
    options = [True, False, False, 300, 120, 1.0]

    # 팝업 띄우기
    result = unreal.EditorDialog.show_object_details_view(
        "Placement Options",
        obj,
        options
    )

    # 취소하면 None
    if not result:
        _log("User cancelled.")
        return None

    _log(f"입력된 옵션: start_row={obj.start_row}, per_row={obj.per_row}, spacing_cm={obj.spacing_cm}")
    return obj


def _run():
    src = _get_selected_content_path()
    _log(f"[AutoOverViewMeshes] src={src}")

    options = _get_placement_options()
    if options is None:
        _log("사용자가 옵션 입력을 취소했습니다.")
        return

    auto_place_from_selected_folder(
        folder=src,
        start_row=options.start_row,
        per_row=options.per_row,
        spacing_cm=options.spacing_cm
    )


def register_menus():
    menus = unreal.ToolMenus.get()

    # Content Browser 폴더 우클릭 메뉴
    cb_menu = menus.extend_menu("ContentBrowser.FolderContextMenu")

    # 기존 PathViewFolderContext 섹션에 추가 (다른 플러그인과 충돌 방지)
    section_name = "AutoOverViewMeshes"
    cb_menu.add_section(section_name, "Auto OverView Meshes")

    e = unreal.ToolMenuEntry(
        name="AutoOverViewMeshes",
        type=unreal.MultiBlockType.MENU_ENTRY
    )
    e.set_label("Auto Place Meshes from Folder")
    e.set_tool_tip("폴더의 StaticMesh들을 선택한 액터 위에 그리드로 배치")
    e.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type="",
        string="import aom_menu as M; M._run()"
    )
    cb_menu.add_menu_entry(section_name, e)
    _log("[AutoOverViewMeshes] Menus registered")
