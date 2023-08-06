#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cython: language_level=3
"""

"""


from mechanical_components.meshes import MeshAssembly, hardened_alloy_steel,\
        gear_graph_simple
        
import math

import copy

try:
    _open_source = True
    import mechanical_components.optimization.meshes_protected as protected_module
except (ModuleNotFoundError, ImportError) as _:
    _open_source = False

#class ContinuousMeshesAssemblyOptimizer(protected_module.ProtectedContinuousMeshesAssemblyOptimizer if _open_source==True else object):

        

class MeshAssemblyOptimizer(protected_module.MeshAssemblyOptimizer if _open_source==True else object):
    """
    Gear mesh assembly optimizer supervisor
    
    :param connections: List of tuples defining gear mesh connection [(node1,node2), (node2,node3)...]
    :param gear_speeds: Dictionary defining minimum and maximum speed for each gear mesh {node1: [speed_min,speed_max], node2: [speed_min,speed_max]...}
    :param center_distances: List of two elements define gear mesh connection [[mesh1_centerdistance_min, mesh1_centerdistance_max], [mesh2_centerdistance_min, mesh2_centerdistance_max] ...] with mesh1 the mesh between node1 and node2 ...
    :param transverse_pressure_angle: List of two elements define the transversal pressure angle interval for each mesh [[mesh1_transversepressure_min, mesh1_transversepressure_max], [mesh2_transversepressure_min, mesh2_transversepressure_max] ...]
    :param helix_angle: Dictionary to define for one mesh the minimum and maximum helix angle {node2: [mesh1_helixangle_min, mesh1_helixangle_max]}
    :param gear_width: Dictionary to define for each gear mesh the minimum and maximum gear width {node1: [node1_gearwidth_min,node1_gearwidth_max] ,node2: [node2_gearwidth_min,node2_gearwidth_max] ...}
    :param forbidden_frequencies: List of two elements defining unacceptable frequency interval [(freq1_min,freq1_max), (freq2_min,freq2_max)...]
    :param coefficient_profile_shift: Dictionary defining the minimum and maximum coefficient profile shift for each node {node1: [node1_coeffshift_min,node1_coeffshift_max],node2: [node2_coeffshift_min,node2_coeffshift_max] ...}
    :param rack_list: Dictionary define all admissible rack {rack1:mechanical_components.meshes.Rack, rack2:mechanical_components.meshes.Rack ...}
    :param rack_choice: Dictionary assign for each gear mesh a list of acceptable rack {node1:[rack1,rack2], node2:[rack1],node3:[rack4,rack5] ...}
    :param material: Dictionary defining material for each gear mesh {node1:mechanical_components.meshes.Material, node2:mechanical_components.meshes.Material ...}
    :param torques: Dictionary defining all input torque, one node where the torque is not specified is define as the 'output' {node1:torque1, node2:torque2, node3:'output'}
    :param cycles: Dictionary defining the number of cycles for one node {node3: number_cycles3}
    :param safety_factor: Safety factor used for the ISO design
    
    >>> list_cd=[[0.117,0.117],[0.12,0.13]]
    >>> list_gear_set=[(1,0),(0,2)]
    >>> list_speed={1:[1000*npy.pi/30.,1500*npy.pi/30.],0:[4100*npy.pi/30.,
                   4300*npy.pi/30.],2:[200*npy.pi/30.,400*npy.pi/30.]}
    >>> GA = meshes_opt.MeshAssemblyOptimizer(connections = list_gear_set,
                                gear_speed = list_speed,
                                center_distance = list_cd)
    """
    def __init__(self, connections, gear_speeds, center_distances, torques, cycles,
                 rigid_links=[], Z=None, transverse_pressure_angle={},  
                 helix_angle=None, gear_width=None, forbidden_frequencies=[],
                 coefficient_profile_shift=None, rack_list=None,
                 rack_choice=None, material=None,
                 safety_factor=1, verbose=False):

        self._drap_gear_graph=False
        self._drap_list_gear=False
        self._drap_connections_kinematic_dfs=False
        self._drap_sub_graph_dfs=False
        
        list_gear=[] # list of all gears
        for gs in connections:
            for (eng1,eng2) in gs:
                if eng1 not in list_gear:
                    list_gear.append(eng1)
                if eng2 not in list_gear:
                    list_gear.append(eng2)
        number_mesh=0
        for gs in connections:
            for (eng1,eng2) in gs:
                number_mesh+=1
                  
        # default parameters
        if len(transverse_pressure_angle.keys())<number_mesh:
            for num_mesh in list_gear:
                if num_mesh not in transverse_pressure_angle.keys():
                    transverse_pressure_angle[num_mesh]=[15/180.*math.pi,30/180.*math.pi]

        if helix_angle==None:
            helix_angle={list_gear[0]:[15/180.*math.pi,25/180.*math.pi]}
        
        if gear_width==None:
            gear_width={list_gear[0]:[15*1e-3,25*1e-3]}
        gw_min = math.inf
        gw_max = -math.inf
        for ne in gear_width.keys():
            if gear_width[ne][0]<gw_min:
                gw_min=gear_width[ne][0]
            if gear_width[ne][1]>gw_max:
                gw_max=gear_width[ne][1]
        for ne in list_gear:
            if ne not in gear_width.keys():
                gear_width[ne]=[gw_min,gw_max]
                
        if coefficient_profile_shift==None:
            coefficient_profile_shift={list_gear[0]:[-0.8,0.8]}
        for ne in list_gear:
            if ne not in coefficient_profile_shift.keys():
                coefficient_profile_shift[ne]=[-0.8,0.8]
                
        speed_min,speed_max=[math.inf,-math.inf]
        # definition min/max absolute speed
        for num_engr,(speed_interval_min,speed_interval_max) in gear_speeds.items():
            if speed_interval_min<speed_min:
                speed_min=speed_interval_min
            if speed_interval_max>speed_max:
                speed_max=speed_interval_max
            
        if rack_list==None:
#            rack_list={0:{'name':'Optim_Module','module':[1*1e-3,2.5*1e-3],
#                          'transverse_pressure_angle_rack':[20*npy.pi/180.,20*npy.pi/180.],
#                          'coeff_gear_addendum':[1,1],
#                          'coeff_gear_dedendum':[1.25,1.25],
#                          'coeff_root_radius':[0.38,0.38],
#                          'coeff_circular_tooth_thickness':[0.5,0.5]}}
            rack_list={0:{}}
        for num_rack, rack in rack_list.items():
            if 'module' not in rack.keys():
                rack_list[num_rack]['module'] = [1*1e-3,2.5*1e-3]
            if 'transverse_pressure_angle_rack' not in rack.keys():
                rack_list[num_rack]['transverse_pressure_angle_rack'] = [20*math.pi/180.,20*math.pi/180.]
            if 'coeff_gear_addendum' not in rack.keys():
                rack_list[num_rack]['coeff_gear_addendum'] = [1,1]
            if 'coeff_gear_dedendum' not in rack.keys():
                rack_list[num_rack]['coeff_gear_dedendum'] = [1.25,1.25]
            if 'coeff_root_radius' not in rack.keys():
                rack_list[num_rack]['coeff_root_radius'] = [0.38,0.38]
            if 'coeff_circular_tooth_thickness' not in rack.keys():
                rack_list[num_rack]['coeff_circular_tooth_thickness'] = [0.5,0.5]
            if 'name' not in rack.keys():
                rack_list[num_rack]['name'] = 'Optim_Module'
                        
            
        if rack_choice==None:
            rack_choice={list_gear[0]:[list(rack_list.keys())[0]]}
        for ne in list_gear:
            if ne not in rack_choice.keys():
                rack_choice[ne]=[list(rack_list.keys())[0]]
                
        if material==None:
            material={list_gear[0]:hardened_alloy_steel}
        for ne in list_gear:
            if ne not in material.keys():
                material[ne]=hardened_alloy_steel
        
#        if torques==None:
#            torques=[{list_gear[0]:100,list_gear[1]:'output'}]
#            
#        if cycle==None:
#            cycle={list_gear[0]:1e6}
        
        if Z==None:
            Z={}
            
        self.Z=Z
        self.connections = connections
        self.gear_speeds = gear_speeds
        self.forbidden_frequencies = forbidden_frequencies
        self.center_distances = center_distances
        self.transverse_pressure_angle = transverse_pressure_angle
        self.coefficient_profile_shift = coefficient_profile_shift
        self.rack_list = rack_list
        self.rack_choice = rack_choice
        self.material = material
        self.torques = torques
        self.cycles = cycles
        self.safety_factor = safety_factor
        self.rigid_links = rigid_links
        self.safety_factor = safety_factor
            
        self.nb_rack = len(self.rack_list.keys())
        self.check = True
        
        if self.Z == {}:
            var_Z = self.AnalyseZ()
            for num, li_z in var_Z.items():
                if li_z[0] > li_z[1]:
                    self.check = False
            self.Z=var_Z
            
#        print(self.Z)
            
        self.solutions=[]
        self.solutions_search=[]
        self.analyse=[]
