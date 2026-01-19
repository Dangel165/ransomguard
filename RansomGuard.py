#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RansomGuard - 랜섬웨어 정보 데이터베이스 (다국어 지원)
RansomGuard - Ransomware Information Database (Multi-language Support)

제작자: Dangel
Author: Dangel
"""

import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from datetime import datetime
import webbrowser
from pathlib import Path
import subprocess
import os
import sys
import urllib.request
import threading
import shutil
import zipfile
import hashlib

class RansomGuardApp:
    def __init__(self, root):
        self.root = root
        self.current_lang = "ko"  # 기본 언어: 한국어
        
        # 언어별 텍스트
        self.translations = {
            "ko": {
                "title": "RansomGuard - 랜섬웨어 정보 데이터베이스",
                "db_version": "데이터베이스 버전",
                "last_updated": "마지막 업데이트",
                "total_count": "총",
                "ransomware_count": "개 랜섬웨어",
                "ransomware_list": "랜섬웨어 목록",
                "search": "검색:",
                "detail_info": "상세 정보",
                "basic_info": "📋 기본 정보",
                "family": "패밀리",
                "aliases": "별칭",
                "first_seen": "최초 발견",
                "severity": "위험도",
                "extensions": "🔒 암호화 파일 확장자",
                "ransom_notes": "📝 랜섬 노트 파일명",
                "decryption": "🔓 복호화 가능 여부",
                "decryption_available": "✅ 복호화 도구 사용 가능",
                "decryption_unavailable": "❌ 현재 복호화 도구 없음",
                "decryption_tools": "🛠️ 복호화 도구",
                "tool_name": "도구명",
                "provider": "제공",
                "effectiveness": "효과",
                "requirements": "요구사항",
                "download": "다운로드",
                "additional_info": "ℹ️ 추가 정보",
                "references": "🔗 참고 자료",
                "language": "언어",
                "switch_to_en": "English",
                "switch_to_ko": "한국어",
                "recovery_video": "🎥 복구 동영상",
                "play_video": "동영상 재생",
                "run_tool": "복구 툴 실행",
                "video_not_found": "동영상 파일을 찾을 수 없습니다",
                "tool_not_found": "복구 툴을 찾을 수 없습니다",
                "tool_path": "툴 경로",
                "video_uploader": "동영상 제공",
                "tool_guide_creator": "복구 가이드 제작",
                "tool_original_author": "복구툴 원작자",
                "check_update": "업데이트 확인",
                "update_available": "업데이트 사용 가능",
                "update_now": "지금 업데이트",
                "no_update": "최신 버전입니다",
                "updating": "업데이트 중...",
                "update_success": "업데이트 완료",
                "update_failed": "업데이트 실패",
                "auto_update": "자동 업데이트",
                "about": "정보",
                "developer": "제작자"
            },
            "en": {
                "title": "RansomGuard - Ransomware Information Database",
                "db_version": "Database Version",
                "last_updated": "Last Updated",
                "total_count": "Total",
                "ransomware_count": "Ransomware",
                "ransomware_list": "Ransomware List",
                "search": "Search:",
                "detail_info": "Detail Information",
                "basic_info": "📋 Basic Information",
                "family": "Family",
                "aliases": "Aliases",
                "first_seen": "First Seen",
                "severity": "Severity",
                "extensions": "🔒 Encrypted File Extensions",
                "ransom_notes": "📝 Ransom Note Filenames",
                "decryption": "🔓 Decryption Availability",
                "decryption_available": "✅ Decryption Tool Available",
                "decryption_unavailable": "❌ No Decryption Tool Available",
                "decryption_tools": "🛠️ Decryption Tools",
                "tool_name": "Tool Name",
                "provider": "Provider",
                "effectiveness": "Effectiveness",
                "requirements": "Requirements",
                "download": "Download",
                "additional_info": "ℹ️ Additional Information",
                "references": "🔗 References",
                "language": "Language",
                "switch_to_en": "English",
                "switch_to_ko": "한국어",
                "recovery_video": "🎥 Recovery Video",
                "play_video": "Play Video",
                "run_tool": "Run Recovery Tool",
                "video_not_found": "Video file not found",
                "tool_not_found": "Recovery tool not found",
                "tool_path": "Tool Path",
                "video_uploader": "Video Provided by",
                "tool_guide_creator": "Recovery Guide by",
                "tool_original_author": "Tool Original Author",
                "check_update": "Check Update",
                "update_available": "Update Available",
                "update_now": "Update Now",
                "no_update": "Up to date",
                "updating": "Updating...",
                "update_success": "Update Complete",
                "update_failed": "Update Failed",
                "auto_update": "Auto Update",
                "about": "About",
                "developer": "Developer"
            }
        }
        
        # 업데이트 URL 설정 (전체 패키지 매니페스트)
        # GitHub Releases 사용 예시:
        self.update_manifest_url = "https://raw.githubusercontent.com/YOUR_USERNAME/ransomguard-updates/main/update_manifest.json"
        
        # 또는 Google Drive / 자체 서버 사용
        # self.update_manifest_url = "https://your-server.com/ransomguard/update_manifest.json"
        
        self.update_title()
        self.root.geometry("1200x700")
        
        # 데이터 로드
        self.ransomware_data = self.load_data()
        
        # UI 구성
        self.setup_ui()
        
        # 자동 업데이트 확인 (백그라운드)
        self.check_for_updates_background()
        
    def update_title(self):
        """창 제목 업데이트"""
        self.root.title(self.translations[self.current_lang]["title"])
        
    def t(self, key):
        """번역 텍스트 가져오기"""
        return self.translations[self.current_lang].get(key, key)
        
    def switch_language(self):
        """언어 전환"""
        self.current_lang = "en" if self.current_lang == "ko" else "ko"
        self.update_title()
        self.refresh_ui()
        
    def load_data(self):
        """랜섬웨어 데이터베이스 로드"""
        # EXE 실행 파일의 위치를 기준으로 경로 설정
        if getattr(sys, 'frozen', False):
            # PyInstaller로 빌드된 EXE인 경우
            app_dir = Path(sys.executable).parent
        else:
            # 개발 환경에서 .py 파일로 실행하는 경우
            app_dir = Path(__file__).parent
        
        db_path = app_dir / "ransomware_db.json"
        
        # 데이터베이스 기본 디렉토리 저장
        self.db_base_dir = app_dir
        
        if not db_path.exists():
            return {
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
                "ransomware_families": []
            }
        
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
            return {"ransomware_families": []}
    
    def setup_ui(self):
        """UI 구성"""
        # 상단 프레임
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        # 정보 표시
        info_frame = ttk.Frame(top_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        version = self.ransomware_data.get("version", "N/A")
        last_updated = self.ransomware_data.get("last_updated", "N/A")
        total_count = len(self.ransomware_data.get("ransomware_families", []))
        
        info_text = f"{self.t('db_version')}: {version} | {self.t('last_updated')}: {last_updated} | {self.t('total_count')} {total_count}{self.t('ransomware_count')} | {self.t('developer')}: Dangel"
        self.info_label = ttk.Label(info_frame, text=info_text, font=("맑은 고딕", 9))
        self.info_label.pack()
        
        # 언어 전환 버튼
        lang_frame = ttk.Frame(top_frame)
        lang_frame.pack(side=tk.RIGHT)
        
        ttk.Label(lang_frame, text=f"{self.t('language')}:", font=("맑은 고딕", 9)).pack(side=tk.LEFT, padx=5)
        self.lang_button = ttk.Button(
            lang_frame,
            text=self.t('switch_to_en') if self.current_lang == "ko" else self.t('switch_to_ko'),
            command=self.switch_language,
            width=10
        )
        self.lang_button.pack(side=tk.LEFT)
        
        # 업데이트 버튼
        self.update_button = ttk.Button(
            lang_frame,
            text=self.t('check_update'),
            command=self.check_for_updates,
            width=12
        )
        self.update_button.pack(side=tk.LEFT, padx=5)
        
        # 메인 컨테이너
        self.main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 왼쪽: 랜섬웨어 목록
        self.left_frame = ttk.Frame(self.main_container)
        self.main_container.add(self.left_frame, weight=1)
        
        self.list_title = ttk.Label(self.left_frame, text=self.t('ransomware_list'), font=("맑은 고딕", 11, "bold"))
        self.list_title.pack(pady=5)
        
        # 검색
        search_frame = ttk.Frame(self.left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.search_label = ttk.Label(search_frame, text=self.t('search'))
        self.search_label.pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_list)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # 리스트박스
        list_frame = ttk.Frame(self.left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.ransomware_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("맑은 고딕", 10),
            selectmode=tk.SINGLE
        )
        self.ransomware_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.ransomware_listbox.yview)
        
        self.ransomware_listbox.bind('<<ListboxSelect>>', self.on_select)
        
        # 오른쪽: 상세 정보
        self.right_frame = ttk.Frame(self.main_container)
        self.main_container.add(self.right_frame, weight=2)
        
        self.detail_title = ttk.Label(self.right_frame, text=self.t('detail_info'), font=("맑은 고딕", 11, "bold"))
        self.detail_title.pack(pady=5)
        
        # 상세 정보 표시 영역
        self.detail_text = scrolledtext.ScrolledText(
            self.right_frame,
            wrap=tk.WORD,
            font=("맑은 고딕", 10),
            padx=10,
            pady=10
        )
        self.detail_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 액션 버튼 프레임 (동영상 재생, 복구 툴 실행)
        self.action_frame = ttk.Frame(self.right_frame)
        self.action_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.video_button = ttk.Button(
            self.action_frame,
            text=self.t('play_video'),
            command=self.play_recovery_video,
            state=tk.DISABLED
        )
        self.video_button.pack(side=tk.LEFT, padx=5)
        
        self.tool_button = ttk.Button(
            self.action_frame,
            text=self.t('run_tool'),
            command=self.run_recovery_tool,
            state=tk.DISABLED
        )
        self.tool_button.pack(side=tk.LEFT, padx=5)
        
        # 현재 선택된 랜섬웨어 정보 저장
        self.current_family = None
        
        # 태그 설정
        self.detail_text.tag_config("title", font=("맑은 고딕", 14, "bold"), foreground="#2c3e50")
        self.detail_text.tag_config("section", font=("맑은 고딕", 11, "bold"), foreground="#34495e")
        self.detail_text.tag_config("critical", foreground="#e74c3c", font=("맑은 고딕", 10, "bold"))
        self.detail_text.tag_config("high", foreground="#e67e22", font=("맑은 고딕", 10, "bold"))
        self.detail_text.tag_config("available", foreground="#27ae60", font=("맑은 고딕", 10, "bold"))
        self.detail_text.tag_config("unavailable", foreground="#c0392b", font=("맑은 고딕", 10, "bold"))
        self.detail_text.tag_config("link", foreground="#3498db", underline=True)
        
        # 목록 채우기
        self.populate_list()
        
    def refresh_ui(self):
        """UI 새로고침"""
        # 정보 레이블 업데이트
        version = self.ransomware_data.get("version", "N/A")
        last_updated = self.ransomware_data.get("last_updated", "N/A")
        total_count = len(self.ransomware_data.get("ransomware_families", []))
        
        info_text = f"{self.t('db_version')}: {version} | {self.t('last_updated')}: {last_updated} | {self.t('total_count')} {total_count}{self.t('ransomware_count')} | {self.t('developer')}: Dangel"
        self.info_label.config(text=info_text)
        
        # 언어 버튼 업데이트
        self.lang_button.config(text=self.t('switch_to_en') if self.current_lang == "ko" else self.t('switch_to_ko'))
        
        # 제목 업데이트
        self.list_title.config(text=self.t('ransomware_list'))
        self.detail_title.config(text=self.t('detail_info'))
        self.search_label.config(text=self.t('search'))
        
        # 선택된 항목 다시 표시
        selection = self.ransomware_listbox.curselection()
        if selection:
            self.on_select(None)
    
    def populate_list(self):
        """랜섬웨어 목록 채우기"""
        self.ransomware_listbox.delete(0, tk.END)
        
        families = self.ransomware_data.get("ransomware_families", [])
        for family in families:
            name = family.get("name", "Unknown")
            variant = family.get("variant")
            display_name = f"{name} {variant}" if variant else name
            self.ransomware_listbox.insert(tk.END, display_name)
    
    def filter_list(self, *args):
        """검색 필터"""
        search_term = self.search_var.get().lower()
        self.ransomware_listbox.delete(0, tk.END)
        
        families = self.ransomware_data.get("ransomware_families", [])
        for family in families:
            name = family.get("name", "Unknown")
            variant = family.get("variant", "")
            aliases = " ".join(family.get("aliases", []))
            
            search_text = f"{name} {variant} {aliases}".lower()
            
            if search_term in search_text:
                display_name = f"{name} {variant}" if variant else name
                self.ransomware_listbox.insert(tk.END, display_name)
    
    def on_select(self, event):
        """랜섬웨어 선택 시"""
        selection = self.ransomware_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        
        # 필터링된 목록에서 실제 인덱스 찾기
        search_term = self.search_var.get().lower()
        families = self.ransomware_data.get("ransomware_families", [])
        
        if search_term:
            filtered_families = []
            for family in families:
                name = family.get("name", "Unknown")
                variant = family.get("variant", "")
                aliases = " ".join(family.get("aliases", []))
                search_text = f"{name} {variant} {aliases}".lower()
                
                if search_term in search_text:
                    filtered_families.append(family)
            
            if index < len(filtered_families):
                self.display_details(filtered_families[index])
        else:
            if index < len(families):
                self.display_details(families[index])
    
    def display_details(self, family):
        """상세 정보 표시"""
        self.current_family = family  # 현재 선택된 랜섬웨어 저장
        
        self.detail_text.config(state=tk.NORMAL)
        self.detail_text.delete(1.0, tk.END)
        
        # 제목
        name = family.get("name", "Unknown")
        variant = family.get("variant")
        title = f"{name} {variant}" if variant else name
        self.detail_text.insert(tk.END, f"{title}\n\n", "title")
        
        # 기본 정보
        self.detail_text.insert(tk.END, f"{self.t('basic_info')}\n", "section")
        self.detail_text.insert(tk.END, f"{self.t('family')}: {family.get('family', 'N/A')}\n")
        
        aliases = family.get("aliases", [])
        if aliases:
            self.detail_text.insert(tk.END, f"{self.t('aliases')}: {', '.join(aliases)}\n")
        
        first_seen = family.get("first_seen", "N/A")
        self.detail_text.insert(tk.END, f"{self.t('first_seen')}: {first_seen}\n")
        
        severity = family.get("severity", "unknown")
        severity_text = f"{self.t('severity')}: {severity.upper()}\n"
        if severity == "critical":
            self.detail_text.insert(tk.END, severity_text, "critical")
        elif severity == "high":
            self.detail_text.insert(tk.END, severity_text, "high")
        else:
            self.detail_text.insert(tk.END, severity_text)
        
        self.detail_text.insert(tk.END, "\n")
        
        # 파일 확장자
        extensions = family.get("known_extensions", [])
        if extensions:
            self.detail_text.insert(tk.END, f"{self.t('extensions')}\n", "section")
            self.detail_text.insert(tk.END, f"{', '.join(extensions)}\n\n")
        
        # 랜섬 노트
        note_files = family.get("ransom_note_filenames", [])
        if note_files:
            self.detail_text.insert(tk.END, f"{self.t('ransom_notes')}\n", "section")
            for note in note_files:
                self.detail_text.insert(tk.END, f"  • {note}\n")
            self.detail_text.insert(tk.END, "\n")
        
        # 복호화 가능 여부
        self.detail_text.insert(tk.END, f"{self.t('decryption')}\n", "section")
        decryption_available = family.get("decryption_available", False)
        if decryption_available:
            self.detail_text.insert(tk.END, f"{self.t('decryption_available')}\n\n", "available")
            
            # 복호화 도구
            tools = family.get("decryption_tools", [])
            if tools:
                self.detail_text.insert(tk.END, f"{self.t('decryption_tools')}\n", "section")
                for tool in tools:
                    tool_name = tool.get("name", "Unknown")
                    provider = tool.get("provider", "Unknown")
                    effectiveness = tool.get("effectiveness", "unknown")
                    
                    self.detail_text.insert(tk.END, f"\n{self.t('tool_name')}: {tool_name}\n")
                    self.detail_text.insert(tk.END, f"{self.t('provider')}: {provider}\n")
                    self.detail_text.insert(tk.END, f"{self.t('effectiveness')}: {effectiveness}\n")
                    
                    requirements = tool.get("requirements")
                    if requirements:
                        self.detail_text.insert(tk.END, f"{self.t('requirements')}: {requirements}\n")
                    
                    download_url = tool.get("download_url")
                    if download_url:
                        self.detail_text.insert(tk.END, f"{self.t('download')}: ")
                        self.detail_text.insert(tk.END, download_url, "link")
                        self.detail_text.insert(tk.END, "\n")
                        # 링크 클릭 이벤트
                        self.detail_text.tag_bind("link", "<Button-1>", 
                                                 lambda e, url=download_url: webbrowser.open(url))
                
                self.detail_text.insert(tk.END, "\n")
        else:
            self.detail_text.insert(tk.END, f"{self.t('decryption_unavailable')}\n\n", "unavailable")
        
        # 복구 동영상
        video_path = family.get("recovery_video_path")
        if video_path:
            self.detail_text.insert(tk.END, f"{self.t('recovery_video')}\n", "section")
            self.detail_text.insert(tk.END, f"{video_path}\n")
            
            # 동영상 제공자
            video_uploader = family.get("video_uploader")
            if video_uploader:
                self.detail_text.insert(tk.END, f"{self.t('video_uploader')}: {video_uploader}\n")
            
            self.detail_text.insert(tk.END, "\n")
            self.video_button.config(state=tk.NORMAL)
        else:
            self.video_button.config(state=tk.DISABLED)
        
        # 복구 툴 경로
        tool_path = family.get("recovery_tool_path")
        if tool_path:
            self.detail_text.insert(tk.END, f"{self.t('tool_path')}\n", "section")
            self.detail_text.insert(tk.END, f"{tool_path}\n")
            
            # 복구툴 원작자
            tool_original_author = family.get("tool_original_author")
            if tool_original_author:
                self.detail_text.insert(tk.END, f"{self.t('tool_original_author')}: {tool_original_author}\n")
            
            # 복구 가이드 제작자
            tool_guide_creator = family.get("tool_guide_creator")
            if tool_guide_creator:
                self.detail_text.insert(tk.END, f"{self.t('tool_guide_creator')}: {tool_guide_creator}\n")
            
            self.detail_text.insert(tk.END, "\n")
            self.tool_button.config(state=tk.NORMAL)
        else:
            self.tool_button.config(state=tk.DISABLED)
        
        # 추가 정보
        notes = family.get("notes")
        if notes:
            self.detail_text.insert(tk.END, f"{self.t('additional_info')}\n", "section")
            self.detail_text.insert(tk.END, f"{notes}\n\n")
        
        # 참고 자료
        references = family.get("references", [])
        if references:
            self.detail_text.insert(tk.END, f"{self.t('references')}\n", "section")
            for ref in references:
                self.detail_text.insert(tk.END, f"  • ")
                self.detail_text.insert(tk.END, ref, "link")
                self.detail_text.insert(tk.END, "\n")
                # 링크 클릭 이벤트
                self.detail_text.tag_bind("link", "<Button-1>", 
                                         lambda e, url=ref: webbrowser.open(url))
        
        self.detail_text.config(state=tk.DISABLED)
    
    def play_recovery_video(self):
        """복구 동영상 재생"""
        if not self.current_family:
            return
        
        video_path = self.current_family.get("recovery_video_path")
        if not video_path:
            messagebox.showwarning(self.t('play_video'), self.t('video_not_found'))
            return
        
        # 상대 경로를 절대 경로로 변환
        video_file = self.db_base_dir / video_path
        
        if not video_file.exists():
            messagebox.showerror(self.t('play_video'), f"{self.t('video_not_found')}\n{video_file}")
            return
        
        try:
            # Windows에서 기본 비디오 플레이어로 재생
            os.startfile(str(video_file))
        except Exception as e:
            messagebox.showerror(self.t('play_video'), f"Error: {e}")
    
    def run_recovery_tool(self):
        """복구 툴 실행"""
        if not self.current_family:
            return
        
        tool_path = self.current_family.get("recovery_tool_path")
        if not tool_path:
            messagebox.showwarning(self.t('run_tool'), self.t('tool_not_found'))
            return
        
        # 상대 경로를 절대 경로로 변환
        tool_file = self.db_base_dir / tool_path
        
        if not tool_file.exists():
            messagebox.showerror(self.t('run_tool'), f"{self.t('tool_not_found')}\n{tool_file}")
            return
        
        try:
            # 복구 툴 실행
            subprocess.Popen([str(tool_file)], shell=True)
            messagebox.showinfo(self.t('run_tool'), f"복구 툴을 실행했습니다:\n{tool_file.name}")
        except Exception as e:
            messagebox.showerror(self.t('run_tool'), f"Error: {e}")
    
    def check_for_updates_background(self):
        """백그라운드에서 업데이트 확인 (전체 패키지)"""
        def check():
            try:
                manifest = self.check_update_manifest()
                if manifest:
                    latest_version = manifest.get("latest_version", "0.0.0")
                    self.root.after(0, lambda: self.show_update_notification(latest_version, manifest))
            except:
                pass  # 조용히 실패
        
        thread = threading.Thread(target=check, daemon=True)
        thread.start()
    
    def check_update_manifest(self):
        """업데이트 매니페스트 확인"""
        try:
            with urllib.request.urlopen(self.update_manifest_url, timeout=10) as response:
                manifest = json.loads(response.read().decode('utf-8'))
                
                latest_version = manifest.get("latest_version", "0.0.0")
                current_version = self.ransomware_data.get("version", "0.0.0")
                
                if self.compare_versions(latest_version, current_version) > 0:
                    return manifest
                return None
        except Exception as e:
            print(f"매니페스트 확인 실패: {e}")
            return None
    
    def check_for_updates(self):
        """수동 업데이트 확인"""
        self.update_button.config(state=tk.DISABLED, text=self.t('updating'))
        
        def check():
            try:
                manifest = self.check_update_manifest()
                if manifest:
                    latest_version = manifest.get("latest_version", "0.0.0")
                    self.root.after(0, lambda: self.prompt_update(manifest, latest_version))
                else:
                    current_version = self.ransomware_data.get("version", "0.0.0")
                    self.root.after(0, lambda: messagebox.showinfo(
                        self.t('check_update'),
                        f"{self.t('no_update')}\n{self.t('db_version')}: {current_version}"
                    ))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    self.t('check_update'),
                    f"{self.t('update_failed')}\n{str(e)}"
                ))
            finally:
                self.root.after(0, lambda: self.update_button.config(
                    state=tk.NORMAL,
                    text=self.t('check_update')
                ))
        
        thread = threading.Thread(target=check, daemon=True)
        thread.start()
    
    def show_update_notification(self, new_version, manifest):
        """업데이트 알림 표시 (전체 패키지)"""
        current_version = self.ransomware_data.get("version", "0.0.0")
        changelog = manifest.get("changelog", {}).get(self.current_lang, "")
        file_size_mb = manifest.get("file_size", 0) / (1024 * 1024)
        
        message = (
            f"{self.t('update_available')}!\n\n"
            f"현재 버전: {current_version}\n"
            f"최신 버전: {new_version}\n"
            f"다운로드 크기: {file_size_mb:.1f} MB\n\n"
            f"변경 사항:\n{changelog}\n\n"
            f"{self.t('update_now')}?"
        )
        
        result = messagebox.askyesno(
            self.t('update_available'),
            message
        )
        
        if result:
            self.perform_full_update(manifest)
    
    def prompt_update(self, manifest, new_version):
        """업데이트 확인 프롬프트 (전체 패키지)"""
        current_version = self.ransomware_data.get("version", "0.0.0")
        changelog = manifest.get("changelog", {}).get(self.current_lang, "")
        file_size_mb = manifest.get("file_size", 0) / (1024 * 1024)
        
        message = (
            f"{self.t('update_available')}!\n\n"
            f"현재 버전: {current_version}\n"
            f"최신 버전: {new_version}\n"
            f"다운로드 크기: {file_size_mb:.1f} MB\n\n"
            f"변경 사항:\n{changelog}\n\n"
            f"{self.t('update_now')}?"
        )
        
        result = messagebox.askyesno(
            self.t('update_available'),
            message
        )
        
        if result:
            self.perform_full_update(manifest)
    
    def perform_full_update(self, manifest):
        """전체 패키지 업데이트 수행"""
        self.update_button.config(state=tk.DISABLED, text=self.t('updating'))
        
        def update():
            try:
                # 1. 다운로드
                zip_path = self.download_update_package(manifest)
                
                if not zip_path:
                    raise Exception("다운로드 실패" if self.current_lang == "ko" else "Download failed")
                
                # 2. 체크섬 검증 (선택사항)
                expected_hash = manifest.get("sha256")
                if expected_hash and not self.verify_package_checksum(zip_path, expected_hash):
                    zip_path.unlink()
                    raise Exception("체크섬 불일치" if self.current_lang == "ko" else "Checksum mismatch")
                
                # 3. 설치
                if not self.install_update_package(zip_path):
                    raise Exception("설치 실패" if self.current_lang == "ko" else "Installation failed")
                
                # 4. 데이터 다시 로드
                self.ransomware_data = self.load_data()
                self.root.after(0, lambda: self.refresh_after_update())
                
                # 5. 완료 메시지
                self.root.after(0, lambda: messagebox.showinfo(
                    self.t('update_success'),
                    f"{self.t('update_success')}!\n"
                    f"{self.t('db_version')}: {self.ransomware_data.get('version', 'N/A')}\n\n"
                    f"데이터베이스, 동영상, 복구 툴이 모두 업데이트되었습니다."
                    if self.current_lang == "ko" else
                    f"{self.t('update_success')}!\n"
                    f"{self.t('db_version')}: {self.ransomware_data.get('version', 'N/A')}\n\n"
                    f"Database, videos, and recovery tools have been updated."
                ))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    self.t('update_failed'),
                    f"{self.t('update_failed')}\n{str(e)}"
                ))
            finally:
                self.root.after(0, lambda: self.update_button.config(
                    state=tk.NORMAL,
                    text=self.t('check_update')
                ))
        
        thread = threading.Thread(target=update, daemon=True)
        thread.start()
    
    def download_update_package(self, manifest):
        """업데이트 패키지 다운로드 (진행률 표시)"""
        update_url = manifest.get("update_url")
        file_size = manifest.get("file_size", 0)
        
        # 임시 파일 경로
        temp_zip = self.db_base_dir / "update_temp.zip"
        
        # 진행률 창 생성
        progress_window = tk.Toplevel(self.root)
        progress_window.title("업데이트 다운로드 중..." if self.current_lang == "ko" else "Downloading Update...")
        progress_window.geometry("400x120")
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        # 진행률 레이블
        progress_label = ttk.Label(
            progress_window, 
            text="다운로드 준비 중..." if self.current_lang == "ko" else "Preparing download...",
            font=("맑은 고딕", 10)
        )
        progress_label.pack(pady=10)
        
        # 진행률 바
        progress_bar = ttk.Progressbar(progress_window, length=350, mode='determinate')
        progress_bar.pack(pady=10)
        
        # 상태 레이블
        status_label = ttk.Label(progress_window, text="0%", font=("맑은 고딕", 9))
        status_label.pack(pady=5)
        
        download_success = [False]
        
        def update_progress(count, block_size, total_size):
            """진행률 업데이트"""
            if total_size > 0:
                downloaded = count * block_size
                percent = min((downloaded / total_size) * 100, 100)
                
                progress_bar['value'] = percent
                progress_label.config(
                    text=f"다운로드 중... {downloaded / (1024*1024):.1f} MB / {total_size / (1024*1024):.1f} MB"
                    if self.current_lang == "ko" else
                    f"Downloading... {downloaded / (1024*1024):.1f} MB / {total_size / (1024*1024):.1f} MB"
                )
                status_label.config(text=f"{percent:.1f}%")
                progress_window.update()
        
        def download():
            """다운로드 실행"""
            try:
                urllib.request.urlretrieve(
                    update_url,
                    temp_zip,
                    reporthook=update_progress
                )
                download_success[0] = True
            except Exception as e:
                print(f"다운로드 실패: {e}")
                download_success[0] = False
            finally:
                progress_window.destroy()
        
        download_thread = threading.Thread(target=download, daemon=True)
        download_thread.start()
        
        progress_window.wait_window()
        
        return temp_zip if download_success[0] and temp_zip.exists() else None
    
    def verify_package_checksum(self, zip_path, expected_hash):
        """패키지 체크섬 검증"""
        if not expected_hash:
            return True
        
        sha256_hash = hashlib.sha256()
        with open(zip_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest() == expected_hash
    
    def install_update_package(self, zip_path):
        """업데이트 패키지 설치"""
        try:
            # 백업 디렉토리 생성
            backup_dir = self.db_base_dir / "backup"
            backup_dir.mkdir(exist_ok=True)
            
            # 타임스탬프로 백업 파일명 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_zip = backup_dir / f"backup_{timestamp}.zip"
            
            # 현재 파일들 백업
            with zipfile.ZipFile(backup_zip, 'w', zipfile.ZIP_DEFLATED) as backup:
                # 데이터베이스 백업
                db_file = self.db_base_dir / "ransomware_db.json"
                if db_file.exists():
                    backup.write(db_file, "ransomware_db.json")
                
                # videos 폴더 백업
                videos_dir = self.db_base_dir / "videos"
                if videos_dir.exists():
                    for video_file in videos_dir.rglob("*"):
                        if video_file.is_file():
                            rel_path = video_file.relative_to(self.db_base_dir)
                            backup.write(video_file, str(rel_path))
                
                # tools 폴더 백업
                tools_dir = self.db_base_dir / "tools"
                if tools_dir.exists():
                    for tool_file in tools_dir.rglob("*"):
                        if tool_file.is_file():
                            rel_path = tool_file.relative_to(self.db_base_dir)
                            backup.write(tool_file, str(rel_path))
            
            # 새 패키지 압축 해제
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.db_base_dir)
            
            # 임시 파일 삭제
            zip_path.unlink()
            
            return True
        except Exception as e:
            print(f"설치 실패: {e}")
            return False
    
    def refresh_after_update(self):
        """업데이트 후 UI 새로고침"""
        # 목록 다시 채우기
        self.populate_list()
        
        # 정보 레이블 업데이트
        version = self.ransomware_data.get("version", "N/A")
        last_updated = self.ransomware_data.get("last_updated", "N/A")
        total_count = len(self.ransomware_data.get("ransomware_families", []))
        
        info_text = f"{self.t('db_version')}: {version} | {self.t('last_updated')}: {last_updated} | {self.t('total_count')} {total_count}{self.t('ransomware_count')} | {self.t('developer')}: Dangel"
        self.info_label.config(text=info_text)
    
    def compare_versions(self, v1, v2):
        """버전 비교 (v1 > v2 이면 1, v1 == v2 이면 0, v1 < v2 이면 -1)"""
        try:
            v1_parts = [int(x) for x in v1.split('.')]
            v2_parts = [int(x) for x in v2.split('.')]
            
            for i in range(max(len(v1_parts), len(v2_parts))):
                v1_part = v1_parts[i] if i < len(v1_parts) else 0
                v2_part = v2_parts[i] if i < len(v2_parts) else 0
                
                if v1_part > v2_part:
                    return 1
                elif v1_part < v2_part:
                    return -1
            
            return 0
        except:
            return 0

def main():
    root = tk.Tk()
    app = RansomGuardApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
