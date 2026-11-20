@echo off
rem Lancé par le Planificateur de tâches Windows (voir CLAUDE.md § 9) : %1 = auto-maison ou auto-informatique
cd /d "%~dp0.."
git pull -q --ff-only origin main
python _source\chercher_tests.py --rubrique %1 > "_source\data\agy_%1.log" 2>&1
