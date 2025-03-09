# MRI AI Results API

This is the backend Django API for the CM3070 final report. Run together with Angular UI [https://github.com/DanConstantin/report-fe](frontend).

Run in your python environment by installing the pip modules with `pip install -r requirements.txt` and then `python manage.py runserver`.

Also copy from the Google Drive with the models (you can find the link in the report) the Swin Transformer best model, move it to `preciseMed` folder and rename it to `model_Swin_Transformer_best.pth`. The file was too big to be pushed to git.

The credentials are `patient1` up to `patient5` and `doctor1` to `doctor5`, all with password `University#559`.