# CyberDefender

CyberDefender è una web app pensata per aiutare privati e aziende a riconoscere e prevenire le minacce informatiche più comuni. Attraverso form per il rilevamento degli attacchi sulla base delle osservazioni riportate dagli utenti, analisi di messaggi sospetti e verifica di numeri di telefono, offre strumenti semplici e concreti per migliorare la sicurezza digitale. L’applicazione è progettata per garantire la massima sicurezza nell’interazione con i dati degli utenti, grazie all’uso di tecnologie moderne che prevengono attacchi informatici e proteggono la privacy. CyberDefender è accessibile, gratuita e supporta l’utente con consigli personalizzati, rendendo la sicurezza online più vicina e comprensibile per tutti.

---

## Indice

- [Modello Entità-Relazione](#modello-entità-relazione)
- [Funzionalità Principali](#funzionalità-principali)
- [Tecnologie utilizzate](#tecnologie-utilizzate)
- [Installazione](#installazione)
- [Esempio di utilizzo](#esempio-di-utilizzo)
- [Licenza](#licenza)

---


## Modello Entità-Relazione

Il modello Entità-Relazione rappresenta le entità principali del sistema e le loro relazioni, permettendo la gestione strutturata e coerente di utenti, contenuti dell’enciclopedia degli attacchi, messaggi e numeri da analizzare, nonché delle domande presenti nel modulo di rilevamento, i cui risultati vengono salvati in report PDF personalizzati.

--- 

## Funzionalità Principali

La piattaforma propone le seguenti funzionalità principali:

1. **Enciclopedia degli attacchi:**  
   Una raccolta organizzata di schede informative che descrivono i principali tipi di attacchi informatici (come phishing, SQL injection, cross-site scripting, ecc.), presentate con un linguaggio chiaro e accessibile a utenti non esperti. Ogni scheda include:  
   a. Definizione dell’attacco;  
   b. Modalità di esecuzione;  
   c. Possibili conseguenze;  
   d. Consigli pratici per la prevenzione.

2. **Compilazione modulo rilevamento attacco:**  
   Sulla base delle informazioni presenti nell’Enciclopedia degli attacchi, l’utente può compilare un modulo guidato per rilevare un possibile attacco informatico in corso. Il modulo propone una serie di domande semplici e mirate, costruite in relazione ai sintomi comuni degli attacchi descritti.

3. **Report PDF con consigli su misura:**  
   Al termine dell’analisi delle risposte, CyberDefender genera un report personalizzato in formato PDF. Questo documento riassume i risultati, individua eventuali vulnerabilità o rischi, e offre una serie di raccomandazioni pratiche per migliorare la propria sicurezza digitale.

4. **Analizzatore di messaggi sospetti:**  
   Uno strumento interattivo che permette agli utenti di inserire messaggi o query sospette (ad esempio email, testi o codici). Il sistema analizza il contenuto alla ricerca di parole chiave o pattern tipici di attacchi informatici, valutando la gravità del rischio e fornendo un feedback immediato. Questo aiuta l’utente a riconoscere tempestivamente potenziali minacce.

5. **Verifica numeri di telefono:**  
   È presente anche una funzionalità per inserire numeri di telefono sospetti e verificarne l’autenticità, distinguendo tra numeri affidabili e potenziali chiamate pubblicitarie o fraudolente.

#### Funzionalità future specifiche per utenti aziendali:

6. **Accesso a contenuti tecnici più approfonditi:**  
   Per le aziende e i referenti tecnici, CyberDefender mette a disposizione sezioni dedicate con materiale più specialistico, tra cui:  
   a. Linee guida avanzate sulle configurazioni di sicurezza;  
   b. Check-list basate su standard riconosciuti come OWASP;  
   c. Risorse per la formazione continua del personale in ambito cybersecurity.

Queste funzionalità sono pensate per rispondere alle diverse esigenze degli utenti, garantendo un’esperienza personalizzata e una copertura completa sia degli aspetti teorici che pratici della sicurezza informatica.

---

## Tecnologie utilizzate

CyberDefender è sviluppato come applicazione web con backend in Python tramite il framework Django e frontend realizzato con Bootstrap (HTML, CSS, JavaScript), adottando tecnologie moderne e sicure.

Le principali caratteristiche tecniche includono:

- Gestione differenziata degli utenti (privati e aziende) tramite un sistema di controllo degli accessi basato sui ruoli (RBAC), che assegna permessi specifici per ogni sezione.
- Adozione di pratiche di sicurezza contro vulnerabilità come SQL Injection, Cross-Site Request Forgery (CSRF) e gestione sicura dei cookie di sessione, secondo le linee guida OWASP.
- Funzionalità di form per il riconoscimento di attacchi, analisi semantica dei messaggi sospetti, verifica numeri di telefono e generazione report personalizzati.
- Sistema avanzato di logging e auditing per tracciare in modo sicuro tutte le operazioni critiche (login, richieste, consultazione report).
- Test approfonditi (unit test, integration test, system test, acceptance test e penetration test) per garantire qualità, sicurezza e affidabilità.
- Strategie di sicurezza basate sul modello STRIDE, in linea con standard ISO/IEC 27001, NIST e OWASP ASVS.

---

## Installazione

Per eseguire l'applicazione, è necessario:

1. Disporre di Python installato nel proprio ambiente.  
2. Avere accesso a un server SQLite3 per una gestione semplificata.

**Clonare il progetto:**

```bash
git clone https://github.com/Axel0252/SW_Sicuro_Website
cd Progetto_BdD
Creare e attivare un ambiente virtuale:

```bash
python -m venv venv
# Linux/macOS
```bash
source venv/bin/activate
# Windows Powershell
```bash
.\.venv\Scripts\Activate.ps1
# Windows cmd
```bash
.\.venv\Scripts\activate.bat
Installare le dipendenze:
```bash
pip install -r requirements.txt
Se non si dispone di un file requirements.txt, si può installare manualmente:
```bash


pip install django mysqlclient

##Configurazione del Database:
CyberDefender utilizza SQLite3 come database predefinito, che è integrato di default in Django e non richiede configurazioni esterne complesse.
Per utilizzare SQLite3, assicurati che nel file settings.py la configurazione del database sia simile a questa:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
Non è necessario installare software aggiuntivo per il database, poiché SQLite è leggero e funziona direttamente con il file di progetto.

Migrazioni e avvio server:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
L'applicazione sarà accessibile all'indirizzo: http://localhost:8000.

## Esempio di utilizzo
Quando un utente vuole consultare informazioni sugli attacchi informatici, inizia inviando una richiesta specifica al sistema, selezionando la scheda desiderata. Il sistema recupera le informazioni dall’archivio enciclopedia, che includono definizione, modalità di esecuzione, conseguenze e consigli pratici.
L’evento di consultazione viene registrato in modo sicuro nei log, con dati come l’identificativo utente (se disponibile), orario e contenuto visualizzato, per garantire tracciabilità e audit.

Infine, i dati vengono inviati all’interfaccia utente per la visualizzazione completa della scheda informativa, completando così la consultazione.

## Licenza
Questo progetto è rilasciato sotto licenza MIT.
Consulta il file LICENSE per maggiori dettagli.

