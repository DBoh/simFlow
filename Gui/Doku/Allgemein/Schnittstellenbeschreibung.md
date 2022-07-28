# Schnittstellenbeschreibung

>Anhand vom Beispielfall: 2022-04-06-simFlow-Beispielfall.pdf und PythonKonsoleBeispielfall.txt

Nach Drücken des `grünen A` importiert FreeCAD die Scripts CfdAnalysis, CfdTools, CfdPhysicsSelection, CfdFluidMaterial, CfdInitialiseFlowField und CfdSolverFoam.
 Ein Objekt `analysis` wird mit der Methode makeCfdAnalysis angelegt.
 Daraufhin werden jeweils die Eigenschaften `PhysicsSelection`, `FluidMaterial`, `Flowfields` und `Solverfoam` zur Analyse hinzugefügt.

Nachdrücken des `Netzsymbols` wird das Skript CfdMesh importiert.
 Das Skript erzeugt ein CfdMesh Objekt mit der Methode makeCfdMesh.
 CfdTools holt sich das CfdMesh Objekt und fügt es zur aktuellen Analyse hinzu.

Beim Drücken von `write mesh case` CfdMeshTools wird importiert und der Mesh case wird geschrieben.
 Sobald `run mesher` gedrückt wurde führt CfdTools die Methode makeRunCommand aus, um sich den Linux Befehl zur Ausführung in der relevanten Umgebung zu generieren und gibt sich daraufhin die Umgebungssettings zurück mit getRunEnvironment.
 Ein Objekt von CfdConsoleProcess wird erzeugt und als `mesh\_process` angelegt.

Nach dem Klicken von `PhysicsModel` legt FreeCAD ein Objekt an mit dem aktuellen PhysicsModel.
 Die jeweiligen Parameter werden für das Objekt gesetzt.
 Dies passiert durch `\_TaskPanelCfdPhysicsSelection.py`.

Dasselbe geschieht auch für `FluidProperties`.
 Im `TaskPanelCfdFluidProperties.py` kann man die jeweiligen Parameter einsehen.

 Zuletzt bei `InitialiseFields` auch die Parameter gesetzt.
 Im Beispielfall mit 100m/s auf X und einem Druck von 100000 Pascal.
 Diese werden auch durch `\_TaskPanelCfdInitialiseInternalFlowField.py` weitergegeben.

 Abschließend wird nachdem Drücken des `grünen Pfeils` der Case für die Analyse geschrieben mit `CfdCaseWriterFoam.py`.
 Es wird ein Objekt von `CfdSolver` unter den Namen `writer` angelegt und die Analyse kann nun ausgeführt werden mit `run`.