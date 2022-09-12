#!/bin/bash

source /home/cdc/Desktop/CDC_Web_Portal_Backend/cdc-placement-website-backend/venv/bin/activate

cd /home/cdc/Desktop/CDC_Web_Portal_Backend/cdc-placement-website-backend/CDC_Backend

python manage.py process_tasks
