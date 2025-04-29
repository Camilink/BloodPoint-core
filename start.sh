#!/bin/bash
gunicorn bloodpoint_project.wsgi --workers 4 --timeout 120 -b 0.0.0.0:5000 &
superset run -p 8088
