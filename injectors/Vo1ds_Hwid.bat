@echo off
cls

rem Set color variables
set "logo_color=95"
set "output_color=95"
set "label_color=97" rem white color

:start
cls

rem ASCII Art Logo
echo.
echo   [%logo_color%m ____        ____       ____        ______      ______      __        [0m 
echo  [%logo_color%m/\  _`\     /\  _`\    /\  _`\     /\__  _\    /\  _  \    /\ \       [0m 
echo  [%logo_color%m\ \,\L\_\   \ \ \L\_\  \ \ \L\ \   \/_/\ \/    \ \ \L\ \   \ \ \      [0m 
echo  [%logo_color%m \/_\__ \    \ \  _\L   \ \ ,  /      \ \ \     \ \  __ \   \ \ \  __ [0m 
echo  [%logo_color%m   /\ \L\ \   \ \ \L\ \  \ \ \\ \      \_\ \__   \ \ \/\ \   \ \ \L\ \[0m 
echo  [%logo_color%m   \ `\____\   \ \____/   \ \_\ \_\    /\_____\   \ \_\ \_\   \ \____/[0m 
echo  [%logo_color%m    \/_____/    \/___/     \/_/\/ /    \/_____/    \/_/\/_/    \/___/  [0m 
echo.                                                                                                                                            

rem Function to get drive details
echo [%label_color%mDrive Details:[0m
echo [%label_color%m=======================[0m
for /f "tokens=1,* delims==" %%A in ('wmic logicaldisk where "drivetype=3" get caption^, volumename /format:list') do (
    if "%%A"=="Caption" (
        set "driveCaption=%%B"
    ) else if "%%A"=="VolumeName" (
        set "driveVolume=%%B"
        echo   [%output_color%m%%B[0m
    )
)

echo.
rem Function to get CPU serial number
echo [%label_color%mCPU:[0m
echo [%label_color%m=======================[0m
for /f "skip=1 tokens=2 delims==" %%A in ('wmic cpu get processorid /format:list') do (
    echo [%output_color%mSerialNumber: %%A[0m
    goto :break1
)
:break1

echo.
rem Function to get BIOS serial number
echo [%label_color%mBIOS:[0m
echo [%label_color%m=======================[0m
for /f "tokens=2 delims==" %%A in ('wmic bios get serialnumber /format:list') do (
    echo [%output_color%mSerialNumber: %%A[0m
    goto :break2
)
:break2

echo.
rem Function to get motherboard serial number
echo [%label_color%mMotherboard:[0m
echo [%label_color%m=======================[0m
for /f "tokens=2 delims==" %%A in ('wmic baseboard get serialnumber /format:list') do (
    echo [%output_color%mSerialNumber: %%A[0m
    goto :break3
)
:break3

echo.
rem Function to get smBIOS UUID
echo [%label_color%msmBIOS UUID:[0m
echo [%label_color%m=======================[0m
for /f "tokens=2 delims==" %%A in ('wmic csproduct get uuid /format:list') do (
    echo [%output_color%mUUID: %%A[0m
    goto :break4
)
:break4

echo.
rem Function to get network adapters physical address and transport name
echo [%label_color%mNetwork Adapters Physical Address and Transport Name:[0m
echo [%label_color%m=======================================================[0m
wmic nic get macaddress, netconnectionid /format:table

echo.
echo.

pause >nul
cls
goto :start
