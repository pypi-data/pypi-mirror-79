
from PDSim.flow import flow_models
cimport PDSim.flow.flow_models as flow_models

from PDSim.flow.flow_models import FlowFunction
from PDSim.flow.flow_models cimport FlowFunction

from PDSim.flow.flow import FlowPath
from PDSim.flow.flow cimport FlowPath

from PDSim.scroll import scroll_geo

from PDSim.scroll.common_scroll_geo import geoVals
from PDSim.scroll.common_scroll_geo cimport geoVals
    
cdef class _Scroll(object):
    cdef public geoVals geo
    cdef public double theta
    cdef public double HTC
    
    cpdef dict __cdict__(self)
    cpdef double SA_S(self, FlowPath FP)
    cpdef double Discharge(self,FlowPath FP)
    cpdef double Inlet_sa(self, FlowPath FP)
    cpdef double RadialLeakage(self, FlowPath FP, double t = *)
    cpdef double FlankLeakage(self, FlowPath FP, int Ncv_check = *)
