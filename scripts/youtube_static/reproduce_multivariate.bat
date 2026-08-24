@echo off
setlocal

REM Move from scripts\youtube_static\ to the repository root
cd /d "%~dp0\..\.."

set "NOTEBOOK_DIR=%CD%\notebooks\youtube_static"
set "OUTPUT_DIR=%CD%\executed_notebooks\youtube_static"

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

echo Starting Naive
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\youtube_static\Naive.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished Naive
echo ==============================================

echo Starting XGB
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\youtube_static\XGB_Multivariate.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished XGB
echo ==============================================

echo Starting iTransformer
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\youtube_static\iTransformer_Multivariate.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished iTransformer
echo ==============================================

echo Starting PatchTST
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\youtube_static\PatchTST_Multivariate.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished PatchTST
echo ==============================================

echo Starting TTM
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\youtube_static\TTM_Multivariate.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished TTM
echo ==============================================

echo Starting RF
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\youtube_static\RF_Multivariate.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished RF
echo ==============================================

echo Starting Chronos Zeroshot
echo ==============================================
python -m jupyter nbconvert --to notebook --execute "notebooks\youtube_static\Chronos_Zeroshot_Multivariate.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished Chronos Zeroshot
echo ==============================================

echo Starting Chronos Fine-tuning
echo ==============================================
python -m jupyter nbconvert --to notebook --execute "notebooks\youtube_static\Chronos_finetuning_Multivariate.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished Chronos Fine-tuning
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
