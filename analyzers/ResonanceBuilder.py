'''Builds L{resonances<heppy.particles.tlv.resonance>}.'''

from heppy.framework.analyzer import Analyzer
from heppy.particles.tlv.resonance import Resonance2 as Resonance

import pprint 
import itertools

mass = {23: 91, 24: 80.4, 25: 125}

class ResonanceBuilder(Analyzer):
    '''Builds L{resonances<heppy.particles.tlv.resonance>}.

    Example:: 

        from heppy.analyzers.ResonanceBuilder import ResonanceBuilder
        zeds = cfg.Analyzer(
          ResonanceBuilder,
          output = 'zeds',
          leg_collection = 'sel_iso_leptons',
          pdgid = 23
        )

    @param output: L{Resonances<heppy.particles.tlv.resonance>} are stored in this collection, 
      sorted according to their distance to the nominal mass corresponding 
      to the specified pdgid. The first resonance in this collection is thus the best one. 
    
      Additionally, a collection zeds_legs (in this case) is created to contain the 
      legs of the best resonance. 

    @param leg_collection: Collection of particles that will be combined into resonances.

    @param pdgid: Pythia code for the target resonance. 
    '''
    
    def process(self, event):
        '''Process the event
        
        The event must contain:
         - self.cfg_ana.leg_collection: the input collection of particles
         
        This method creates:
         - event.<self.cfg_ana.output>: collection of resonances
         - event.<self.cfg_ana.output>_legs: the two legs of the best resonance.
        '''
        legs = getattr(event, self.cfg_ana.leg_collection)
        resonances = []
        for leg1, leg2 in itertools.combinations(legs,2):
            resonances.append( Resonance(leg1, leg2, self.cfg_ana.pdgid) )
        # sorting according to distance to nominal mass
        nominal_mass = mass[self.cfg_ana.pdgid]
        resonances.sort(key=lambda x: abs(x.m()-nominal_mass))
        setattr(event, self.cfg_ana.output, resonances)
