# 🛡️ RansomGuard

**랜섬웨어 정보 데이터베이스 프로그램 / Ransomware Information Database Program**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![Status](https://img.shields.io/badge/team-recruiting-orange)

---

## 📋 목차 / Table of Contents

- [한국어](#한국어)
  - [소개](#소개)
  - [주요 기능](#주요-기능)
  - [설치 방법](#설치-방법)
  - [사용 방법](#사용-방법)
  - [시스템 요구사항](#시스템-요구사항)
- [English](#english)
  - [Introduction](#introduction)
  - [Key Features](#key-features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [System Requirements](#system-requirements)

---

## 한국어

### 소개

RansomGuard는 랜섬웨어에 대한 정보를 제공하고 복구를 돕는 교육용 프로그램입니다. 15개의 주요 랜섬웨어 패밀리에 대한 상세 정보, 복호화 도구, 복구 가이드를 제공합니다.

**⚠️ 현재 상태**: v1.0.0은 기본 데이터베이스와 정보 제공 기능을 포함하고 있습니다. 복구 동영상 및 복구 툴은 향후 업데이트를 통해 점진적으로 추가될 예정입니다.

### 주요 기능

#### 🔍 랜섬웨어 정보 조회
- **15개 랜섬웨어 패밀리 데이터베이스**
  - WannaCry, LockBit 3.0, Ryuk, REvil, Maze
  - Conti, DarkSide, BlackCat, Hive, Ragnar Locker
  - Netwalker, Babuk, Clop, Dharma, STOP
- 각 랜섬웨어의 특징, 암호화 방식, 확장자 정보
- 복호화 가능 여부 및 난이도 표시

#### 🛠️ 복구 도구 실행
- 복호화 도구 다운로드 링크 제공
- No More Ransom, Kaspersky, Avast 등 신뢰할 수 있는 출처
- 원클릭 복구 툴 실행 (tools 폴더에 저장된 경우)
- ⚠️ **현재 준비 중**: 복구 툴은 향후 업데이트를 통해 추가될 예정입니다

#### 🎥 복구 동영상 재생
- 랜섬웨어 복구 과정 동영상 가이드
- 단계별 복구 방법 설명
- 내장 비디오 플레이어
- ⚠️ **현재 준비 중**: 복구 동영상은 향후 업데이트를 통해 추가될 예정입니다

#### 🌐 다국어 지원
- 한국어 / English 지원
- 실시간 언어 전환
- 모든 UI 요소 번역

#### 🔄 자동 업데이트
- GitHub 기반 자동 업데이트 시스템
- 최신 랜섬웨어 정보 자동 다운로드
- 백그라운드 업데이트 확인

### 설치 방법

#### 방법 1: 설치 프로그램 사용 (권장)

1. **설치 파일 다운로드**
   - [GitHub Releases](https://github.com/Dangel165/ransomguard/releases)에서 최신 버전 다운로드
   - `RansomGuard_Setup.exe` 실행

2. **설치 진행**
   - 라이선스 동의
   - 설치 경로 선택 (기본: `C:\Program Files\RansomGuard`)
   - 바탕화면 바로가기 생성 (선택사항)

3. **첫 실행**
   - 프로그램이 자동으로 데이터베이스 다운로드
   - 약 3KB 크기의 데이터 다운로드

#### 방법 2: 소스 코드 실행

```bash
# 저장소 클론
git clone https://github.com/Dangel165/ransomguard.git
cd ransomguard

# 필요한 패키지 설치
pip install tkinter pillow requests

# 프로그램 실행
python RansomGuard.py
```

### 사용 방법

#### 1. 랜섬웨어 검색
- 검색창에 랜섬웨어 이름 입력
- 목록에서 선택하여 상세 정보 확인

#### 2. 상세 정보 보기
- **기본 정보**: 이름, 유형, 위험도
- **기술 정보**: 암호화 방식, 파일 확장자
- **복구 정보**: 복호화 가능 여부, 난이도

#### 3. 복구 도구 사용
- "복구 툴 실행" 버튼 클릭
- 다운로드 링크로 이동하거나 로컬 툴 실행

#### 4. 복구 동영상 시청
- "복구 동영상 재생" 버튼 클릭
- 단계별 복구 가이드 시청

#### 5. 언어 변경
- 상단 메뉴에서 "Language" 선택
- 한국어 ↔ English 전환

#### 6. 업데이트 확인
- "업데이트 확인" 버튼 클릭
- 새 버전이 있으면 자동 다운로드

### 시스템 요구사항

- **운영체제**: Windows 7 이상
- **메모리**: 최소 512MB RAM
- **저장공간**: 50MB 이상
- **인터넷**: 업데이트 확인 및 다운로드용
- **Python**: 3.8 이상 (소스 실행 시)

### 데이터베이스 정보

현재 버전: **4.0.0**

포함된 랜섬웨어:
1. WannaCry - 2017년 대규모 공격
2. LockBit 3.0 - RaaS (Ransomware as a Service)
3. Ryuk - 표적형 공격
4. REvil (Sodinokibi) - 공급망 공격
5. Maze - 이중 갈취
6. Conti - 조직화된 그룹
7. DarkSide - Colonial Pipeline 공격
8. BlackCat (ALPHV) - Rust 기반
9. Hive - 이중 갈취
10. Ragnar Locker - 표적형 공격
11. Netwalker - 교육기관 표적
12. Babuk - 소스코드 유출
13. Clop - 대기업 표적
14. Dharma (Crysis) - RaaS
15. STOP (Djvu) - 광범위 배포

---

## English

### Introduction

RansomGuard is an educational program that provides information about ransomware and helps with recovery. It offers detailed information, decryption tools, and recovery guides for 15 major ransomware families.

**⚠️ Current Status**: v1.0.0 includes basic database and information features. Recovery videos and recovery tools will be gradually added through future updates.

### Key Features

#### 🔍 Ransomware Information Lookup
- **15 Ransomware Family Database**
  - WannaCry, LockBit 3.0, Ryuk, REvil, Maze
  - Conti, DarkSide, BlackCat, Hive, Ragnar Locker
  - Netwalker, Babuk, Clop, Dharma, STOP
- Characteristics, encryption methods, file extensions
- Decryption availability and difficulty indicators

#### 🛠️ Recovery Tool Execution
- Decryption tool download links
- Trusted sources: No More Ransom, Kaspersky, Avast
- One-click recovery tool execution (if stored in tools folder)
- ⚠️ **Coming Soon**: Recovery tools will be added in future updates

#### 🎥 Recovery Video Playback
- Video guides for ransomware recovery process
- Step-by-step recovery instructions
- Built-in video player
- ⚠️ **Coming Soon**: Recovery videos will be added in future updates

#### 🌐 Multi-language Support
- Korean / English support
- Real-time language switching
- All UI elements translated

#### 🔄 Automatic Updates
- GitHub-based automatic update system
- Latest ransomware information auto-download
- Background update checking

### Installation

#### Method 1: Using Installer (Recommended)

1. **Download Installer**
   - Download latest version from [GitHub Releases](https://github.com/Dangel165/ransomguard/releases)
   - Run `RansomGuard_Setup.exe`

2. **Installation Process**
   - Accept license agreement
   - Choose installation path (default: `C:\Program Files\RansomGuard`)
   - Create desktop shortcut (optional)

3. **First Run**
   - Program automatically downloads database
   - Downloads approximately 3KB of data

#### Method 2: Running from Source

```bash
# Clone repository
git clone https://github.com/Dangel165/ransomguard.git
cd ransomguard

# Install required packages
pip install tkinter pillow requests

# Run program
python RansomGuard.py
```

### Usage

#### 1. Search Ransomware
- Enter ransomware name in search box
- Select from list to view details

#### 2. View Details
- **Basic Info**: Name, type, risk level
- **Technical Info**: Encryption method, file extensions
- **Recovery Info**: Decryption availability, difficulty

#### 3. Use Recovery Tools
- Click "Run Recovery Tool" button
- Navigate to download link or run local tool

#### 4. Watch Recovery Videos
- Click "Play Recovery Video" button
- Watch step-by-step recovery guide

#### 5. Change Language
- Select "Language" from top menu
- Switch between Korean ↔ English

#### 6. Check for Updates
- Click "Check for Updates" button
- Automatically downloads if new version available

### System Requirements

- **OS**: Windows 7 or higher
- **Memory**: Minimum 512MB RAM
- **Storage**: 50MB or more
- **Internet**: For update checking and downloads
- **Python**: 3.8 or higher (for source execution)

### Database Information

Current Version: **4.0.0**

Included Ransomware:
1. WannaCry - 2017 massive attack
2. LockBit 3.0 - RaaS (Ransomware as a Service)
3. Ryuk - Targeted attacks
4. REvil (Sodinokibi) - Supply chain attacks
5. Maze - Double extortion
6. Conti - Organized group
7. DarkSide - Colonial Pipeline attack
8. BlackCat (ALPHV) - Rust-based
9. Hive - Double extortion
10. Ragnar Locker - Targeted attacks
11. Netwalker - Educational institutions target
12. Babuk - Source code leaked
13. Clop - Large enterprise target
14. Dharma (Crysis) - RaaS
15. STOP (Djvu) - Widespread distribution

---

## 📸 스크린샷 / Screenshots

### 메인 화면 / Main Screen
- 랜섬웨어 목록 및 검색 기능
- Ransomware list and search functionality

### 상세 정보 / Details View
- 랜섬웨어 상세 정보 표시
- Detailed ransomware information display

### 복구 도구 / Recovery Tools
- 복구 툴 실행 및 다운로드
- Recovery tool execution and download

---

## 🔒 보안 및 개인정보 / Security & Privacy

- ✅ 개인정보 수집 없음 / No personal data collection
- ✅ 오픈소스 / Open source
- ✅ 안전한 다운로드 (GitHub) / Safe downloads (GitHub)
- ✅ 바이러스 없음 / Virus-free

---

## 🤝 기여 / Contributing

버그 리포트, 기능 제안, 풀 리퀘스트를 환영합니다!
Bug reports, feature suggestions, and pull requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 라이선스 / License

이 프로젝트는 Apache License 2.0 하에 배포됩니다.
This project is licensed under the Apache License 2.0.

자세한 내용은 [LICENSE.txt](LICENSE.txt)를 참조하세요.
See [LICENSE.txt](LICENSE.txt) for details.

---

## 👨‍💻 개발 / Development

**Project Lead: Dangel**

- GitHub: [@Dangel165](https://github.com/Dangel165)
- Repository: [ransomguard](https://github.com/Dangel165/ransomguard)

**팀 멤버 모집 중 / Team Members Wanted**

현재 개발팀을 구성하고 있습니다. 함께 프로젝트를 발전시킬 팀원을 찾고 있습니다!
Currently building a development team. Looking for team members to grow this project together!

---

## ⚠️ 면책 조항 / Disclaimer

본 소프트웨어는 교육 및 정보 제공 목적으로만 제작되었습니다. 실제 랜섬웨어 감염 시 전문가의 도움을 받으시기 바랍니다.

This software is created for educational and informational purposes only. For actual ransomware infections, please seek professional assistance.

---

## 📅 업데이트 내역 / Update History

### v1.0.0 (2026-01-20)
- ✨ 초기 릴리즈 / Initial release
- 📦 15개 랜섬웨어 데이터베이스 / 15 ransomware database
- 🌐 한국어/영어 지원 / Korean/English support
- 🔄 자동 업데이트 시스템 / Automatic update system
- 🛠️ 복구 도구 통합 (준비 중) / Recovery tool integration (coming soon)
- 🎥 복구 동영상 재생 (준비 중) / Recovery video playback (coming soon)

### 향후 업데이트 계획 / Future Updates
- 📹 복구 동영상 콘텐츠 추가 / Add recovery video content
- 🔧 복구 툴 로컬 실행 기능 / Local recovery tool execution
- 📊 더 많은 랜섬웨어 정보 추가 / Add more ransomware information
- 🎨 UI/UX 개선 / UI/UX improvements

---

**Made with ❤️ by Dangel**

**License:** Apache 2.0 | **Status:** Team Members Wanted
