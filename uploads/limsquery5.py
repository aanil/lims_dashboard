
from genologics.entities import *
from genologics.lims import *
from genologics.config import BASEURI, USERNAME, PASSWORD
lims= Lims(BASEURI, USERNAME, PASSWORD)

p = Process(lims, id ='24-219360' )
for out in p.all_outputs():
    if "P6156_101" in out.name:
        out.udf["Min Size (bp)"]=25501
        out.put()
    elif "P6156_102" in out.name:
        out.udf["Min Size (bp)"]=18955
        out.put()
    elif "P6156_103" in out.name:
        out.udf["Min Size (bp)"]=28106
        out.put()
    elif "P6156_104" in out.name:
        out.udf["Min Size (bp)"]=15554
        out.put()

