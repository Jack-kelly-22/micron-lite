cd %HOMEPATH%
cd Desktop
cd micron-lite
pip install virtualenv
virtualenv env
CALL .\env\Scripts\activate.bat
pip install -r requirements.txt
PAUSE
