# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2015 - Qingfeng Xia <qingfeng.xia()eng.ox.ac.uk>        *
# *   Copyright (c) 2017 Alfred Bogaers (CSIR) <abogaers@csir.co.za>        *
# *   Copyright (c) 2017 Oliver Oxtoby (CSIR) <ooxtoby@csir.co.za>          *
# *   Copyright (c) 2017 Johan Heyns (CSIR) <jheyns@csir.co.za>             *
# *   Copyright (c) 2019-2022 Oliver Oxtoby <oliveroxtoby@gmail.com>        *
# *   Copyright (c) 2022 Jonathan Bergh <bergh.jonathan@gmail.com>          *
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
# Kommentare SimFlow
#
# Diagramm "Simulation residuals"
# Klasse CfdRunnable
# Klasse CfdRunnableFoam
#
# Input:
# Output:
#
# ***************************************************************************

from __future__ import print_function

import FreeCAD
import CfdTools
import CfdAnalysis
from PySide.QtCore import QObject, Signal
from collections import OrderedDict


class CfdRunnable(QObject, object):

    def __init__(self, analysis=None, solver=None):
        super(CfdRunnable, self).__init__()

        if analysis and isinstance(analysis.Proxy, CfdAnalysis._CfdAnalysis):
            self.analysis = analysis
        else:
            if FreeCAD.GuiUp:
                self.analysis = CfdTools.getActiveAnalysis()

        self.solver = None
        if solver:
            self.solver = solver
        else:
            if analysis:
                self.solver = CfdTools.getSolver(self.analysis)
            if not self.solver:
                FreeCAD.Console.printMessage("Solver object is missing from Analysis Object")

        if self.analysis:
            self.results_present = False
            self.result_object = None
        else:
            raise Exception('No active analysis found')

    def check_prerequisites(self):
        return ""


class CfdRunnableFoam(CfdRunnable):
    update_residual_signal = Signal(list, list, list, list)

    def __init__(self, analysis=None, solver=None):
        super(CfdRunnableFoam, self).__init__(analysis, solver)

        self.initResiduals()

    def check_prerequisites(self):
        return ""

    def initResiduals(self):
        self.UxResiduals = []
        self.UyResiduals = []
        self.UzResiduals = []
        self.pResiduals = []
        self.rhoResiduals = []
        self.EResiduals = []
        self.kResiduals = []
        self.epsilonResiduals = []
        self.omegaResiduals = []
        self.nuTildaResiduals = []
        self.gammaIntResiduals = []
        self.ReThetatResiduals = []
        self.time = []
        self.niter = 0
        self.latest_time = 0
        self.prev_time = 0
        self.latest_outer_iter = 0
        self.prev_num_outer_iters = 0
        self.solver.Proxy.residual_plot.reInitialise(self.analysis)

    def get_solver_cmd(self, case_dir):
        self.initResiduals()

        # Environment is sourced in run script, so no need to include in run command
        cmd = CfdTools.makeRunCommand('./Allrun', case_dir, source_env=False)
        FreeCAD.Console.PrintMessage("Solver run command: " + ' '.join(cmd) + "\n")
        return cmd

    def getRunEnvironment(self):
        return CfdTools.getRunEnvironment()

    def process_output(self, text):
        log_lines = text.split('\n')
        prev_niter = self.niter
        for line in log_lines:
            split = line.split()

            # Only record the first residual per outer iteration
            if line.startswith(u"Time = "):
                self.prev_time = self.latest_time
                self.latest_time = float(line.lstrip(u"Time = "))
                self.prev_num_outer_iters = self.latest_outer_iter
                if self.latest_time > 0:
                    # Don't keep spurious time zero
                    self.latest_outer_iter = 0
                    self.niter += 1
            if line.find(u"PIMPLE: iteration ") >= 0 or line.find(u"pseudoTime: iteration ") >= 0:
                self.latest_outer_iter += 1
                # Don't increment counter on first outer iter as this was already done with time
                if self.latest_outer_iter > 1:
                    self.niter += 1

            # Add a point to the time axis for each outer iteration
            if self.niter > len(self.time):
                self.time.append(self.latest_time)
                if self.latest_outer_iter > 0:
                    # Outer-iteration case
                    # Create virtual times to space the residuals of the outer iterations nicely on the time graph
                    self.prev_num_outer_iters = max(self.prev_num_outer_iters, self.latest_outer_iter)
                    for i in range(self.latest_outer_iter):
                        self.time[-(self.latest_outer_iter-i)] = self.prev_time + (
                            self.latest_time-self.prev_time)*((i+1)/self.prev_num_outer_iters)

            if "Ux," in split and self.niter > len(self.UxResiduals):
                self.UxResiduals.append(float(split[7].split(',')[0]))
            if "Uy," in split and self.niter > len(self.UyResiduals):
                self.UyResiduals.append(float(split[7].split(',')[0]))
            if "Uz," in split and self.niter > len(self.UzResiduals):
                self.UzResiduals.append(float(split[7].split(',')[0]))
            if "p," in split and self.niter > len(self.pResiduals):
                self.pResiduals.append(float(split[7].split(',')[0]))
            if "p_rgh," in split and self.niter > len(self.pResiduals):
                self.pResiduals.append(float(split[7].split(',')[0]))
            if "h," in split and self.niter > len(self.EResiduals):
                self.EResiduals.append(float(split[7].split(',')[0]))
            # HiSA coupled residuals
            if "Residual:" in split and self.niter > len(self.rhoResiduals):
                self.rhoResiduals.append(float(split[4]))
                self.UxResiduals.append(float(split[5].lstrip('(')))
                self.UyResiduals.append(float(split[6]))
                self.UzResiduals.append(float(split[7].rstrip(')')))
                self.EResiduals.append(float(split[8]))
            if "k," in split and self.niter > len(self.kResiduals):
                self.kResiduals.append(float(split[7].split(',')[0]))
            if "epsilon," in split and self.niter > len(self.epsilonResiduals):
                self.epsilonResiduals.append(float(split[7].split(',')[0]))
            if "omega," in split and self.niter > len(self.omegaResiduals):
                self.omegaResiduals.append(float(split[7].split(',')[0]))
            if "nuTilda," in split and self.niter > len(self.nuTildaResiduals):
                self.nuTildaResiduals.append(float(split[7].split(',')[0]))
            if "gammaInt," in split and self.niter > len(self.gammaIntResiduals):
                self.gammaIntResiduals.append(float(split[7].split(',')[0]))
            if "ReThetat," in split and self.niter > len(self.ReThetatResiduals):
                self.ReThetatResiduals.append(float(split[7].split(',')[0]))

        if self.niter > 1 and self.niter > prev_niter:
            self.solver.Proxy.residual_plot.updateResiduals(self.time, OrderedDict([
                ('$\\rho$', self.rhoResiduals),
                ('$U_x$', self.UxResiduals),
                ('$U_y$', self.UyResiduals),
                ('$U_z$', self.UzResiduals),
                ('$p$', self.pResiduals),
                ('$E$', self.EResiduals),
                ('$k$', self.kResiduals),
                ('$\\epsilon$', self.epsilonResiduals),
                ('$\\tilde{\\nu}$', self.nuTildaResiduals),
                ('$\\omega$', self.omegaResiduals),
                ('$\\gamma$', self.gammaIntResiduals),
                ('$Re_{\\theta}$', self.ReThetatResiduals)]))
