# Scripts and Files for the Python Workshop at SLUB 2019 

Das Modul `slub_scrapber.py` stellt einige Funktionen zur Verfügung, um Mets-Dateien von einer OAI-Schnittstelle herunterzuladen, einzelne Records auf der Festplatte abzuspeichern und diese nach bibliographischen Angaben zu durchsuchen.

Es wurde entwickelt, um als Beispielsammlung für einen Python-Workshop im [TextLab](https://www.slub-dresden.de/service/textlab/) der [SLUB](https://www.slub-dresden.de/startseite/) zu dienen. Es steht jedem frei, damit zu tun, was man möchte.

`download_xml(url, output_path)`: Lädt eine XML-Datei von der übergebenen URL (z.B. 'https://digital.slub-dresden.de/oai/?verb=ListRecords&metadataPrefix=mets&set=15th-century-prints') und speichert sie in dem angegebenen Pfad (z.B. 'data') ab.

`find_places(path)`: Durchsucht jede Datei im angegebenen Pfadt (z.B. `'data/*.mets'`) nach dem Publikationsort.

Vergleichbare Funktionen sind `find_authors()`, `find_publishers()`, `find_titles()` und `find_issue_date()`. Sie erwarten alle eine Pfadangabe mit gespeicherten Mets-Dateien als Argument und geben jeweils ein Generator-Objekt zurück. Es können also Aufrufe wie folgt aussehen:

```python
for author in find_authors('data/*.mets'):
    print(author)
```

`works(path)` erstellt eine Liste, in der jedes Element ein Dictionary mit den bibliographischen Angaben für einen Eintrag ist.

`write_files(input_path, output_path)` nimmt eine einzelne Mets-Datei aus dem `input_path`, sucht die einzelnen Einträge heraus und schreibt diese in den `output_path`.
