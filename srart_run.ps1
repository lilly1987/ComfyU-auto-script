# need "Install-Module VirtualDesktop"
$cnt=Get-DesktopCount
$cnt
if ( $cnt -eq 1 ) 
{
	"new"
	New-Desktop
}
$desk=Get-Desktop 1

# 주석 해제 필요
$desk | Move-Window (Get-ConsoleHandle)

$CommandLine=Get-WmiObject Win32_Process -Filter "name = 'cmd.exe'" | Select-Object CommandLine
# $CommandLine
# $CommandLine -Match "_srart_run.cmd"

if ( -Not ( $CommandLine -Match "_run_nvidia_gpu.bat" ) ){
	$run=Start-Process -PassThru "_run_nvidia_gpu.bat"
	Start-Sleep -Seconds 1
	$desk | Move-Window ($run).MainWindowHandle
}

if ( -Not ( $CommandLine -Match "_run_nvidia_gpu.bat" ) ){
	$run=Start-Process -PassThru "_Run.bat"
	Start-Sleep -Seconds 1
	$desk | Move-Window ($run).MainWindowHandle
}
