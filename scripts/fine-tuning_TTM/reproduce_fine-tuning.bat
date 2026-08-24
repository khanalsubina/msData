@echo off
setlocal

REM Move from scripts\fine-tuning_TTM\ to the repository root
cd /d "%~dp0\..\.."

set "NOTEBOOK_DIR=%CD%\notebooks\fine-tuning_TTM"
set "OUTPUT_DIR=%CD%\executed_notebooks\fine-tuning_TTM"

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

echo Running fine-tuning TTM notebooks...
echo ==============================================

echo Starting TTM Adapter-based approach
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\Fine-Tuning_strategies_for_TTM\TTM_Adapter-based.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished TTM Adapter-based approach
echo ==============================================

echo Starting TTM Head-only approach
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\Fine-Tuning_strategies_for_TTM\TTM_HeadOnly.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished TTM Head-only approach
echo ==============================================



if %ERRORLEVEL% NEQ 0 (
    echo.
    echo One of the notebook executions failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo All TTM fine-tuning notebooks executed successfully.
pause
