@echo off
set /p create="do you want to create supruser ? (Y/N) "


if %create% equ Y  ( python manage.py createsuperuser  )
if %create% equ y  ( python manage.py createsuperuser  )

python manage.py collectstatic --noinput
if exist Storage (echo Storage Directory already exists) else ( echo Creating Storage Directory... & mkdir Storage & echo Storage Directory Created)
timeout 3 > NUL
pause
