#!/bin/bash
#mysql5 -u root < sql/drop-db.sql
#mysql5 -u root < sql/create-db.sql
rm matt_cv.db
../manage.py syncdb --noinput
rm -rf media/*
python scripts/create.py
