; Inno Setup 스크립트 - RansomGuard 설치 프로그램
; Inno Setup 다운로드: https://jrsoftware.org/isdl.php

#define MyAppName "RansomGuard"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Dangel"
#define MyAppExeName "RansomGuard.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\RansomGuard
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=installer_output
OutputBaseFilename=RansomGuard_Setup
SetupIconFile=app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; EXE 파일만 설치 (데이터베이스, 동영상, 복구툴은 자동 업데이트로 다운로드)
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
{ 빈 플레이스홀더 파일 생성 }
procedure CreateEmptyFile(FileName: String);
var
  FilePath: String;
begin
  FilePath := ExpandConstant(FileName);
  SaveStringToFile(FilePath, '', False);
end;

{ 설치 후 필요한 폴더 생성 }
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    { videos 폴더 생성 }
    ForceDirectories(ExpandConstant('{app}\videos'));
    CreateEmptyFile('{app}\videos\.placeholder');
    
    { tools 폴더 생성 }
    ForceDirectories(ExpandConstant('{app}\tools'));
    CreateEmptyFile('{app}\tools\.placeholder');
    
    { backup 폴더 생성 }
    ForceDirectories(ExpandConstant('{app}\backup'));
  end;
end;

{ 환영 메시지 커스터마이징 }
procedure InitializeWizard;
begin
  WizardForm.WelcomeLabel2.Caption := 
    'RansomGuard는 랜섬웨어 정보 데이터베이스 프로그램입니다.' + #13#10 + #13#10 +
    '랜섬웨어 정보 조회, 복구 도구 실행, 복구 동영상 재생 기능을 제공합니다.' + #13#10 + #13#10 +
    '첫 실행 시 데이터베이스, 동영상, 복구 툴이 자동으로 다운로드됩니다.' + #13#10 + #13#10 +
    '계속하려면 [다음]을 클릭하세요.';
end;
