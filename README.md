# Reseptit

## Sovelluksen toiminnot
* Sovelluksessa käyttäjät pystyvät jakamaan ruokareseptejään. Reseptissä lukee tarvittavat ainekset ja valmistusohje.
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään reseptejä ja muokkaamaan ja poistamaan niitä.
* Käyttäjä näkee sovellukseen lisätyt reseptit.
* Käyttäjä pystyy etsimään reseptejä hakusanalla.
* Käyttäjäsivu näyttää, montako reseptiä käyttäjä on lisännyt ja listan käyttäjän lisäämistä resepteistä.
* Käyttäjä pystyy luokittelemaan ruokalajin ja ruokavalion mukaan (esim. pääruoka ja maidoton).
* Käyttäjä pystyy antamaan reseptille kommentin ja arvosanan. Reseptistä näytetään kommentit ja keskimääräinen arvosana.

## Asennusohjeet
Linux:
Asenna sovelluksen hakemistoon virtuaaliympäristö, jotta et tarvitse pääkäyttäjän oikeuksia, seuraavalla komennolla:

```
$ python3 -m venv venv
```

Aktivoi virtuaaliympäristö komennolla:

```
$ source venv/bin/activate
```

Asenna `Flask`-kirjasto:

```
$ pip install flask
```

Luo tietokanta:

```
$ sqlite3 database.db < schema.sql
```

Käynnistä sovellus:

```
$ flask run
```

Avaa seuraava osoite selaimessa:

```
http://127.0.0.1:5000/
```

Kun haluat poistua virtuaaliympäristöstä kirjoita:

```
$ deactivate
```
