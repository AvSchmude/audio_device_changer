@echo off
set arg1=%1
set arg2=%2
start cmd /k echo nircmd setdefaultsounddevice %arg1% %arg2%