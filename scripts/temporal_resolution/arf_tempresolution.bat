@echo off
setlocal

REM Run from the repository root or double-click this file.
cd /d "%~dp0\.."

if not exist executed_notebooks\temporal_resolution mkdir executed_notebooks\temporal_resolution

echo Running multivariate notebooks...
echo ==============================================

echo Starting ARF
echo ==============================================
jupyter nbconvert --to notebook --execute "..\notebooks\Temporal_Resolution\AdaptiveRF_Multivariate.ipynb" --output-dir "..\executed_notebooks\temporal_resolution" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished ARF
echo ==============================================


if %ERRORLEVEL% NEQ 0 (
    echo.
    echo One of the notebook executions failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ARF multivariate notebook executed successfully.
echo Results saved in results\executed_notebooks\temporal_resolution
pause
