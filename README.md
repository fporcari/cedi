# CEDI - Gestionale Casa Editrice

Gestionale per piccole case editrici indipendenti, costruito con [GenroPy](https://genropy.org).

Nasce da un'esigenza concreta: trasformare decine di report Excel sparsi tra distributori, piattaforme digitali e fogli personali in un sistema unico, leggibile e a prova di errore.

## Il problema

Una piccola casa editrice riceve ogni mese file di vendita da Messaggerie, report da Bookwire, royalties da Amazon KDP, fogli fiere, movimenti ecommerce. Ogni canale ha il suo formato, le sue regole, i suoi tempi. I rischi principali sono quattro:

1. **Pagare due volte le royalties** a un autore per lo stesso periodo
2. **Perdere copie fuori magazzino** senza sapere dove sono finite
3. **Non sapere quante copie ci sono davvero** nel magazzino principale
4. **Non ricordare quali autori sono già stati pagati** e per quale periodo

## Architettura

### Flusso generale dei dati

```mermaid
flowchart LR
    subgraph INPUT["File in ingresso"]
        MSG["Messaggerie\n(XLS mensili)"]
        BW["Bookwire\n(CSV mensili)"]
        KDP["Amazon KDP\n(XLSX mensili)"]
        ECOM["Ecommerce\n(XLSX)"]
        FIERE["Fiere\n(XLSX)"]
        INV["Inventario\n(XLSX)"]
    end

    subgraph CEDI["CEDI - Gestionale"]
        IMPORT["Import &\nAnti-doppione"]
        CAT["Catalogo\nTitoli + Autori"]
        VEND["Registro\nVendite"]
        MAG["Magazzino\nFogazzaro"]
        ROY["Calcolo\nRoyalties"]
        PAG["Pagamenti\nAutori"]
    end

    subgraph OUTPUT["Output"]
        REND["Rendiconti\nAutori"]
        REPORT["Report\nCatalogo"]
        STOCK["Situazione\nMagazzino"]
    end

    MSG --> IMPORT
    BW --> IMPORT
    KDP --> IMPORT
    ECOM --> IMPORT
    FIERE --> IMPORT
    INV --> IMPORT

    IMPORT --> VEND
    IMPORT --> MAG
    CAT --> ROY
    VEND --> ROY
    ROY --> PAG

    PAG --> REND
    CAT --> REPORT
    MAG --> STOCK
```

### Modello dati

```mermaid
erDiagram
    TITOLO {
        string isbn UK
        string titolo
        string collana_codice FK
        string formato_codice FK
        string genere_codice FK
        date data_pubblicazione
        boolean attivo
    }

    AUTORE {
        string cognome
        string nome
        string codice_fiscale
        string partita_iva
        string regime_fiscale FK
        decimal ritenuta_acconto
        string iban
    }

    TITOLO_AUTORE {
        string titolo_id FK
        string autore_id FK
        decimal quota_percentuale
        string ruolo
    }

    TITOLO_CODIFICA {
        string titolo_id FK
        string codice
        string tipo_codice "ISBN / ASIN / ISBN_STORYTEL"
        string tipo_prodotto "EBOOK / CARTACEO / AUDIOLIBRO"
        string tipo_stampa "POD / SELF / TIRATURA"
        decimal prezzo
        decimal royalty_percentuale
    }

    MOVIMENTO {
        string canale_codice FK
        date periodo_da
        date periodo_a
        string tipo_movimento "VENDITA / RESO / ROYALTY"
        string file_sorgente
        datetime data_importazione
        string valuta
    }

    MOVIMENTO_RIGA {
        string movimento_id FK
        string titolo_id FK
        string isbn
        int quantita
        decimal prezzo_unitario
        decimal importo_lordo
        decimal importo_netto
        decimal royalty
        string valuta
        string paese
        string store
    }

    INVENTARIO {
        string titolo_id FK
        string isbn
        date data
        int quantita
        decimal ricavo
        string tipo "CONCORSO / FIERA / ECOMMERCE / OMAGGIO"
    }

    TITOLO ||--o{ TITOLO_AUTORE : "ha autori"
    AUTORE ||--o{ TITOLO_AUTORE : "scrive"
    TITOLO ||--o{ TITOLO_CODIFICA : "ha codifiche"
    TITOLO ||--o{ MOVIMENTO_RIGA : "venduto in"
    TITOLO ||--o{ INVENTARIO : "movimentato"
    MOVIMENTO ||--o{ MOVIMENTO_RIGA : "contiene"
    CANALE ||--o{ MOVIMENTO : "origine"
```

### Flusso calcolo royalties

```mermaid
flowchart TD
    START["Vendita registrata"] --> CANALE{"Canale?"}

    CANALE -->|Messaggerie| MSG_CALC["copie nette x\n(prezzo copertina / 1,04)\nx % royalty"]
    CANALE -->|Bookwire| BW_CALC["Payment Amount Publisher\nx % royalty\nx quota beneficiario"]
    CANALE -->|KDP| KDP_CALC["colonna Royalty KDP\nx % royalty contrattuale\n(separare valute)"]
    CANALE -->|Ecommerce| ECOM_CALC["ricavo / 1,04\nx % royalty"]
    CANALE -->|Fiere| FIERA_CALC["copie vendute (no omaggi)\nx (prezzo / 1,04)\nx % royalty"]
    CANALE -->|Inventario| INV_CALC{"Tipo movimento?"}

    INV_CALC -->|"INVIO DIRETTO\nECOMMERCE"| INV_ROY["quantità x\n(prezzo / 1,04)\nx % royalty"]
    INV_CALC -->|"DIRECTBOOK\nMESSAGGERIE"| INV_ZERO["Uscita magazzino\n(zero royalty)"]
    INV_CALC -->|"OMAGGIO\nDEPOSITO LEGALE\nCOPIE AUTORE"| INV_NULLA["Zero royalty"]

    MSG_CALC --> COAUTORI
    BW_CALC --> COAUTORI
    KDP_CALC --> COAUTORI
    ECOM_CALC --> COAUTORI
    FIERA_CALC --> COAUTORI
    INV_ROY --> COAUTORI

    COAUTORI{"Coautori?"} -->|"Autore unico"| TOTALE["Royalty = base x 100%"]
    COAUTORI -->|"Più autori"| QUOTA["Royalty autore =\nbase x quota %"]

    TOTALE --> REGISTRO["Registro pagamenti"]
    QUOTA --> REGISTRO
```

### Flusso magazzino

```mermaid
flowchart LR
    subgraph ENTRATE["Entrate"]
        STAMPA["Stampa / Ristampa"]
        RESI_MAG["Resi da librerie"]
        RIENTRO_FIERA["Rientri fiera"]
    end

    subgraph MAGAZZINO["Magazzino Fogazzaro"]
        STOCK[("Giacenza\nreale")]
    end

    subgraph USCITE["Uscite"]
        MESS_OUT["Invio Messaggerie"]
        FIERA_OUT["Carico fiera"]
        DEPOSITO["Conto deposito"]
        DIRETTO["Invio diretto"]
        OMAGGIO["Omaggi / Copie autore"]
    end

    STAMPA -->|"+N copie"| STOCK
    RESI_MAG -->|"+N copie"| STOCK
    RIENTRO_FIERA -->|"+N copie"| STOCK

    STOCK -->|"-N copie"| MESS_OUT
    STOCK -->|"-N copie"| FIERA_OUT
    STOCK -->|"-N copie"| DEPOSITO
    STOCK -->|"-N copie"| DIRETTO
    STOCK -->|"-N copie"| OMAGGIO
```

## Cosa fa il gestionale

### Anagrafiche (package `cedi`)

- **Catalogo titoli**: ISBN, formato, collana, genere, data pubblicazione
- **Codifiche titolo**: ogni edizione (ebook, cartaceo, audiolibro) ha il suo codice (ISBN, ASIN, ISBN Storytel) con prezzo, tipo prodotto, tipo stampa e percentuale royalty specifici
- **Autori**: dati fiscali, IBAN, contratto, ritenuta d'acconto, regime fiscale
- **Relazione titolo-autore**: coautori con quote percentuali per la ripartizione delle royalties
- **Tabelle di codifica**: collane, formati, generi, regimi fiscali

### Vendite e movimenti (package `vendite`)

- **Movimenti**: testata per ogni file importato (canale, periodo, tipo, totali)
- **Righe movimento**: dettaglio per ISBN con quantità, importi lordi/netti, royalty, valuta, paese, store
- **Inventario**: movimenti fisici del magazzino (concorsi, fiere, ecommerce, omaggi, resi)
- **Canali**: Messaggerie, Bookwire, Amazon KDP, BookRepublic, Ecommerce, Fiere, Inventario

### Magazzino Fogazzaro

Il magazzino fisico principale deve mostrare la giacenza reale. Solo i movimenti fisici (ingresso copie, uscite, resi) modificano lo stock. Le vendite digitali e i report royalty non lo toccano.

### Fiere

Gestite separatamente dal conto deposito. Il ciclo completo è: carico fiera → venduto fiera → omaggi → rientri. Le copie non devono essere scaricate due volte dal magazzino.

### Conto deposito

Traccia i libri inviati ai clienti: inviati, venduti, resi, ancora fuori. La royalty matura solo sul venduto dichiarato, non sull'invio.

### Calcolo royalties

Il sistema deve calcolare il dovuto agli autori con regole diverse per canale:

**Messaggerie** (vendite fisiche tramite distributore):
```
Royalty = copie nette × (prezzo copertina / 1,04) × % royalty contrattuale
```
Le vendite si sommano, le rese si sottraggono. La base è il prezzo di copertina al netto dell'IVA al 4%, non il netto Messaggerie.

**Bookwire / BookRepublic** (vendite digitali tramite aggregatore):
```
Royalty = Payment Amount Publisher × % royalty × quota beneficiario
```
La base è la quota netta percepita dall'editore. I resi (Sale Type = retour) vanno inclusi perché sono già negativi. I freegoods generano zero royalty.

**Amazon KDP** (vendite dirette Amazon):
```
Royalty = colonna Royalty del report KDP × % royalty contrattuale
```
Non bisogna riapplicare il 70%/60% di Amazon (è già nella colonna Royalty). Non usare il prezzo medio di listino come base. Separare le valute (EUR, GBP, USD) e convertire con il cambio effettivo del Payment Report KDP. Includere le righe KENP/Kindle Unlimited.

**Ecommerce** (vendite dirette dal sito):
```
Royalty = ricavo / 1,04 × % royalty
```
La base è il ricavo al netto dell'IVA. Non sottrarre commissioni o costi di spedizione salvo diverso accordo contrattuale.

**Fiere**:
```
Royalty = copie vendute (omaggio=0) × (prezzo copertina / 1,04) × % royalty
```
Gli omaggi non generano royalty, vanno solo conteggiati a parte.

**Inventario** (invii diretti):
```
Royalty solo su movimenti INVIO DIRETTO ed ECOMMERCE
```
Esclusi: Directbook, Messaggerie (uscite magazzino terzi), omaggi, deposito legale, copie autore (zero royalty).

**Audiolibri** (Storytel/Storyside):
```
Base = MIN(quota editore, saldo EUR) per prudenza
Royalty = base × % royalty contrattuale
```
Solo i saldi positivi generano pagamento. I saldi negativi restano a nuovo.

**Coautori**: se un titolo ha più beneficiari, la royalty si ripartisce per quota:
```
Royalty autore = base royalty titolo × % royalty × quota beneficiario
```

### Pagamenti autori

Registro separato per sapere chi è stato pagato, quando, per quale periodo e quanto resta da saldare. Gestione ritenuta d'acconto.

### Import e anti-doppione

Ogni file importato lascia traccia con: nome file, data importazione, canale, periodo, numero righe. Il sistema controlla duplicati (stesso file già importato), conflitti (stesso periodo/canale già presente), righe anomale.

## Struttura del progetto

```
cedi/
├── packages/
│   ├── cedi/                    # Catalogo e anagrafiche
│   │   ├── model/               # Tabelle: titolo, autore, collana, codifica...
│   │   ├── resources/tables/    # Interfacce (view, form, batch)
│   │   └── webpages/
│   └── vendite/                 # Vendite e movimenti
│       ├── model/               # Tabelle: movimento, riga, inventario, canale
│       ├── resources/tables/
│       └── webpages/
├── scripts/
│   ├── import_anagrafica.py     # Importa catalogo titoli da Excel
│   └── import_vendite.py        # Importa vendite da tutti i canali
└── instances/
    └── cedipg/                  # Istanza PostgreSQL
```

## Requisiti

- Python 3.8+
- PostgreSQL
- [GenroPy](https://github.com/genropy/genropy) installato nel virtualenv
- `openpyxl`, `xlrd` per gli script di importazione

## Installazione

```bash
# Clona il progetto nella cartella genropy_projects
cd ~/sviluppo/genropy_projects
git clone https://github.com/fporcari/cedi.git

# Crea il database
gnr db setup cedipg

# Avvia il server
gnr web serve cedipg
```

## Importazione dati

Gli script di importazione leggono i file dalla cartella `DELRAI/` (non inclusa nel repo).

```bash
# Importa anagrafica titoli
python scripts/import_anagrafica.py --instance cedipg --clear

# Importa tutte le vendite
python scripts/import_vendite.py --instance cedipg --clear

# Importa solo un canale/anno
python scripts/import_vendite.py --instance cedipg --canale messaggerie --anno 2025
```

Canali supportati: `messaggerie`, `bookwire`, `kdp`, `inventario`, `fiere`, `ecommerce`, `tutti`.

## Stato del progetto

Il progetto è in fase iniziale. Sono implementati:

- [x] Anagrafica titoli con codifiche multi-formato (ISBN/ASIN/ISBN Storytel)
- [x] Anagrafica autori con dati fiscali e quote coautore
- [x] Import catalogo da Excel
- [x] Import vendite Messaggerie (vendite e resi, formato XLS)
- [x] Import vendite Bookwire (formato CSV)
- [x] Import royalties Amazon KDP (formato XLSX)
- [x] Import inventario, fiere, ecommerce (formato XLSX)
- [x] Collegamento automatico ISBN/ASIN ai titoli del catalogo

Da implementare:

- [ ] Magazzino Fogazzaro con giacenza reale
- [ ] Gestione fiere (carico/scarico/rientri)
- [ ] Conto deposito
- [ ] Calcolo royalties per canale con le regole sopra descritte
- [ ] Gestione coautori e quote nella ripartizione royalties
- [ ] Registro pagamenti autori con saldo residuo
- [ ] Import log con controllo anti-doppione
- [ ] Import BookRepublic (storico)
- [ ] Import audiolibri (Storytel/Storyside)
- [ ] Rendiconti autori stampabili
- [ ] Report catalogo, conto deposito, fiere

## Licenza

Questo progetto è distribuito con licenza open source. Contributi benvenuti.
