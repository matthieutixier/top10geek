@echo off
rem Lance par le Planificateur de taches Windows (voir CLAUDE.md, section 9) : %1 = auto-maison ou auto-informatique
set PYTHONUTF8=1
cd /d "%~dp0.."
git pull -q --ff-only origin main
python _source\chercher_tests.py --rubrique %1 > "_source\data\agy_%1.log" 2>&1
