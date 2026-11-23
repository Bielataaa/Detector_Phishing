# 🛡️ Detector de Phishing

![Detector de Phishing](img/hero.jpg)

Eina educativa que analitza el text d'un correu electrònic i calcula el seu **nivell de risc de phishing** (de 0 a 100), indicant quines senyals sospitoses ha trobat.

🌐 **Prova-la en línia:** [bielataaa.github.io/Detector_Phishing](https://bielataaa.github.io/Detector_Phishing/)

---

## Què és el phishing?

El **phishing** és un tipus d'estafa en què l'atacant es fa passar per una entitat de confiança (un banc, una empresa, el servei tècnic...) per enganyar-te i aconseguir que li donis informació personal, com ara contrasenyes o números de targeta, o que facis un pagament.

---

## Com s'utilitza

### Opció 1: la pàgina web

1. Obre [la web](https://bielataaa.github.io/Detector_Phishing/) (o fes doble clic a `index.html`).
2. Enganxa el text del correu al quadre.
3. Prem **Analitzar**.

### Opció 2: el programa en Python

```bash
python detector.py
```

El programa et demanarà el text del correu i mostrarà el resultat a la terminal.

> ⚠️ A la terminal, `input()` només llegeix una línia. Si el correu té diversos paràgrafs, enganxa'l tot en una sola línia o fes servir la web.

---

## En què es basa la detecció

El detector **no entén el significat del correu**. Funciona com una **llista de comprovació automàtica**: busca paraules i patrons típics del phishing, suma punts per cada tipus de senyal i, segons el total, assigna un nivell de risc.

L'anàlisi es fa en tres passos.

### Pas 1: Normalitzar el text

Abans de buscar res, el text es converteix a **minúscules** i se li **treuen els accents**. Així, «Contrasenya», «CONTRASENYA» i «contrasenyà» es tracten igual.

### Pas 2: Buscar senyals sospitoses

El detector revisa 9 indicadors. Cada indicador suma punts **una sola vegada**, encara que hi hagi diverses paraules del mateix tipus.

| Indicador | Què busca | Punts |
|---|---|---|
| 🔐 Sol·licita informació personal | «contrasenya», «dades bancàries», «número de targeta», «PIN», «DNI»... | **+30** |
| 🔗 Enllaç escurçat | `bit.ly`, `tinyurl.com`, `t.co`, `is.gd` | **+25** |
| ⏰ Missatges d'urgència | «urgent», «en 24 hores», «actua ara», «retingut», «caduca»... | **+20** |
| 💶 Demana un pagament | «paga», «pagament», «taxa», o quantitats com «2,95 €» | **+20** |
| 🎁 Promet un premi | «has guanyat», «premi», «sorteig»... | **+20** |
| 🌐 Conté enllaços | Qualsevol adreça que comenci per `http://` o `https://` | **+15** |
| 🕵️ Enllaç amb paraules sospitoses | Enllaços que contenen «login», «verifica», «actualitza», «pagament»... | **+15** |
| 🔓 Enllaç sense connexió segura | Enllaços que comencen per `http://` en lloc de `https://` | **+10** |
| 🏦 Esmenta una entitat o servei | «banc», «suport tècnic», «administrador», «PayPal», «Netflix»... | **+10** |

**Per què aquests punts?**

- **Demanar dades personals (30)** és el més greu, perquè és l'objectiu final del phishing.
- **Els enllaços escurçats (25)** amaguen la destinació real: no saps on et porten fins que hi cliques.
- **La urgència, els pagaments i els premis (20)** són trucs psicològics per fer-te actuar sense pensar.
- **Un enllaç (15)** pot ser normal, però gairebé tots els correus de phishing en porten.
- **Esmentar una entitat (10)** puntua poc perquè molts correus legítims també ho fan.

### Pas 3: Classificar el risc

Se sumen els punts (amb un màxim de 100) i es classifica el correu:

| Puntuació | Classificació |
|---|---|
| 60 – 100 | 🔴 **RISC ALT** |
| 30 – 59 | 🟠 **RISC MITJÀ** |
| 0 – 29 | 🟢 **RISC BAIX** |

---

## Millores per evitar errors

### Paraules completes

El detector busca **paraules senceres**. Així «banc» no es detecta dins de «bancàries» o «banca», i `t.co` no es confon amb adreces com `seguretat.com`.

### Frases de seguretat

Els correus legítims sovint avisen: *«Mai et demanarem la contrasenya»*. Per no confondre aquest avís amb una petició de dades, les frases que contenen expressions com «mai et demanarem», «no et demanarem» o «no comparteixis» **no compten** com a sol·licitud d'informació personal.

---

## Exemple

> *Correus: el teu paquet està retingut a la nostra oficina per una adreça incompleta. Paga 2,95 € de gestió per rebre'l: https://is.gd/paquet24*

| Indicador detectat | Punts |
|---|---|
| Missatges d'urgència («retingut») | +20 |
| Demana un pagament («Paga», «2,95 €») | +20 |
| Conté enllaços | +15 |
| Enllaç escurçat (`is.gd`) | +25 |
| **Total** | **80 → 🔴 RISC ALT** |

---

## Limitacions

Com que és un sistema basat en **regles fixes**, té limitacions:

- **No entén el context.** Només busca paraules; no sap si una frase és una amenaça o una broma.
- **Només coneix les paraules de les seves llistes.** Un estafador que faci servir expressions noves pot passar desapercebut.
- **No revisa el remitent** ni les capçaleres tècniques del correu.
- **No comprova on porten realment els enllaços** ni si un domini és fiable.
- **Pot donar falsos positius.** Una web legítima com `https://www.seguretat.com` suma punts perquè conté la paraula «seguretat».

Els filtres professionals (com els de Gmail o Outlook) combinen regles com aquestes amb **intel·ligència artificial** entrenada amb milions de correus, a més de comprovar la reputació dels remitents i dels dominis.

> ⚠️ **Important:** un resultat de risc baix **no garanteix** que el correu sigui segur. Davant del dubte, no cliquis cap enllaç i contacta directament amb l'entitat pels canals oficials.

---

## Estructura del projecte

```
Detector_Phishing/
├── detector.py   → Versió en Python per a la terminal
├── index.html    → Pàgina web (mateixa lògica en JavaScript)
├── img/          → Imatges de la web
└── README.md     → Aquest document
```

`detector.py` i `index.html` fan servir **exactament les mateixes regles**. Si es modifiquen les llistes de paraules en un fitxer, cal fer el mateix canvi a l'altre.

---

## Tecnologies

- **Python 3**: mòduls `re` (expressions regulars) i `unicodedata` (treure accents).
- **HTML, CSS i JavaScript**: pàgina web sense dependències externes.
- **GitHub Pages**: publicació de la web.

---

*Projecte educatiu. Tots els correus d'exemple són ficticis.*
