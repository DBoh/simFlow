# Erweiterung CfdSolver

Um weitere CfdSolver Eigenschaften hinzuzufügen muss man im Sourcecode unter **data -> defaults -> system ->
controlDict** die Eigenschaften, die nicht änderbar sind, anpassen.
So wie im unten angehängten Beispiel zum TimeStep, welches vorher festegelegt war als 1 und nun in der GUI in FreeCad anpassbar ist.

![steadyTimeStep](https://user-images.githubusercontent.com/80594490/173585733-54a3fa5c-e1c4-4a94-bc10-5eea8f6842d3.PNG)

Des Weiteren muss man im Sourcecode in der Datei **CfdSolverFoam.py** in der Methode **initProperties** die Eigenschaften mitgeben.

![steadyTimeStep2](https://user-images.githubusercontent.com/80594490/173586571-8ae75112-52ba-44ed-b608-0f3758c13444.PNG)

Damit die Eigenschaft unter CfdSolver angelegt und angezeigt wird reicht ein Neustart der FreeCAD Anwendung.

![steadyTimeStep3](https://user-images.githubusercontent.com/80594490/173587944-74f428ed-6585-433b-a43b-169755f5885f.PNG)
