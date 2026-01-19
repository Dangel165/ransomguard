@echo off
chcp 65001 >nul
echo ========================================
echo RansomGuard EXE 빌드
echo ========================================
echo.

REM 현재 디렉토리 표시
echo 현재 작업 디렉토리: %CD%
echo.

REM 파일 존재 확인
if not exist "RansomGuard.py" (
    echo [오류] RansomGuard.py 파일을 찾을 수 없습니다!
    echo 현재 디렉토리: %CD%
    echo.
    echo 이 배치 파일을 RansomGuard.py가 있는 폴더에서 실행해주세요.
    echo.
    pause
    exit /b 1
)

echo [1/3] RansomGuard.py 파일 확인됨
echo.

REM PyInstaller 설치 확인
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo [오류] PyInstaller가 설치되어 있지 않습니다.
    echo PyInstaller를 설치하는 중...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo PyInstaller 설치 실패!
        pause
        exit /b 1
    )
)

echo [2/3] PyInstaller 확인됨
echo.

REM 이전 빌드 정리
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "RansomGuard.spec" del /q RansomGuard.spec

echo [3/3] EXE 파일을 빌드 중...
echo.

REM PyInstaller 실행 (tkinter 명시적 포함)
python -m PyInstaller ^
    --name=RansomGuard ^
    --onefile ^
    --windowed ^
    --clean ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.scrolledtext ^
    --hidden-import=tkinter.messagebox ^
    --hidden-import=tkinter.filedialog ^
    RansomGuard.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo 빌드 실패!
    echo ========================================
    pause
    exit /b 1
)

echo.
echo ========================================
echo 빌드 완료!
echo EXE 파일 위치: dist\RansomGuard.exe
echo ========================================
echo.
echo 참고: 
echo - 생성된 EXE는 dist 폴더에 있습니다
echo - 데이터베이스, 동영상, 복구 툴은 자동 업데이트로 배포됩니다
echo - 업데이트 패키지 생성: python create_update_package.py
echo - 자세한 내용: AUTO_UPDATE_QUICK_GUIDE.md 참조
echo.
pause
