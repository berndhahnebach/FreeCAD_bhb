# ***************************************************************************
# *   Copyright (c) 2019 Bernd Hahnebach <bernd@bimstatik.org>              *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
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

__title__ = "OOFEM Writer"
__author__ = "Bernd Hahnebach"
__url__ = "http://www.freecadweb.org"

## \addtogroup FEM
#  @{

import time

import FreeCAD

from .. import writerbase
from femmesh import meshtools


class FemInputWriterOOFEM(writerbase.FemInputWriter):
    def __init__(
        self,
        analysis_obj,
        solver_obj,
        mesh_obj,
        member,
        dir_name=None,
        write_comments=True
        # write comments is a parameter value in this inherited class only
        # thus we do not pass it to instantiate the FemInputWriter class
    ):
        writerbase.FemInputWriter.__init__(
            self,
            analysis_obj,
            solver_obj,
            mesh_obj,
            member,
            dir_name
        )
        # comments
        self.write_comments = write_comments

        # working dir and input file
        from os.path import join
        self.main_file_name = self.mesh_object.Name + ".in"
        self.file_name = join(self.dir_name, self.main_file_name)
        FreeCAD.Console.PrintLog(
            "FemInputWriterOOFEM --> self.dir_name  -->  {}\n"
            .format(self.dir_name)
        )
        FreeCAD.Console.PrintLog(
            "FemInputWriterOOFEM --> self.main_file_name  -->  {}\n"
            .format(self.main_file_name)
        )
        FreeCAD.Console.PrintMessage(
            "FemInputWriterOOFEM --> self.file_name  -->  {}\n"
            .format(self.file_name)
        )

    def write_oofem_input_file(self):

        timestart = time.clock()

        """
        # once we gone need the nodes, we may recode the mesh writer
        # because we would get the nodes twice
        if not self.femnodes_mesh:
            self.femnodes_mesh = self.femmesh.Nodes
        """
        if not self.femelement_table:
            self.femelement_table = meshtools.get_femelement_table(self.femmesh)
            self.element_count = len(self.femelement_table)

        inpfile = open(self.file_name, "w")

        self.write_output_file_record(inpfile)

        self.write_job_description_record(inpfile)

        self.write_analysis_record(inpfile)

        self.write_domain_record(inpfile)

        self.write_output_manager_record(inpfile)

        self.write_components_size_record(inpfile)

        self.write_dof_manager_record(inpfile)

        self.write_node_and_element_records(inpfile)

        self.write_cross_section_record(inpfile)

        self.write_material_type_record(inpfile)

        self.write_boundary_condition_record(inpfile)

        self.write_nodal_load_record(inpfile)

        self.write_time_function_record(inpfile)

        self.write_set_record(inpfile)

        # footer
        self.write_footer(inpfile)
        inpfile.close()
        writing_time_string = (
            "Writing time input file: {} seconds"
            .format(round((time.clock() - timestart), 2))
        )
        FreeCAD.Console.PrintMessage(writing_time_string + " \n\n")
        return self.file_name

    def write_output_file_record(self, f):
        """ output filename String """
        if self.write_comments is True:
            f.write("#\n")
            f.write("# {}\n".format(67 * "*"))
            f.write("# OOFEM Output File Name Record\n")
            f.write("#\n")
        f.write(self.mesh_object.Name + ".out\n")

    def write_job_description_record(self, f):
        """ Job description string """
        if self.write_comments is True:
            f.write("#\n")
            f.write("#\n")
            f.write("# {}\n".format(67 * "*"))
            f.write("# Description Record\n")
            f.write("#\n")
        f.write(self.document.Name + "\n")

    def write_analysis_record(self, f):
        """ *AnalysisType
                *nsteps # (in)
                 [renumber # (in) ]
                 [profileopt # (in) ]
                 attributes # (string)
                 [ninitmodules # (in) ]
                 [nmodules # (in) ]
                 [nxfemman # (in) ]

                *StaticStructural
                 nsteps # (in)
                 [deltat # (...) ]
                 [prescribedtimes # (...) ]
                 [stiffmode # (...) ]
                 [nonlocalext # (...) ]
                 [sparselinsolverparams # (...) ]

                *LinearStability
                 nroot # (in)
                 rtolv # (rn)
                 [eigensolverparams # (...) ]

                *NonLinearStatic
                 [nmsteps # (in) ]
                 nsteps # (in)
                 [contextOutputStep # (in) ]
                 [sparselinsolverparams # (string) ]
                 [nonlinform # (in) ]
                 [nonlocstiff # (in) ]
                 [nonlocalext]
                 [loadbalancing]
        """
        if self.write_comments is True:
            f.write("#\n")
            f.write("#\n")
            f.write("# {}\n".format(67 * "*"))
            f.write("# Analysis and extra Output Modules Record\n")
            f.write("#\n")
        f.write("LinearStatic  nsteps 1  nmodules 1\n")
        f.write("vtkxml tstep_all domain_all  primvars 1 1  vars 5 1 2 4 5 27  stype 2\n")

    def write_domain_record(self, f):
        """ domain *domainType
                *2dPlaneStress
                 two default dofs per node (u-displacement, v-displacement)
                 1, 2
                *2d-Truss
                 three default dofs per node (u-displacement, v-displacement, w-displacement)
                 1, 2, 3
                *3d
                 three default dofs per node (w-displacent, u-rotation, v-rotation)
                 1, 2, 3
                *2dMindlinPlate
                 six default dofs per node (displacement and rotation along each axis)
                 1, 2, 3, 4, 5, 6
                *3dShell
                 three default dofs per node (u-displacement, w-displacement, v-rotation)
                 1, 2, 5
                *2dBeam
                 three default dofs per node (u-velocity, v-velocity, and pressure)
                 7, 8, 11
        available dofs
            u-displacement=1
            v-displacement=2
            w-displacement=3
            u-rotation=4
            v-rotation=5
            w-rotation=6
            u-velocity=7
            v-velocity=8
            w-velocity=9
            temperature=10
            pressure=11
            special dofs for gradient-type constitutive models=12 and 13
            mass concentration=14
            special dofs for extended finite elements (XFEM)=15–30
        """
        if self.write_comments is True:
            f.write("#\n")
            f.write("#\n")
            f.write("# {}\n".format(67 * "*"))
            f.write("# Domain Record\n")
            f.write("#\n")
        if meshtools.is_zplane_2D_mesh(self.femmesh):
            self.domain = "2dPlaneStress"
        else:
            self.domain = "3d"
        f.write("domain " + self.domain + "\n")

    def write_output_manager_record(self, f):
        """ OutputManager
                [tstep all]
                [tstep step # (in) ]
                [tsteps out # (rl) ]
                [dofman all]
                [dofman output # (rl) ]
                [dofman except # (rl) ]
                [element all]
                [element output # (rl) ]
                [element except # (rl) ]
                ndofman # (in)
                nelem # (in)
                ncrosssect # (in)
                nmat # (in)
                nbc # (in)
                nic # (in)
                nltf # (in)
                [nbarrier # (in) ]
        """
        if self.write_comments is True:
            f.write("#\n")
            f.write("#\n")
            f.write("# {}\n".format(67 * "*"))
            f.write("# Output Manager Record\n")
            f.write("#\n")
        f.write("OutputManager tstep_all dofman_all element_all\n")

    def write_components_size_record(self, f):
        """ Components size record, describes the number of components in related domain
                ndofman #(in)
                nelem #(in)
                ncrosssect #(in)
                nmat #(in)
                nbc #(in)
                nic #(in)
                nltf #(in)
                [nbarrier #(in)]
                neset #[in]
        """
        if self.write_comments is True:
            f.write("#\n")
            f.write("#\n")
            f.write("# {}\n".format(67 * "*"))
            f.write("# Components Size Record\n")
            f.write("#\n")
        f.write("ndofman 8 nelem 5 ncrosssect 1 nmat 1 nbc 3 nic 0 nltf 1 nset 3\n")

    def write_dof_manager_record(self, f):
        """ *DofManagerType
             (num#) (in)
             [load # (ra) ]
             [DofIDMask # (ia) ]
             [bc # (ia) ]
             [ic # (ia) ]
             [doftype # (ia) masterMask # (ia) ]
             [shared]i | h[remote]i | h[null]
             [partitions # (ia) ]
        """
        if self.write_comments is True:
            f.write("#\n")
            f.write("#\n")
            f.write("# {}\n".format(67 * "*"))
            f.write("# DOF Manager Record\n")

    def write_node_and_element_records(self, f):
        """ Mesh writer, see OOFEM mesh file writer module """
        if self.write_comments is True:
            f.write("#\n")
            f.write("#\n")
            f.write("# {}\n".format(67 * "*"))
            f.write("# Node and Element Records\n")
            f.write("#\n")
        from feminout.importOofemMesh import write_oofem_mesh_to_file as write_mesh
        write_mesh(f, self.femmesh, self.femelement_table, None, self.write_comments)

    def write_cross_section_record(self, f):
        """ *CrossSectType (num#) (in)
                *SimpleCS [thick # (rn) ] [width # (rn) ] [area # (rn) ]
                 [iy # (rn) ] [iz # (rn) ] [ik # (rn) ]
                 [shearareay # (rn) ] [shearareaz # (rn) ] beamshearcoeff # (rn)

                *VariableCS [thick # (expr) ] [width # (expr) ] [area # (expr) ]
                 [iy # (expr) ] [iz # (expr) ] [ik # (expr) ]
                 [shearareay # (expr) ] [shearareaz # (expr) ]

                *LayeredCS nLayers # (in)
                 LayerMaterials # (ia)
                 Thicks # (ra) Widths # (ra)
                 midSurf # (rn)
        """
        if self.write_comments is True:
            f.write("#\n")
            f.write("#\n")
            f.write("# {}\n".format(67 * "*"))
            f.write("# Cross Section Record\n")
            f.write("#\n")
        f.write("SimpleCS 1 thick 1.0 width 1.0 material 1 set 1\n")

    def write_material_type_record(self, f):
        """ *MaterialType (num#) (in) d # (rn)
                 Linear isotropic elastic material
                *IsoLE num (in) # d (rn) # E (rn) # n (rn) # tAlpha (rn) #
                 Mooney-Rivlin
                *MooneyRivlin (in) # d (rn) # K (rn) # C1 (rn) # C2 (rn) #
                 Large-strain master material material
                *LSmasterMat (in) # m (rn) # slavemat (in) #
                 DP material
                *DruckerPrager
                    num (in) # d (rn) # tAlpha (rn) # E (rn) #
                    n (rn) # alpha (rn) # alphaPsi (rn) # ht (in) #
                    iys (rn) # lys (rn) # hm (rn) # kc (rn) #
                    [ yieldtol (rn) #]
                 Mises plasticity model with isotropic hardening
                *MisesMat
                    (in) # d (rn) # E (rn) # n (rn) # sig0 (rn) #
                    H (rn) # omega crit (rn) #a (rn) #
                 Rotating crack model for concrete
                *Concrete3
                    d (rn) # E (rn) # n (rn) # Gf (rn) #
                    Ft (rn) # exp soft (in) # tAlpha (rn) #
                 EC2CreepMat model for concrete creep and shrinkage
                *EC2CreepMat
                    n (rn) # [ begOfTimeOfInterest (rn) #] [ end-OfTimeOfInterest (rn) #]
                    relMatAge (rn) # [ timeFactor (rn) #] stiffnessFactor (rn) #
                    [ tAlpha (rn) #] fcm28 (rn) # t0 (rn) # cem- Type (in) # [ henv (rn) #]
                    h0 (rn) # shType (in) # [ spectrum ][ temperatureDependent ]
        """
        if self.write_comments is True:
            f.write("#\n")
            f.write("#\n")
            f.write("# {}\n".format(67 * "*"))
            f.write("# Material Type Record\n")
            f.write("#\n")
        f.write("IsoLE 1 d 0. E 15.0 n 0.25 talpha 1.0\n")

    def write_boundary_condition_record(self, f):
        if self.write_comments is True:
            f.write("#\n")
            f.write("#\n")
            f.write("# {}\n".format(67 * "*"))
            f.write("# Boundary Condition Record\n")
            f.write("#\n")
        f.write("BoundaryCondition 1 loadTimeFunction 1 dofs 2 1 2 values 1 0.0 set 2\n")
        f.write("BoundaryCondition 2 loadTimeFunction 1 dofs 1 2 values 1 0.0 set 3\n")

    def write_nodal_load_record(self, f):
        if self.write_comments is True:
            f.write("#\n")
            f.write("#\n")
            f.write("# {}\n".format(67 * "*"))
            f.write("# Nodal Load Record\n")
            f.write("#\n")
        f.write("NodalLoad 3 loadTimeFunction 1 dofs 2 1 2 components 2 2.5 0.0 set 3\n")

    def write_time_function_record(self, f):
        if self.write_comments is True:
            f.write("#\n")
            f.write("#\n")
            f.write("# {}\n".format(67 * "*"))
            f.write("# Time Function Record\n")
            f.write("#\n")
        f.write("ConstantFunction 1 f(t) 1.0\n")

    def write_set_record(self, f):
        """ Set (num#) (in)
            [elements # (ia) ] [elementranges # (rl) ] [allElements]
            [nodes # (ia) ] [noderanges # (rl) ] [allNodes]
            [elementboundaries # (ia) ] [elementedges # (ia) ]
        """
        if self.write_comments is True:
            f.write("#\n")
            f.write("#\n")
            f.write("# {}\n".format(67 * "*"))
            f.write("# Set Record\n")
            f.write("#\n")
        f.write("Set 1 elementranges {(1 5)}\n")
        f.write("Set 2 nodes 2 1 2\n")
        f.write("Set 3 nodes 2 7 8\n")

    def write_footer(self, f):
        if self.write_comments is True:
            f.write("#\n")
            f.write("#\n")
            f.write("# {}\n".format(67 * "*"))
            f.write("# End of Input File\n")
            f.write("#\n")


example_input_file = """2DPlaneStress.out
Patch test of PlaneStress2d elements -> pure compression
LinearStatic nsteps 1 nmodules 1
vtkxml tstep_all domain_all  primvars 1 1 vars 5 1 2 4 5 27 stype 2
domain 2dPlaneStress
OutputManager tstep_all dofman_all element_all
ndofman 8 nelem 5 ncrosssect 1 nmat 1 nbc 3 nic 0 nltf 1 nset 3
node 1 coords 3  0.0   0.0   0.0
node 2 coords 3  0.0   4.0   0.0
node 3 coords 3  2.0   2.0   0.0
node 4 coords 3  3.0   1.0   0.0
node 5 coords 3  8.0   0.8   0.0
node 6 coords 3  7.0   3.0   0.0
node 7 coords 3  9.0   0.0   0.0
node 8 coords 3  9.0   4.0   0.0
PlaneStress2d 1 nodes 4 1 4 3 2  NIP 1
PlaneStress2d 2 nodes 4 1 7 5 4  NIP 1
PlaneStress2d 3 nodes 4 4 5 6 3  NIP 1
PlaneStress2d 4 nodes 4 3 6 8 2  NIP 1
PlaneStress2d 5 nodes 4 5 7 8 6  NIP 1
Set 1 elementranges {(1 5)}
Set 2 nodes 2 1 2
Set 3 nodes 2 7 8
SimpleCS 1 thick 1.0 width 1.0 material 1 set 1
IsoLE 1 d 0. E 15.0 n 0.25 talpha 1.0
BoundaryCondition 1 loadTimeFunction 1 dofs 2 1 2 values 1 0.0 set 2
BoundaryCondition 2 loadTimeFunction 1 dofs 1 2 values 1 0.0 set 3
NodalLoad 3 loadTimeFunction 1 dofs 2 1 2 components 2 2.5 0.0 set 3
ConstantFunction 1 f(t) 1.0
"""

##  @}
