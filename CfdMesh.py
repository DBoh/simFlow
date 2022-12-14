# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2016 - Bernd Hahnebach <bernd@bimstatik.org>            *
# *   Copyright (c) 2019 Oliver Oxtoby <oliveroxtoby@gmail.com>             *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

# ***************************************************************************
#
# Kommentare SimFlow
#
# cfDMesh erstellen
# Erstellung einses Mesh Objects
# Viewer für das cfDMesh Object
#
# Input:
# Output: CfdMeshRefinement
#
# ***************************************************************************

from __future__ import print_function

import FreeCAD
import FreeCADGui
from PySide import QtCore
import CfdTools
from CfdTools import addObjectProperty
import os


MESHER_DESCRIPTIONS = ['cfMesh', 'snappyHexMesh', 'gmsh (tetrahedral)', 'gmsh (polyhedral dual mesh)']
MESHERS = ['cfMesh', 'snappyHexMesh', 'gmsh', 'gmsh']
DIMENSION = ['3D', '3D', '3D', '3D']
DUAL_CONVERSION = [False, False, False, True]


def makeCfdMesh(name="CFDMesh"):
    obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", name)
    _CfdMesh(obj)
    if FreeCAD.GuiUp:
        _ViewProviderCfdMesh(obj.ViewObject)
    return obj


class _CommandCfdMeshFromShape:
    def GetResources(self):
        icon_path = os.path.join(CfdTools.get_module_path(), "Gui", "Resources", "icons", "mesh.png")
        return {'Pixmap': icon_path,
                'MenuText': QtCore.QT_TRANSLATE_NOOP("Cfd_MeshFromShape",
                                                     "CFD mesh"),
                'ToolTip': QtCore.QT_TRANSLATE_NOOP("Cfd_MeshFromShape",
                                                    "Create a mesh using cfMesh, snappyHexMesh or gmsh")}

    def IsActive(self):
        sel = FreeCADGui.Selection.getSelection()
        analysis = CfdTools.getActiveAnalysis()
        return analysis is not None and sel and len(sel) == 1 and sel[0].isDerivedFrom("Part::Feature")

    def Activated(self):
        FreeCAD.ActiveDocument.openTransaction("Create CFD mesh")
        analysis_obj = CfdTools.getActiveAnalysis()
        if analysis_obj:
            meshObj = CfdTools.getMesh(analysis_obj)
            if not meshObj:
                sel = FreeCADGui.Selection.getSelection()
                if len(sel) == 1:
                    if sel[0].isDerivedFrom("Part::Feature"):
                        mesh_obj_name = sel[0].Name + "_Mesh"
                        FreeCADGui.doCommand("")
                        FreeCADGui.addModule("CfdMesh")
                        FreeCADGui.doCommand("CfdMesh.makeCfdMesh('" + mesh_obj_name + "')")
                        FreeCADGui.doCommand("App.ActiveDocument.ActiveObject.Part = App.ActiveDocument." + sel[0].Name)
                        if CfdTools.getActiveAnalysis():
                            FreeCADGui.addModule("CfdTools")
                            FreeCADGui.doCommand(
                                "CfdTools.getActiveAnalysis().addObject(App.ActiveDocument.ActiveObject)")
                        FreeCADGui.ActiveDocument.setEdit(FreeCAD.ActiveDocument.ActiveObject.Name)
        else:
            print("ERROR: You cannot have more than one mesh object")
        FreeCADGui.Selection.clearSelection()


class _CfdMesh:
    """ CFD mesh properties """

    # Variables that need to be used outside this class and therefore are included outside of
    # the constructor
    known_element_dimensions = ['2D', '3D']

    def __init__(self, obj):
        self.Type = "CfdMesh"
        self.Object = obj
        obj.Proxy = self
        self.initProperties(obj)

    def initProperties(self, obj):
        addObjectProperty(obj, 'CaseName', "meshCase", "App::PropertyString", "",
                          "Name of directory in which the mesh is created")

        # Setup and utility
        addObjectProperty(obj, 'STLLinearDeflection', 0.05, "App::PropertyFloat", "", "STL linear deflection")

        addObjectProperty(obj, 'NumberOfProcesses', 1, "App::PropertyInteger", "",
                          "Number of parallel processes (only applicable to cfMesh and snappyHexMesh)")

        addObjectProperty(obj, 'NumberOfThreads', 0, "App::PropertyInteger", "",
                          "Number of parallel threads per process (only applicable to cfMesh and gmsh). "
                          "0 means use all available (if NumberOfProcesses = 1) or use 1 (if NumberOfProcesses > 1)")

        addObjectProperty(obj, "Part", None, "App::PropertyLink", "Mesh Parameters", "Part object to mesh")

        if addObjectProperty(obj, "MeshUtility", MESHERS, "App::PropertyEnumeration",
                             "Mesh Parameters", "Meshing utilities"):
            obj.MeshUtility = MESHERS[0]

        # Refinement
        addObjectProperty(obj, "CharacteristicLengthMax", "0 m", "App::PropertyLength", "Mesh Parameters",
                          "Max mesh element size (0.0 = infinity)")

        addObjectProperty(obj, 'PointInMesh', {"x": '0 m', "y": '0 m', "z": '0 m'}, "App::PropertyMap",
                          "Mesh Parameters",
                          "Location vector inside the region to be meshed (must not coincide with a cell face)")

        addObjectProperty(obj, 'CellsBetweenLevels', 3, "App::PropertyInteger", "Mesh Parameters",
                          "Number of cells between each level of refinement")

        addObjectProperty(obj, 'EdgeRefinement', 1, "App::PropertyFloat", "Mesh Parameters",
                          "Relative edge (feature) refinement")

        # PolyDualMesh
        addObjectProperty(obj, 'ConvertToDualMesh', True, "App::PropertyBool", "Mesh Parameters",
                          "Convert to polyhedral dual mesh")

        # Edge detection, implicit / explicit (NB Implicit = False implies Explicit = True)
        addObjectProperty(obj, 'ImplicitEdgeDetection', False, "App::PropertyBool", "Mesh Parameters",
                          "Use implicit edge detection")

        # Mesh dimension
        if addObjectProperty(obj, 'ElementDimension', _CfdMesh.known_element_dimensions, "App::PropertyEnumeration",
                             "Mesh Parameters", "Dimension of mesh elements (Default 3D)"):
            obj.ElementDimension = '3D'

    def onDocumentRestored(self, obj):
        self.initProperties(obj)

    def execute(self, obj):
        pass

    def __getstate__(self):
        return self.Type

    def __setstate__(self, state):
        if state:
            self.Type = state


class _ViewProviderCfdMesh:
    """ A View Provider for the CfdMesh object """
    def __init__(self, vobj):
        vobj.Proxy = self
        self.taskd = None

    def getIcon(self):
        icon_path = os.path.join(CfdTools.get_module_path(), "Gui", "Resources", "icons", "mesh.png")
        return icon_path

    def attach(self, vobj):
        self.ViewObject = vobj
        self.Object = vobj.Object

    def updateData(self, obj, prop):
        return

    def onChanged(self, vobj, prop):
        CfdTools.setCompSolid(vobj)
        return

    def setEdit(self, vobj, mode):
        for obj in FreeCAD.ActiveDocument.Objects:
            if hasattr(obj, 'Proxy') and isinstance(obj.Proxy, _CfdMesh):
                obj.ViewObject.show()
        import _TaskPanelCfdMesh
        self.taskd = _TaskPanelCfdMesh._TaskPanelCfdMesh(self.Object)
        self.taskd.obj = vobj.Object
        FreeCADGui.Control.showDialog(self.taskd)
        return True

    def unsetEdit(self, vobj, mode):
        if self.taskd:
            self.taskd.closed()
            self.taskd = None
        FreeCADGui.Control.closeDialog()

    def doubleClicked(self, vobj):
        if FreeCADGui.activeWorkbench().name() != 'CfdOFWorkbench':
            FreeCADGui.activateWorkbench("CfdOFWorkbench")
        gui_doc = FreeCADGui.getDocument(vobj.Object.Document)
        if not gui_doc.getInEdit():
            gui_doc.setEdit(vobj.Object.Name)
        else:
            FreeCAD.Console.PrintError('Task dialog already open\n')
        return True

    def onDelete(self, feature, subelements):
        try:
            for obj in self.Object.Group:
                obj.ViewObject.show()
        except Exception as err:
            FreeCAD.Console.PrintError("Error in onDelete: " + str(err))
        return True

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None
