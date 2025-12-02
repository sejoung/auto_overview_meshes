# AutoOverViewMeshes

Unreal Engine 에디터 플러그인으로, 선택한 폴더의 StaticMesh들을 레벨에 그리드 형태로 자동 배치합니다.

## 기능

- Content Browser에서 폴더 우클릭 → **AutoOverViewMeshes** 메뉴로 실행
- 선택한 액터 위에 메쉬들을 그리드로 배치
- 배치 옵션 설정 가능:
  - **start_row**: 시작 row 번호 (0부터 시작)
  - **per_row**: 한 줄에 배치할 메쉬 개수
  - **spacing_cm**: 그리드 간격 (cm)

## 사용법

1. 레벨 뷰포트에서 배치 기준이 될 메쉬(바닥 등)를 선택
2. Content Browser에서 StaticMesh가 있는 폴더 우클릭
3. **AutoOverViewMeshes** 메뉴 클릭
4. Placement Options 다이얼로그에서 옵션 설정 후 확인
5. 선택한 메쉬 위에 그리드로 배치됨

## 설치

1. 플러그인 폴더를 프로젝트의 `Plugins` 디렉토리에 복사
2. 에디터 재시작

## 요구사항

- Unreal Engine 5.x
- PythonScriptPlugin (활성화 필요)
- EditorScriptingUtilities (활성화 필요)

## 참고

- [에디터 Python 스크립팅의 자동 완성 세팅](https://dev.epicgames.com/documentation/ko-kr/unreal-engine/setting-up-autocomplete-for-unreal-editor-python-scripting)