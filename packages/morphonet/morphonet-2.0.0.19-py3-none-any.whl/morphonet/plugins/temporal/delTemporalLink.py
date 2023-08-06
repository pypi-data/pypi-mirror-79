# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin


#UnLinks all objects in time
class delTemporalLink(MorphoPlugin):
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_Name("Delete Links")
        self.set_Parent("Temporal Relation")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None
        for cid in objects:
             o=dataset.getObject(cid)
             if o is not None:
                dataset.del_link(o)
        self.restart()
        
