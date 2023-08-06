# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 11:29:09 2020

@author: LENOVO
"""

class MatData(object):
  def __init__(self,matid):
    self.matid = matid
  
  @property
  def formula(self):
    return self.formua
  
  @property
  def icsd_id(self):
    return self.icsd_id
  
  @property
  def conventional_cell(self):
    return self.conventional_cell
  
  @property
  def conventional_cell_site(self):
    return self.conventional_cell_site
  
  @property
  def primitive_cell(self):
    return self.primitive_cell
  
  @property
  def primitive_cell_site(self):
    return self.primitive_cell_site
  
  @property
  def crystal_system(self):
    return self.crystal_system
  
  @property
  def point_group(self):
    return self.point_group
  
  @property
  def space_group(self):
    return self.spacegroup
  
  @property
  def cif_data(self):
    return self.cif_data
  
  @property
  def magnetization(self):
    return self.magnetization
  
  @property
  def bandStructure(self):
    return self.bandStructure
  
  @property
  def densityOfStates(self):
    return self.densityOfStates
  
  @property
  def poscar_cc(self):
    return self.poscar_cc
  
  @property
  def poscar_pc(self):
    return self.poscar_pc
  
  @property
  def same_file(self):
    return self.same_file
  
  @property
  def poscar(self):
    return self.poscar
  
  @property
  def kpoints_relax(self):
    return self.kpoints_relax
  
  @property
  def kpoints_scf(self):
    return self.kpoints_scf
  
  @property
  def kpath(self):
    return self.kpath
  