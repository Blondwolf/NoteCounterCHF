@echo off

if exist "venv" (
    echo ------- Activate virtual environnement --------
    
    call venv\Scripts\activate

) else (
    echo ------- Install venv ---------

    pip install virtualenv

    echo ------- Create venv ---------

    virtualenv venv
    call venv\scripts\activate

    echo ------- Install requirements -------

    pip install -r requirements.txt

	echo ------- Installation finished --------
)

echo ------- Lauch NoteCounter -------
python color_detection/note_analyser.py

pause
