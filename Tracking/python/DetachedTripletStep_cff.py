import FWCore.ParameterSet.Config as cms
#from RecoPixelVertexing.PixelTriplets.caHitTripletEDProducer_cfi import caHitTripletEDProducer as _caHitTripletEDProducer
# import the full tracking equivalent of this file
import RecoTracker.IterativeTracking.DetachedTripletStep_cff as _standard
from FastSimulation.Tracking.SeedingMigration import _hitSetProducerToFactoryPSet

# fast tracking mask producer
import FastSimulation.Tracking.FastTrackerRecHitMaskProducer_cfi
detachedTripletStepMasks = FastSimulation.Tracking.FastTrackerRecHitMaskProducer_cfi.maskProducerFromClusterRemover(_standard.detachedTripletStepClusters)

# tracking regions
detachedTripletStepTrackingRegions = _standard.detachedTripletStepTrackingRegions.clone()

# trajectory seeds
import FastSimulation.Tracking.TrajectorySeedProducer_cfi
detachedTripletStepSeeds = FastSimulation.Tracking.TrajectorySeedProducer_cfi.trajectorySeedProducer.clone(
    layerList = _standard.detachedTripletStepSeedLayers.layerList.value(),
    trackingRegions = "detachedTripletStepTrackingRegions",
    hitMasks = cms.InputTag("detachedTripletStepMasks")
)
detachedTripletStepSeeds.seedFinderSelector.pixelTripletGeneratorFactory = _hitSetProducerToFactoryPSet(_standard.detachedTripletStepHitTriplets)

#_caHitTripletEDProducer.clone(
 #       doublets = "detachedTripletStepHitDoublets",
  #      extraHitRPhitolerance = detachedTripletStepHitTriplets.extraHitRPhitolerance,
   #     maxChi2 = dict(
    #       pt1    = 0.8, pt2    = 2,
     #      value1 = 300 , value2 = 10,
      #     ),
       # useBendingCorrection = True,
        #CAThetaCut = 0.001,
        #CAPhiCut = 0,
        #CAHardPtCut = 0.2,
#)) 

# track candidates
import FastSimulation.Tracking.TrackCandidateProducer_cfi
detachedTripletStepTrackCandidates = FastSimulation.Tracking.TrackCandidateProducer_cfi.trackCandidateProducer.clone(
    src = cms.InputTag("detachedTripletStepSeeds"),
    MinNumberOfCrossedLayers = 3,
    hitMasks = cms.InputTag("detachedTripletStepMasks")
    )

# tracks 
detachedTripletStepTracks = _standard.detachedTripletStepTracks.clone(TTRHBuilder = 'WithoutRefit')

detachedTripletStepClassifier1 = _standard.detachedTripletStepClassifier1.clone()
detachedTripletStepClassifier1.vertices = "firstStepPrimaryVerticesBeforeMixing"
detachedTripletStepClassifier2 = _standard.detachedTripletStepClassifier2.clone()
detachedTripletStepClassifier2.vertices = "firstStepPrimaryVerticesBeforeMixing"

detachedTripletStep = _standard.detachedTripletStep.clone()

# Final sequence 
DetachedTripletStep = cms.Sequence(detachedTripletStepMasks
                                   +detachedTripletStepTrackingRegions
                                   +detachedTripletStepSeeds
                                   +detachedTripletStepTrackCandidates
                                   +detachedTripletStepTracks
                                   +detachedTripletStepClassifier1*detachedTripletStepClassifier2
                                   +detachedTripletStep
                                   )
