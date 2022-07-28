# Dokumentation Befehle 
| Befehl                                               | Beschreibung                                                                                                                                                                                                                              |
|:-----------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FreeCADGui.addCommand(string, object)                | Fügt einen FreeCAD-Befehl hinzu. String ist der Name des Befehls und Objekt ist ein Klassenname, der den Befehl definiert                                                                                                                 |
| FreeCADGui.doCommand(string)                         | Ausführung des mitgegeben Strings in der FreeCAD Console. </br> Beispiel: </br> `FreeCADGui.doCommand("FreeCAD.getDocument('"+self.__class__.__doc_name+"').recompute()")` (aus TestCfdOf.py)                                             |
| FreeCADGui.ActiveDocument.setEdit(object)            | Um den Bearbeitungsmodus eines Objekts zu aktivieren, verwenden Sie die setEdit-Methode des Dokumentobjekts. <br/>Beispiel: `FreeCADGui.ActiveDocument.setEdit(FreeCAD.ActiveDocument.ActiveObject.Name)` (aus CfdInitialiseFlowField.py) |
| FreeCADGui.ActiveDocument.resetEdit()                | Um den Bearbeitungsmodus eines Objekts zu deaktivieren, verwenden Sie die Methode resetEdit des Dokumentobjekts. <br/>Beispiel: `FreeCADGui.ActiveDocument.resetEdit()`  (aus _TaskPanelCfdMesh.py)                                       |
| FreeCADGui.getDocument(documentName)                 | Ruft das angegeben Dokument auf. Rückgabewert ist hier das Dokument.  </br> Beispiel: </br> `App.getDocument('Unnamed').getObject('CfdAnalysis').ViewObject.doubleClicked()` (aus PythonKonsolenBeispielFall.txt)                         |
| FreeCADGui.Selection.addSelection(object, selection) | Um ein Objekt zur Selektion hinzuzufügen. </br> Beispiel: </br> `Gui.Selection.addSelection('Unnamed','CfdAnalysis')` (aus PythonKonsolenBeispielFall.txt)                                                                                |
| FreeCADGui.Selection.clearSelection()                | Löscht das mitgegebene Dokument aus der Selection. Wenn kein Dokument übergeben, wird die komplette Selection geleert </br> Beispiel: </br> `Gui.Selection.clearSelection()` (aus PythonKonsolenBeispielFall.txt)                         |

## Quellen:
- https://wiki.freecadweb.org/FreeCAD_Scripting_Basics/de
- https://freecad.github.io/SourceDoc/modules.html
- https://wiki.freecadweb.org/Std_Edit 
- https://wiki.freecadweb.org/Selection_API
- https://wiki.freecadweb.org/FreeCADGui_API
- https://forum.freecadweb.org/viewtopic.php?t=23925