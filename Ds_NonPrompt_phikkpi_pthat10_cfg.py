import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

_generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(5360.0),
                         maxEventsToPrint = cms.untracked.int32(0),
                         ExternalDecays = cms.PSet(
                             EvtGen130 = cms.untracked.PSet(
                                 decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
                                 particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
                                 list_forced_decays = cms.vstring('MyD_s+','MyD_s-'),
                                 operates_on_particles = cms.vint32(),
                                 convertPythiaCodes = cms.untracked.bool(False),
                                 user_decay_embedded= cms.vstring(
                                     """
                                     Alias        MyD_s+                 D_s+
                                     Alias        MyD_s-                 D_s-
                                     ChargeConj   MyD_s-                 MyD_s+
                                     Alias        Myphi                  phi
                                     Decay MyD_s+
                                     1.000           Myphi     pi+     SVS;
                                     Enddecay
                                     CDecay MyD_s-
                                     Decay Myphi
                                     1.000           K+        K-      VSS;
                                     Enddecay
                                     End  
                                     """
                                 )
                                 
                                 
                             ),
                             parameterSets = cms.vstring('EvtGen130')
                         ),
                         PythiaParameters = cms.PSet(
                             pythia8CommonSettingsBlock,
                             pythia8CP5SettingsBlock,
                             processParameters = cms.vstring(
                                 'HardQCD:all = on',
                                 'PhaseSpace:pTHatMin = 10', #min pthat
                             ),
                             parameterSets = cms.vstring(
                                 'pythia8CommonSettings',
                                 'pythia8CP5Settings',
                                 'processParameters',
                             )
                         )
                     )

from GeneratorInterface.Core.ExternalGeneratorFilter import ExternalGeneratorFilter
generator = ExternalGeneratorFilter(_generator)
generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

partonfilter = cms.EDFilter("PythiaFilter",
                            ParticleID = cms.untracked.int32(5) # 4 for prompt and 5 for non-prompt particles
                        )

DsDaufilter = cms.EDFilter("PythiaMomDauFilter",
                           ParticleID = cms.untracked.int32(431), #Ds+
                           MomMinPt = cms.untracked.double(20.0),
                           MomMinEta = cms.untracked.double(-2.4),
                           MomMaxEta = cms.untracked.double(2.4),
                           DaughterIDs = cms.untracked.vint32(333, 211), #phi,pi+
                           NumberDaughters = cms.untracked.int32(2),
                           DaughterID = cms.untracked.int32(333),
                           DescendantsIDs = cms.untracked.vint32(321 , -321), #k+,k-
                           NumberDescendants = cms.untracked.int32(2),
                       )
Dsrapidityfilter = cms.EDFilter("PythiaFilter",
                                ParticleID = cms.untracked.int32(431),
                                MinPt = cms.untracked.double(20.0),
                                MaxPt = cms.untracked.double(500.),
                                MinRapidity = cms.untracked.double(-2.4),
                                MaxRapidity = cms.untracked.double(2.4),
                            )

ProductionFilterSequence = cms.Sequence(generator*partonfilter*DsDaufilter*Dsrapidityfilter)
