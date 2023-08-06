# Linkspirit Package

This package contains some useful functions and classes that can be used in Linkspirit's scripts.

## Database
This class can be used to comunicate with SQL database and running queries.

## Configuration
This class can be used to parse and utilize configuration files (in json format).


## Istruzioni per generare il pacchetto

1. Creare un virtualenv con `virtualenv env --python=python3` **ed attivarlo** con `source env/bin/activate`
1. Installare/aggiornare `pip`, `setuptools` e `wheel`:
> `pip install --upgrade pip setuptools wheel`
2. Spostarsi nella root del progetto ed eseguire:
> `python setup.py sdist bdist_wheel`

3. Se il pacchetto è una nuova versione finale (release), copiare il file `.whl` dalla cartella `dist/` a `releases/` 

## Istruzioni per installare il pacchetto in un virtualenv (CONSIGLIATE)

1. Spostarsi nella root del progetto ed eseguire:
> `pip3 install dist/lisp_utils*.whl`


## Istruzioni per installare il pacchetto system-wide

1. Spostarsi nella root del progetto ed eseguire:
> `sudo -H pip3 install dist/lisp_utils-0.1-py3-none-any.whl --system`
2. Controllare i permessi e gli owner delle cartelle
> `/usr/local/lib/python3.6/dist-packages/lisp_utils`
> e
> `/usr/local/lib/python3.6/dist-packages/lisp_utils-0.1.dist-info/`
> (rimpiazzare `python3.6` con la cartella della propria versione di python)
3. Nel caso i permessi non siano corretti, eseguire:
> `sudo chmod o+rx /usr/local/lib/python3.6/dist-packages/lisp_utils -R`
> e
> `sudo chmod o+rx /usr/local/lib/python3.6/dist-packages/lisp_utils-0.1.dist-info/ -R` 
