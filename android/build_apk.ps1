param(
    [switch]$Release,
    [string]$OutputDir = ""
)

$ErrorActionPreference = "Stop"

Write-Host "=== Fibonacci Division Game - Android APK Builder ===" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
$hasJava = $null -ne (Get-Command java -ErrorAction SilentlyContinue)
$hasJavac = $null -ne (Get-Command javac -ErrorAction SilentlyContinue)

if (-not $hasJava) {
    Write-Host "[ERROR] Java (JDK 17+) not found. Install Eclipse Temurin JDK 17 from:" -ForegroundColor Red
    Write-Host "        https://adoptium.net/" -ForegroundColor Yellow
    exit 1
}

$javaVersion = java -version 2>&1 | Select-String -Pattern "version" | ForEach-Object { $_ -replace '.*"([^"]+)".*', '$1' }
Write-Host "[OK] Java version: $javaVersion" -ForegroundColor Green

# Check ANDROID_HOME
$androidHome = $env:ANDROID_HOME
if (-not $androidHome) {
    $androidHome = "$env:LOCALAPPDATA\Android\Sdk"
    if (-not (Test-Path $androidHome)) {
        Write-Host "[ERROR] Android SDK not found. Install it via Android Studio:" -ForegroundColor Red
        Write-Host "        https://developer.android.com/studio" -ForegroundColor Yellow
        Write-Host "        Then set ANDROID_HOME environment variable." -ForegroundColor Yellow
        exit 1
    }
    $env:ANDROID_HOME = $androidHome
}

Write-Host "[OK] Android SDK: $androidHome" -ForegroundColor Green

# Find gradle wrapper or create it
$gradlewPath = Join-Path $PSScriptRoot "gradlew.bat"
$wrapperJar = Join-Path $PSScriptRoot "gradle\wrapper\gradle-wrapper.jar"

if (-not (Test-Path $wrapperJar)) {
    Write-Host "[INFO] Gradle wrapper not found. Attempting to generate it..." -ForegroundColor Yellow

    $hasGradle = $null -ne (Get-Command gradle -ErrorAction SilentlyContinue)
    if ($hasGradle) {
        Write-Host "[INFO] Using system Gradle to generate wrapper..." -ForegroundColor Yellow
        Push-Location $PSScriptRoot
        gradle wrapper --gradle-version 8.7
        Pop-Location
    } else {
        Write-Host "[INFO] Downloading Gradle wrapper jar..." -ForegroundColor Yellow
        $wrapperUrl = "https://raw.githubusercontent.com/gradle/gradle/v8.7.0/gradle/wrapper/gradle-wrapper.jar"
        $jarDir = Join-Path $PSScriptRoot "gradle\wrapper"
        New-Item -ItemType Directory -Path $jarDir -Force | Out-Null
        $jarPath = Join-Path $jarDir "gradle-wrapper.jar"
        try {
            Invoke-WebRequest -Uri $wrapperUrl -OutFile $jarPath -UseBasicParsing
        } catch {
            Write-Host "[ERROR] Failed to download Gradle wrapper. Try installing Gradle manually:" -ForegroundColor Red
            Write-Host "        https://gradle.org/install/" -ForegroundColor Yellow
            exit 1
        }
    }
}

if (-not (Test-Path $gradlewPath) -and (Get-Command gradle -ErrorAction SilentlyContinue)) {
    Write-Host "[INFO] Generating gradlew scripts..." -ForegroundColor Yellow
    Push-Location $PSScriptRoot
    gradle wrapper --gradle-version 8.7
    Pop-Location
}

if (-not (Test-Path $gradlewPath)) {
    Write-Host "[ERROR] gradlew.bat not found. Please run 'gradle wrapper' in the android directory." -ForegroundColor Red
    exit 1
}

# Check if app/src/main/assets/index.html exists
$assetsIndex = Join-Path $PSScriptRoot "app\src\main\assets\index.html"
if (-not (Test-Path $assetsIndex)) {
    Write-Host "[ERROR] Web assets not found. Run 'pygbag --build main.py' in the project root first." -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Web assets found" -ForegroundColor Green

Write-Host ""
Write-Host "=== Building APK ===" -ForegroundColor Cyan

$buildType = if ($Release) { "Release" } else { "Debug" }
Write-Host "Build type: $buildType" -ForegroundColor White

Push-Location $PSScriptRoot
try {
    if ($Release) {
        & .\gradlew.bat assembleRelease
    } else {
        & .\gradlew.bat assembleDebug
    }

    if ($LASTEXITCODE -eq 0) {
        $apkDir = if ($Release) { "app\build\outputs\apk\release" } else { "app\build\outputs\apk\debug" }
        $apkName = if ($Release) { "app-release.apk" } else { "app-debug.apk" }
        $apkPath = Join-Path $PSScriptRoot "$apkDir\$apkName"

        if ($OutputDir) {
            $destDir = New-Item -ItemType Directory -Path $OutputDir -Force
            Copy-Item $apkPath -Destination $destDir
            Write-Host ""
            Write-Host "[DONE] APK copied to: $destDir\$apkName" -ForegroundColor Green
        } else {
            Write-Host ""
            Write-Host "[DONE] APK created at: $apkPath" -ForegroundColor Green
        }
    } else {
        Write-Host "[ERROR] Gradle build failed (exit code: $LASTEXITCODE)" -ForegroundColor Red
        exit 1
    }
} finally {
    Pop-Location
}
