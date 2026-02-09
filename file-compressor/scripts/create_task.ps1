# 文件: create_task.ps1
# 用途: 创建 Windows 任务计划，定时运行 file-compressor

param(
    [string]$Action = "list",
    [string]$Target = "C:\Users\52648\Downloads",
    [string]$Times = "09:00,12:00,18:00,22:00"
)

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = "$ScriptPath\compress.py"
$TaskName = "FileCompressor-Agent"

function Create-Task {
    Write-Host "创建定时任务: $TaskName" -ForegroundColor Green
    Write-Host "目标目录: $Target" -ForegroundColor Cyan
    Write-Host "执行时间: $Times" -ForegroundColor Cyan

    # 移除已存在的任务
    schtasks /delete /tn $TaskName /f 2>$null | Out-Null

    # 为每个时间点创建任务
    $timeList = $Times.Split(',')
    foreach ($time in $timeList) {
        $time = $time.Trim()
        $command = "python `"$PythonScript`" --target `"$Target`" --mode auto"

        schtasks /create `
            /tn "$TaskName-$time" `
            /tr $command `
            /sc daily `
            /st $time `
            /rl HIGHEST `
            /f

        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [OK] $time" -ForegroundColor Green
        } else {
            Write-Host "  [失败] $time" -ForegroundColor Red
        }
    }
}

function Remove-Tasks {
    Write-Host "删除定时任务..." -ForegroundColor Yellow
    schtasks /query /tn "*$TaskName*" /fo list 2>$null | ForEach-Object {
        if ($_ -match "任务名称:\s*(.+)") {
            $name = $matches[1].Trim()
            Write-Host "  删除: $name" -ForegroundColor Yellow
            schtasks /delete /tn $name /f 2>$null | Out-Null
        }
    }
}

function List-Tasks {
    Write-Host "定时任务列表:" -ForegroundColor Green
    Write-Host "="*50
    schtasks /query /tn "*$TaskName*" /fo list 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "没有找到相关任务" -ForegroundColor Yellow
    }
}

function Show-Help {
    Write-Host @"
文件压缩定时任务管理

用法:
    .\create_task.ps1 -Action <命令> [选项]

命令:
    add     - 创建定时任务
    remove  - 删除所有相关任务
    list    - 列出定时任务
    help    - 显示此帮助

选项:
    -Target <路径>  - 要压缩的目标目录 (默认: C:\Users\52648\Downloads)
    -Times <时间>   - 执行时间，逗号分隔 (默认: 09:00,12:00,18:00,22:00)

示例:
    .\create_task.ps1 -Action add -Target "C:\Downloads"
    .\create_task.ps1 -Action add -Target "C:\Downloads" -Times "09:00,14:00,20:00"
    .\create_task.ps1 -Action remove
    .\create_task.ps1 -Action list

"@ -ForegroundColor Cyan
}

# 主逻辑
switch ($Action.ToLower()) {
    "add"    { Create-Task }
    "remove" { Remove-Tasks }
    "list"   { List-Tasks }
    "help"   { Show-Help }
    default  { Show-Help }
}
