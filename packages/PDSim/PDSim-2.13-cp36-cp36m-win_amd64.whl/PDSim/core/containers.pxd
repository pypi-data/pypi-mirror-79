from CoolProp.State import State as StateClass
from CoolProp.State cimport State as StateClass

from CoolProp.constants_header cimport parameters

from libcpp cimport bool

from PDSim.flow.flow import FlowPathCollection
from PDSim.flow.flow cimport FlowPathCollection

from PDSim.misc.datatypes cimport arraym
from PDSim.misc.datatypes import arraym
    
cdef class TubeCollection(list):
    cdef dict _Nodes
    cdef arraym harray, parray, Tarray
    
    cpdef update_existence(self, int NCV)
    cpdef arraym get_h(self)
    cpdef arraym get_p(self)
    cpdef arraym get_T(self)
    cpdef dict get_Nodes(self)
    cpdef update(self)
    
cdef class Tube(object):
    cdef bytes m_key1,m_key2
    cdef public int fixed
    cdef public StateClass State1, State2
    cdef public object TubeFcn
    cdef public double Q_add,alpha,L,ID,OD,mdot,Q
    cdef public bool exists
    cdef public int i1,i2
    
cdef class ControlVolume(object):
    cdef public long keyIndex
    cdef bytes m_key, m_discharge_becomes
    cdef public object becomes
    cdef public object V_dV
    cdef public dict V_dV_kwargs
    cdef public object ForceFcn
    cdef public bint exists
    cdef public StateClass State

cdef class CVScore(object):
    cdef list array_list
    
    # Other variables
    cdef int state_vars, N
    cdef double omega
    
    # Storage arrays that are always required
    cdef public arraym T,p,h,rho,V,dV,cp,cv,m,v,dpdT_constV,Q
    
    # Property derivative arrays
    cdef public arraym summerdm, summerdT, drhodtheta, dTdtheta, dmdtheta, property_derivs
    
    cpdef update_size(self, int N)
    cdef build_all(self, int N)
    cdef free_all(self)
    cpdef copy(self)
    cpdef calculate_flows(self, FlowPathCollection Flows)
    cpdef just_volumes(self, list CVs, double theta)

cdef class CVArrays(CVScore):
    cpdef properties_and_volumes(self, list CVs, double theta, int state_vars, arraym x)
    cpdef calculate_derivs(self, double omega, bint has_liquid)

cdef class ControlVolumeCollection(object):
    cdef readonly list keys, CVs, indices, exists_keys, exists_indices, exists_CV
    cdef readonly dict Nodes
    cdef readonly int N, Nexist
    cdef public CVArrays arrays

    cpdef add(self, ControlVolume CV)
    cpdef rebuild_exists(self)
    cpdef updateStates(self, str name1, arraym array1, str name2, arraym array2)
    cpdef volumes(self, double theta, bint as_dict = *)
    cpdef at(self, int i)
    cpdef get(self, parameters key, double factor=*)
