# My Knowledge Plus

O copie independenta a aplicatiei My Knowledge, cu baza de date inclusa.
Modificarile si notitele salvate aici nu schimba proiectul original.

Interfata My Knowledge Plus este redesenata, disponibila in romana si include
teme deschisa/intunecata, cautare rapida si un aspect adaptat pentru telefon,
tableta si desktop. Tema aleasa este pastrata in browser.

## Pornire

1. Deschide `start.bat`. La prima pornire, scriptul creeaza un mediu Python
   local in `.venv` si instaleaza dependintele din `requirements.txt`.
2. Deschide `http://127.0.0.1:5001` in browser. Copia foloseste un port
   separat de proiectul original.
3. Daca aplicatia era deja pornita inainte de actualizare, opreste-o cu
   `Ctrl+C` in fereastra terminalului si deschide din nou `start.bat`.
4. Pentru oprire, revino la fereastra terminalului si apasa `Ctrl+C`.

Este necesar Python 3 si Python Launcher (`py`) pe Windows.

## Date

Notitele sunt salvate in `knowledge.db`, in acest folder. Baza de date copiata
este independenta de cea a proiectului original.
