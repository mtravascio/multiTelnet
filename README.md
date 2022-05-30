# multiTelnet
Script per l'esecuzione in sequenza/parallelo di comandi telnet su apparati hpee aruba
con filtragio dell'output ansi attraverso le regular expression

## Installazione su Linux Ubuntu dell'ambiente virtuale Python:
- sudo apt install python3 python3-venv python3-pip

- python3 -m venv venv

- source ./venv/bin/activate

- python3 -m pip install -r requirements.txt

## Esecuzione comando:
python3 ./multiTelnet.py

## input
File di input da utilizzare sono 3:
- apparati_aruba.txt che contiene gli indirizzi ip degli apparati aruba
- apparati_hpe.txt  che contiene gli indirizzi ip degli apparati hpee
- apparati_ss che contiene altri indirizzi ip di apparati aruba
ogni indirizzo ip valido è inserito in una riga
ogni indirizzo ip da non utilizzarsi temporaneamente è ignorato se inzia con il carattere '#'

## output
I file di output sono generati con l'indirizzo ip del device contatto e vengono loggati i comandi
e l'output outtenuto in base ad una lista di comandi ad inizio file che vengono eseguiti in sequenza.

