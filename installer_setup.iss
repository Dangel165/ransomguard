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
LicenseFile=LICENSE.txt

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
var
  DownloadPage: TDownloadWizardPage;

{ 다운로드 진행 상황 콜백 }
function OnDownloadProgress(const Url, FileName: String; const Progress, ProgressMax: Int64): Boolean;
begin
  if Progress = ProgressMax then
    Log(Format('다운로드 완료: %s', [FileName]));
  Result := True;
end;

{ 환영 메시지 커스터마이징 }
procedure InitializeWizard;
begin
  WizardForm.WelcomeLabel2.Caption := 
    'RansomGuard는 랜섬웨어 정보 데이터베이스 프로그램입니다.' + #13#10 + #13#10 +
    '랜섬웨어 정보 조회, 복구 도구 실행, 복구 동영상 재생 기능을 제공합니다.' + #13#10 + #13#10 +
    '설치 중 데이터베이스가 자동으로 다운로드됩니다 (약 3KB).' + #13#10 + #13#10 +
    '계속하려면 [다음]을 클릭하세요.';
  
  { 다운로드 페이지 생성 }
  DownloadPage := CreateDownloadPage(SetupMessage(msgWizardPreparing), '데이터베이스 다운로드 중...', @OnDownloadProgress);
end;

{ 다운로드 준비 }
function NextButtonClick(CurPageID: Integer): Boolean;
begin
  if CurPageID = wpReady then begin
    DownloadPage.Clear;
    { GitHub에서 최신 데이터베이스 패키지 다운로드 }
    DownloadPage.Add('https://github.com/Dangel165/ransomguard/releases/download/v1.0.0/ransomguard_v1.0.0.zip', 'ransomguard_data.zip', '');
    DownloadPage.Show;
    try
      try
        DownloadPage.Download;
        Result := True;
      except
        if DownloadPage.AbortedByUser then
          Log('다운로드가 사용자에 의해 중단되었습니다.')
        else
          SuppressibleMsgBox(AddPeriod(GetExceptionMessage), mbCriticalError, MB_OK, IDOK);
        Result := False;
      end;
    finally
      DownloadPage.Hide;
    end;
  end else
    Result := True;
end;

{ 설치 후 처리 }
procedure CurStepChanged(CurStep: TSetupStep);
var
  ZipFile: String;
  AppDir: String;
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    AppDir := ExpandConstant('{app}');
    ZipFile := ExpandConstant('{tmp}\ransomguard_data.zip');
    
    { 필요한 폴더 생성 }
    ForceDirectories(AppDir + '\videos');
    ForceDirectories(AppDir + '\tools');
    ForceDirectories(AppDir + '\backup');
    
    { ZIP 파일이 다운로드되었는지 확인 }
    if FileExists(ZipFile) then
    begin
      try
        { PowerShell을 사용하여 ZIP 압축 해제 }
        Exec('powershell.exe', 
          Format('-NoProfile -Command "Expand-Archive -Path ''%s'' -DestinationPath ''%s'' -Force"', [ZipFile, AppDir]),
          '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
        
        if ResultCode = 0 then
          Log('데이터베이스 압축 해제 완료')
        else
          Log(Format('압축 해제 실패: 오류 코드 %d', [ResultCode]));
      except
        Log('압축 해제 중 오류 발생: ' + GetExceptionMessage);
      end;
    end
    else
    begin
      { 다운로드 실패 시 로그 기록 }
      Log('다운로드된 ZIP 파일을 찾을 수 없습니다. 첫 실행 시 자동 다운로드됩니다.');
    end;
  end;
end;

