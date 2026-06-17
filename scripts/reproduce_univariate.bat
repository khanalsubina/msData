@echo off
setlocal

REM Run from the repository root or double-click this file.
cd /d "%~dp0\.."

if not exist results\executed_notebooks mkdir results\executed_notebooks

echo Running univariate notebooks...
echo ==============================================

echo Starting Naive
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\Naive.ipynb" --output-dir "results\executed_notebooks" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished Naive
echo ==============================================

echo Starting XGB
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\XGBoost_Univariate.ipynb" --output-dir "results\executed_notebooks" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished XGB
echo ==============================================

echo Starting iTransformer
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\iTransformer - Univariate.ipynb" --output-dir "results\executed_notebooks" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished iTransformer
echo ==============================================

echo Starting PatchTST
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\PatchTST - Univariate.ipynb" --output-dir "results\executed_notebooks" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished PatchTST
echo ==============================================

echo Starting TTM
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\TTM-Univariate.ipynb" --output-dir "results\executed_notebooks" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished TTM
echo ==============================================

echo Starting RF
echo ==============================================
jupyter nbconvert --to notebook --execute "notebooks\Random Forest_Univariate.ipynb" --output-dir "results\executed_notebooks" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished RF
echo ==============================================

echo Starting Chronos Zeroshot
echo ==============================================
python -m jupyter nbconvert --to notebook --execute "notebooks\Chronos-Zeroshot - Univariate.ipynb" --output-dir "results\executed_notebooks" --ExecutePreprocessor.timeout=-1
echo ==============================================
echo Finished Chronos Zeroshot
echo ==============================================

echo Starting Chronos Fine-tuning
echo ==============================================
python -m jupyter nbconvert --to notebook --execute "notebooks\Chronos-finetuning - Univariate.ipynb" --output-dir "results\executed_notebooks" --ExecutePreprocessor.timeout=-1
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
echo All univariate notebooks executed successfully.
echo Results saved in results\executed_notebooks
pause
