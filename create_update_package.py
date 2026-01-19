#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RansomGuard 업데이트 패키지 생성 스크립트
Creates update package for RansomGuard
"""

import json
import zipfile
import hashlib
from pathlib import Path
from datetime import datetime

def calculate_sha256(file_path):
    """파일의 SHA256 해시 계산"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def create_update_package(version, base_dir, output_dir):
    """업데이트 패키지 생성"""
    
    base_path = Path(base_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # 패키지 파일명
    package_name = f"ransomguard_v{version}.zip"
    package_path = output_path / package_name
    
    print(f"업데이트 패키지 생성 중: {package_name}")
    print("=" * 50)
    
    # ZIP 파일 생성
    with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        
        # 1. 데이터베이스 파일 추가
        db_file = base_path / "ransomware_db.json"
        if db_file.exists():
            print(f"✓ 추가: ransomware_db.json")
            zipf.write(db_file, "ransomware_db.json")
        else:
            print(f"✗ 없음: ransomware_db.json")
        
        # 2. videos 폴더 추가
        videos_dir = base_path / "videos"
        if videos_dir.exists():
            print(f"\n동영상 파일 추가 중...")
            for video_file in videos_dir.rglob("*"):
                if video_file.is_file():
                    rel_path = video_file.relative_to(base_path)
                    print(f"  ✓ {rel_path}")
                    zipf.write(video_file, str(rel_path))
        else:
            print(f"✗ videos 폴더 없음")
        
        # 3. tools 폴더 추가
        tools_dir = base_path / "tools"
        if tools_dir.exists():
            print(f"\n복구 툴 추가 중...")
            for tool_file in tools_dir.rglob("*"):
                if tool_file.is_file():
                    rel_path = tool_file.relative_to(base_path)
                    print(f"  ✓ {rel_path}")
                    zipf.write(tool_file, str(rel_path))
        else:
            print(f"✗ tools 폴더 없음")
    
    # 패키지 정보
    file_size = package_path.stat().st_size
    sha256_hash = calculate_sha256(package_path)
    
    print("\n" + "=" * 50)
    print(f"✓ 패키지 생성 완료!")
    print(f"  파일: {package_path}")
    print(f"  크기: {file_size / (1024*1024):.2f} MB")
    print(f"  SHA256: {sha256_hash}")
    
    return {
        "package_path": str(package_path),
        "file_size": file_size,
        "sha256": sha256_hash
    }

def create_manifest(version, package_info, changelog_ko, changelog_en, update_url):
    """업데이트 매니페스트 생성"""
    
    manifest = {
        "latest_version": version,
        "update_url": update_url,
        "file_size": package_info["file_size"],
        "sha256": package_info["sha256"],
        "release_date": datetime.now().isoformat(),
        "changelog": {
            "ko": changelog_ko,
            "en": changelog_en
        },
        "required_files": [
            "ransomware_db.json",
            "videos/",
            "tools/"
        ]
    }
    
    return manifest

def main():
    """메인 함수"""
    print("=" * 50)
    print("RansomGuard 업데이트 패키지 생성기")
    print("=" * 50)
    print()
    
    # 설정
    version = input("버전 번호 입력 (예: 5.0.0): ").strip()
    base_dir = input("소스 디렉토리 경로 (예: E:\\My portfolio\\랜섬웨어 정보 프로그램): ").strip()
    output_dir = input("출력 디렉토리 경로 (예: ./packages): ").strip() or "./packages"
    
    print()
    print("변경 사항 입력 (한국어):")
    print("(여러 줄 입력 가능, 빈 줄 입력 시 종료)")
    changelog_ko_lines = []
    while True:
        line = input()
        if not line:
            break
        changelog_ko_lines.append(line)
    changelog_ko = "\n".join(changelog_ko_lines)
    
    print()
    print("변경 사항 입력 (영어):")
    print("(여러 줄 입력 가능, 빈 줄 입력 시 종료)")
    changelog_en_lines = []
    while True:
        line = input()
        if not line:
            break
        changelog_en_lines.append(line)
    changelog_en = "\n".join(changelog_en_lines)
    
    print()
    update_url = input("업데이트 URL (예: https://your-server.com/packages/ransomguard_v5.0.0.zip): ").strip()
    
    print()
    print("=" * 50)
    print("패키지 생성 시작...")
    print("=" * 50)
    print()
    
    # 패키지 생성
    package_info = create_update_package(version, base_dir, output_dir)
    
    # 매니페스트 생성
    manifest = create_manifest(version, package_info, changelog_ko, changelog_en, update_url)
    
    # 매니페스트 저장
    manifest_path = Path(output_dir) / "update_manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print()
    print("=" * 50)
    print(f"✓ 매니페스트 생성 완료!")
    print(f"  파일: {manifest_path}")
    print("=" * 50)
    print()
    print("다음 단계:")
    print("1. 패키지 파일을 서버에 업로드")
    print("2. update_manifest.json을 서버에 업로드")
    print("3. RansomGuard 앱에서 업데이트 확인")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n작업이 취소되었습니다.")
    except Exception as e:
        print(f"\n오류 발생: {e}")
