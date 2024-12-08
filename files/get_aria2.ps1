try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
} catch {
    Write-Error "Outdated operating systems are not supported."
    Exit 1
}

$file = 'aria2c.exe'
$url = 'https://uupdump.net/misc/aria2c.exe';

function Test-Existence {
    param (
        [String]$File
    )

    return Test-Path -PathType Leaf -Path "files\$File"
}

function Retrieve-File {
    param (
        [String]$File,
        [String]$Url
    )

    Write-Host -BackgroundColor Black -ForegroundColor Yellow "Downloading ${File}..."
    Invoke-WebRequest -UseBasicParsing -Uri $Url -OutFile "files\$File" -ErrorAction Stop
}

if(-not (Test-Path -PathType Container -Path "files")) {
    $null = New-Item -Path "files" -ItemType Directory
}

$ProgressPreference = 'SilentlyContinue'

try {
    Retrieve-File -File $file -Url $url
} catch {
    Write-Host "Failed to download $file"
    Write-Host $_
    Exit 1
}

Write-Host -BackgroundColor Black -ForegroundColor Green "Ready."
