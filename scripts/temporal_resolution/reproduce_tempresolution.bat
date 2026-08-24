@echo off
setlocal

REM Move from scripts\temporal_resolution\ to the repository root
cd /d "%~dp0\..\.."

set "NOTEBOOK_DIR=%CD%\notebooks\temporal_resolution"
set "OUTPUT_DIR=%CD%\executed_notebooks\temporal_resolution"

echo Repository root:
echo %CD%
echo.
echo Notebook directory:
echo %NOTEBOOK_DIR%
echo.
echo Executed notebooks will be saved in:
echo %OUTPUT_DIR%
echo.
 
if not exist "%NOTEBOOK_DIR%" (
echo ERROR: Notebook directory not found:
echo %NOTEBOOK_DIR%
pause
exit /b 1
)
 
if not exist "%OUTPUT_DIR%" (
mkdir "%OUTPUT_DIR%"
)

echo Running multivariate notebooks...
echo ==============================================

echo Starting TTM Multivariate
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\Temporal_Resolution\TTM_Multivariate.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished TTM Multivariate
echo ==============================================

echo Starting Chronos-Zeroshot
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\Temporal_Resolution\Chronos_Zeroshot_Multivariate.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished Chronos-Zeroshot
echo ==============================================

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo One of the notebook executions failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo All multivariate notebooks executed successfully.
pause
