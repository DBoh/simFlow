# CfdOF: A Computational fluid dynamics (CFD) workbench for FreeCAD

# Installation von CfdOF

> Unser Team testet nur die Installation auf Windows.

## Linux 

> Es gibt in dem Main-Repository dazu eine Anleitung auf Englisch die genutzt werden kann.
> 
> Main-Repository: [https://github.com/jaheyns/CfdOF](https://github.com/jaheyns/CfdOF)


## iOS
> Die Installation für iOS Nutzer ist im Forum vom Main-Repository erklärt, jedoch weder in dieser Anleitung noch in der im Main-Repository

## Windows

### 1. FreeCAD installieren

> Link um FreeCAD zu downloaden: [https://www.freecadweb.org/downloads.php](https://www.freecadweb.org/downloads.php)

Den Windows 64-Bit Installer auswählen. Nach Download den Installer öffnen.

![install_FreeCAD](Gui/Resources/media/Anleitung/freeCADinstaller.png)

Hier können die Standardeinstellungen übernommen werden. Solange weiter drücken bis das unten gezeigte Fenster kommt.

![Finished_Installation](Gui/Resources/media/Anleitung/installiertFreeCAD.png)

Optional: Checkbox `FreeCAD starten` auswählen

Durch `Fertigstellen` wird FreeCAD installiert und ggfs. direkt geöffnet.

### 2. CfdOF installieren

Über `Tools->Add-on Manager` die Workbench öffnen.

![Open_Workbench](Gui/Resources/media/Anleitung/Addon_Manager.png)

In der Workbench `Plot` auswählen und auf `Install/update selected` um Plot herunterzuladen.

![install_Plot](Gui/Resources/media/Anleitung/Plot_install.png)

Das gleiche jetzt bei CfdOF machen. Also in der Workbench `CfdOF` auswählen und auf `Install/update selected` klicken.

![Install_CfdOF](Gui/Resources/media/Anleitung/CfdOF_install.png)

Nach der erfolgreichen Installation von Plot und CfdOF muss FreeCAD neugestartet werden.

Optional: Nach dem Neustart von FreeCAD kann in der Workbench nach geschaut werden, ob alles installiert wurde.

### 3. BlueCfd installieren

> Link um BlueCfd zu downloaden: [https://bluecfd.github.io/Core/](https://bluecfd.github.io/Core/)

Den Link Link zu BlueCfd öffnen. Dieser führt auf eine Webseite und hier durch das Menü, links, `Downloads` auswählen. 

Hier die neuste Version auswählen.
Die `.exe` anklicken, dadurch wird die Datei heruntergeladen. 

![BlueCfd_Website](Gui/Resources/media/Anleitung/blueCfd.png)

Nach Download die Datei öffnen.

![BlueCfd_installation](Gui/Resources/media/Anleitung/blueCfd_installer.png)

Die Standardeinstellungen können übernommen werden und das License Agreement muss zugestimmt werden. 
Das solange fortführen bis das unten gezeigte Fenster erscheint. 

![BlueCfd_finished_installation](Gui/Resources/media/Anleitung/finished_blueCfd_install.png)

Hier müssen die Checkboxen nicht ausgewählt werden. Dann durch `Finish` die Installation beenden.
Nach der Installation sollten 2 Anwendung-Icons auf dem Desktop erscheinen.

![BlueCfd_Desktop_Icons](Gui/Resources/media/Anleitung/blueCfd_icons.png)

Die Installation von BlueCfd ist dann abgeschlossen.

### 4. Dependencies herunterladen

Über `Edit->Preferences` die Einstellungen öffnen.

![Preferences](Gui/Resources/media/Anleitung/preferences.png)

> Am Besten im Vorfeld ein neuen Ordner in eurem persönlichen Verzeichnis für das Projekt erstellen

Unter `CfdOF` das `default-output-directory` zu dem Ordner umändern, der für das Projekt bestimmt ist.

![install_dependencies](Gui/Resources/media/Anleitung/dependency_preferences.png)

#### OpenFoam installieren

Dann bei `Software Dependecies` durch den Button `Install OpenFOAM` OpenFOAM installieren.
Ein neuen Fenster öffnet sich, für die Installation von OpenFOAM.

![OpenFOAM_installation](Gui/Resources/media/Anleitung/openFoam_install.png)

Hier können die Standardeinstellungen übernommen und dem License Agreement muss zugestimmt werden.

Die Installation kann eine Weile dauern.

#### ParaView installieren

Um ParaView zu installieren, wie bei OpenFOAM unter `Software Dependecies` den Button `Install ParaView` anklicken.
Hier sollte sich ebenfalls ein neues Fenster öffnen.

![ParaView_installation](Gui/Resources/media/Anleitung/paraview_install.png)

Hier können die Standardeinstellungen übernommen werden.

#### cfMesh und HiSA installieren

cfMesh und HiSA können wie die beiden Dependencies oben, nacheinander durch den Button unter `Software Dependecies` installiert werden.

Den Fortschritt der Installation kann in dem Output Fenster verfolgt werden. 
Erst nach erfolgreicher Installation von cfMesh kann HiSa installiert werden.

#### Pfade aktualisieren

Die Pfade zu dem `OpenFOAM install directory` und `ParaView executable path` müssen in den Preferences noch angegeben werden.

Hier ist das Verzeichnis zu OpenFOAM:

![OpenFOAM_install_directory](Gui/Resources/media/Anleitung/openFoam_fileexplorer.png)

Hier ist die `.exe` Datei für ParaView zu finden:

![ParaView_exe](Gui/Resources/media/Anleitung/paraview_fileexplorer.png)

Die beiden Pfade zu den jeweilgen Verzeichnissen/Dateien in den Preferences mit Hilfe von `...` eintragen.

Dann sollte die Preferences wie folgt aussehen:

![dependency_links](Gui/Resources/media/Anleitung/dependency_links.png)

#### Dependency Check

Um zu testen, ob auch alle Dependecies erfolgreich installiert und aufrufbar sind, kann unter `Preferences` das `Run dependency checker` ausgeführt werden.

Im Output-Fenster sollte angezeigt werden, dass alle Dependencies gefunden wurden. (siehe Abbildung)
![dependency_check](Gui/Resources/media/Anleitung/dependency_check.png)

Die Installation von allen relevanten Programmen ist damit abgeschlossen.

# Testing

## simFlow Beispielfall 

Öffnen in FreeCAD von `01-geom.fcmacro` aus dem Ordner `…\cfdOF\demos\Duct` 

![Open_File](Gui/Resources/media/Test/Open.png)

Auf den grünen Pfeil drücken (im Start-Workbench)

![Start_Project](Gui/Resources/media/Test/Start.png)

Nun links im Modell `Fusio` anwählen und auf die Workbench `cfdOF` wechseln. 

Über das grüne `A` (s. Screenshot) ein CfdAnalysis-Modell erzeugen  

![CfdOF](Gui/Resources/media/Test/CfdOF.png)

Über das Netzsymbol (s. Screenshot) ein Netz erzeugen: 

![Netzsymbol](Gui/Resources/media/Test/Netzsymbol.png)

hierfür `Write mesh case` drücken. 
Anschließend `Run Mesher`. Über Paraview-Button kann man sich das Netz anschauen. Danach `Close` drücken. 

![CFO_Mesh_Window](Gui/Resources/media/Test/Window.png)

Nun müssten im Modell folgende Unterfelder eingerichtet sein:  

![Modell_Menu](Gui/Resources/media/Test/Menu.png)

Zunächst muss das `PhysicsModel` gewählt werden, hierfür in der Taskleiste auf das entsprechende Symbol gehen. Nichts ändern und OK drücken. 

 ![Symbol_PhysicsModel](Gui/Resources/media/Test/PhysicsModel.png)

Anschließend die `FluidProperties` auswählen. Nichts ändern und OK drücken. 

![Symbol_FluidProperties](Gui/Resources/media/Test/FluidProperties.png)

Anschließend die InitialiseFields setzen (Anfangsbedingungen). Wähle über `Specify Values` irgendeine Anfangsgeschwindigkeit, z.B. 100 mm/s für U_x, sonst Null, und irgendeinen Anfangsdruck, z.B. 100000 Pa. Auf OK klicken 

![Symbol_InitialiseFields](Gui/Resources/media/Test/InitialiseFields.png)

![Fluid_Properties_Window](Gui/Resources/media/Test/Case.png)

Nun kann der Case gerechnet werden, indem du auf den grünen Pfeil drückst. Erst `Write`,
dann `Run` drücken. In der Konsole sollten die Zwischenergebnisse der Rechnung sehen, 
das ist die Ausgabe von Openfoam. 

![Run_Case](Gui/Resources/media/Test/Write.png)

![View_Case](Gui/Resources/media/Test/Grafik.png)

Die Ergebnisse der einzelnen Teilschritte werden entsprechend der Ordner-Struktur von Openfoam in den von dir angegebenen Outputordner geschrieben:  

![View_File_Explorer](Gui/Resources/media/Test/Output_Ordner.png)

Das Netz z.B. in den Ordner `meshCase`: 

![View_meshCase_directory](Gui/Resources/media/Test/meshCase_Ordner.png)

Der Case, den man rechnet, in den Ordner `case`. Hier finden Sie alle Ihre Einstellungen aus der GUI wieder. 

![View_Case_directory](Gui/Resources/media/Test/case_Ordner.png)
