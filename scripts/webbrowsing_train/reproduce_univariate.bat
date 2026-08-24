@echo off
setlocal

REM Move from scripts\webbrowsing_train\ to the repository root
cd /d "%~dp0\..\.."

set "NOTEBOOK_DIR=%CD%\notebooks\webbrowsing_train"
set "OUTPUT_DIR=%CD%\executed_notebooks\webbrowsing_train"

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

echo Running univariate notebooks...
echo ==============================================

echo Starting Naive
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\webbrowsing_train\Naive.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished Naive
echo ==============================================

echo Starting XGB
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\webbrowsing_train\XGB_Univariate.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished XGB
echo ==============================================

echo Starting iTransformer
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\webbrowsing_train\iTransformer_Univariate.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished iTransformer
echo ==============================================

echo Starting PatchTST
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\webbrowsing_train\PatchTST_Univariate.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished PatchTST
echo ==============================================

echo Starting TTM
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\webbrowsing_train\TTM_Univariate.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished TTM
echo ==============================================

echo Starting RF
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\webbrowsing_train\RF_Univariate.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished RF
echo ==============================================

echo Starting Chronos Zeroshot
echo ==============================================
python -m jupyter nbconvert --to notebook --execute "notebooks\webbrowsing_train\Chronos_Zeroshot_Univariate.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished Chronos Zeroshot
echo ==============================================

echo Starting Chronos Fine-tuning
echo ==============================================
python -m jupyter nbconvert --to notebook --execute "notebooks\webbrowsing_train\Chronos_finetuning_Univariate.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished Chronos Fine-tuning
echo ==============================================

echo Starting Lag-llama Zeroshot
echo ==============================================
python -m jupyter nbconvert --to notebook --execute "notebooks\webbrowsing_train\llama.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished Lag-llama Zeroshot
echo ==============================================

echo Starting Lag-llama Fine-tuning
echo ==============================================
python -m jupyter nbconvert --to notebook --execute "notebooks\webbrowsing_train\llama_Finetuning.ipynb" --output-dir "%OUTPUT_DIR%" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished Lag-llama Fine-tuning
echo ==============================================

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo One of the notebook executions failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo All univariate notebooks executed successfully.
pause
