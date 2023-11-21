dashboard_helptext = """
**Warum dises Dashboard?**\n
Sich einen Überblick über die privaten Finanzen zu verschaffen kann schnell zu einer Zeitintensiven Aufgabe werden.
Dadurch bleiben hohe Kosten, die sich über längere Zeiträume akkumulieren oft unentdeckt. 
Dieses Dashboard dient dazu, diese Kosten zu finden. Hat man dies geschafft, lässt sich entscheiden, wie nötig bzw.
unnötig diese sind, um sie ggf. zu vermeiden. 
\n
Dieses Dashboard liest den CSV-Export von Kontoauszügen aus. Die Daten werden automatisch in Kategorien,
die vom Nutzer in der Datei 'config.toml' definiert werden können, eingeteilt. Dazu wird nach Stichworten in der
Spalte 'Zahlungsempfänger*In' gesucht.
Anschließend werden die Daten für verschiedene Visualisierungen verarbeitet. Siehe dazu die jeweiligen Beschreibungen
der Graphen. Über alle Graphen kann man für mehr Informationen hovern.
Der Fokus liegt auf die Ausgaben.

Folgende Visualisierungen sind Teil dieses Dashboards:
Jeder Visualisierung hat zusätzlich einen eigenen Hilfstext. Einfach über das Fragezeichen hovern.

1. **Ausgabenzusammensetzung seit nutzerdefiniertem Datum.**\n
    * Ausgaben nach Kategorien:
            Zusammensetzung der Ausgaben seit einem nutzerdefiniertem Datum (Tortendiagramm)
    * Top-10 Ausgaben seit dem selben nutzerdefiniertem Datum:
            Die 10 größten Transaktionen werden tabellarisch angezeigt.

2. **Einnahmen und Ausgaben:**\n
    * Aufstellung der Einnahmen und Ausgaben aller Zeiten. Gruppierbar in Wochen, Monate und Jahre.

3. **Verteilung der Ausgabenbeträge:**\n
    * Alle Ausgaben in jeweilige Betragsspannen unterteilt aufsummiert.
    Die Betragsspannen sind der X-Achse zu entnehmen.

4. **Saisonale Analyse der Ausgaben:**\n
    * Alle Ausgaben summiert nach Wochentag
    * Alle Ausgaben summiert nach Monat

5. **Unkategorisierte Ausgaben:**\n
    * Mithilfe der Stichwortsuche können nicht alle Ausgaben einer Kategorie zugeordnet werden,
    wodurch einige Ausgaben manuell geprüft werden müssen.
    Über "von" und "bis" kann der Zu betrachtende Zeitraum definiert werden.
    Alle unkategorisierten Ausgaben in diesem Zeitpunkt werden tabellarisch angelistet.
    Durch Anklicken der Spaltennahmen, lässt sich nach diesen sortieren.
    Z.B. "Betrag_absolut" um die größten unkategorisierten Ausgaben in diesem Zeitraum
    zu ermitteln.
"""

categories_pie_helptext = """
Dieses Diagram unterteilt die Ausgaben in Kategorien
seit einem definierbarem Datum.
In der Datei 'config.toml' können diese Kategorien und
zugehörige Stichworte definiert werden.

Standardmäßig werden die Daten von 1 Jahr vor dem neusten Datenpunkt bis zum neusten Datenpunkt einbezogen.

Das diagram ist interaktiv.
Hovern für details.
In der Legende lassen sich Kategorien durch Klicken
ein- und ausblenden


Ziel des Diagrammes:
Überblick über die größten Kostenfaktoren.
"""

top_ten_helptext = """
Tabelle mit den 10 größten Ausgaben seit dem angegebenen Datum.

Standardmäßig werden die Daten von 1 Jahr vor dem neusten Datenpunkt bis zum neusten Datenpunkt einbezogen.

Das diagram ist interaktiv.
Hovern für details.


Ziel des Diagrammes:
Schneller Zugriff auf die größten Ausgaben.
"""

statement_of_costs_helptext = """
Balkendiagramm mit Einnahme (grün) und Ausgaben (rot).
Zeitraum nicht definierbar.

Auswählbar, ob nach Woche, Monat oder Jahr gruppiert. Standardmäßig jährlich.s

Das diagram ist interaktiv.
Hovern für details.


Ziel des Diagrammes:
Überblick über Einnahmen und Ausgaben im Vergleich.
"""

distribution_of_costs_helptext = """
Alle Ausgaben in Betragsspannen gruppiert und summiert.

Zeitraum nicht definierbar.

Das diagram ist interaktiv.
Hovern für details.


Ziel des Diagrammes:
Überblick darüber, welche Beträge die größten Ausgaben verursachen.
"""

saisonal_analysis_helptext = """
Balkendiagramme mit der Summe aller Ausgaben in 2 Gruppierungen
1. Nach Wochentagen
2. Nach Monaten

Das diagram ist interaktiv.
Hovern für details.
"""

uncategorized_helptext = """
Alle unkategorisierten Ausgaben im ausgewählten Zeitraum ("von"-"bis")

Durch das Anklicken der Spaltennamen, lassen sich diese sortieren.
"Betrag_absolut" sotiert nach Höhe der Ausgaben

Das diagram ist interaktiv.
Hovern für details.
"""