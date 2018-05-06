@echo off

if exist "venv" (
    echo ------- Activate virtual environnement --------
    
    call venv\Scripts\activate

) else (
    echo ------- Create venv ---------

    python -m venv venv
    call venv\scripts\activate

    echo ------- Install requirements -------

    pip install -r requirements.txt

	echo ------- Installation finished --------
)


echo ------- Lauch NoteCounter -------
python homography/init.py

pause
