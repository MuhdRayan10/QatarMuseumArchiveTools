## Rough steps

1. Open powershell as Administrator
2. Locate the directory in which windows.ps1 is located in
2. Execute `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`, then type 'A' when prompted
3. Execute `.\windows.ps1` 
4. Open a new terminal, and try `ffmpeg -version`
