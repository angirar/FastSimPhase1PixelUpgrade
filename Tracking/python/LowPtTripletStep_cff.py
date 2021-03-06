import FWCore.ParameterSet.Config as cms
from RecoPixelVertexing.PixelTriplets.caHitTripletEDProducer_cfi import caHitTripletEDProducer as _caHitTripletEDProducer
from Configuration.Eras.Modifier_trackingPhase1_cff import trackingPhase1

# import the full tracking equivalent of this file
import RecoTracker.IterativeTracking.LowPtTripletStep_cff as _standard
from FastSimulation.Tracking.SeedingMigration import _hitSetProducerToFactoryPSet

# fast tracking mask producer
import FastSimulation.Tracking.FastTrackerRecHitMaskProducer_cfi
lowPtTripletStepMasks = FastSimulation.Tracking.FastTrackerRecHitMaskProducer_cfi.maskProducerFromClusterRemover(_standard.lowPtTripletStepClusters)

# tracking regions
lowPtTripletStepTrackingRegions = _standard.lowPtTripletStepTrackingRegions.clone()

# trajectory seeds
import FastSimulation.Tracking.TrajectorySeedProducer_cfi
lowPtTripletStepSeeds = FastSimulation.Tracking.TrajectorySeedProducer_cfi.trajectorySeedProducer.clone(
    layerList = _standard.lowPtTripletStepSeedLayers.layerList.value(),
    trackingRegions = "lowPtTripletStepTrackingRegions",
    hitMasks = cms.InputTag("lowPtTripletStepMasks"),
)
lowPtTripletStepSeeds.seedFinderSelector.pixelTripletGeneratorFactory = _hitSetProducerToFactoryPSet(_standard.lowPtTripletStepHitTriplets)

trackingPhase1.toReplaceWith(lowPtTripletStepHitTriplets,_caHitTripletEDProducer.clone(
        doublets = "lowPtTripletStepHitDoublets",
        extraHitRPhitolerance = lowPtTripletStepHitTriplets.extraHitRPhitolerance,
        SeedComparitorPSet = lowPtTripletStepHitTriplets.SeedComparitorPSet,
        maxChi2 = dict(
            pt1    = 0.8, pt2    = 2,
            value1 = 70 , value2 = 8,
            ),
        useBendingCorrection = True,
        CAThetaCut = 0.002,
        CAPhiCut = 0.05,
))

lowPtTripletStepSeeds.seedFinderSelector.pixelTripletGeneratorFactory.SeedComparitorPSet.ComponentName = "none"

# track candidates
import FastSimulation.Tracking.TrackCandidateProducer_cfi
lowPtTripletStepTrackCandidates = FastSimulation.Tracking.TrackCandidateProducer_cfi.trackCandidateProducer.clone(
    src = cms.InputTag("lowPtTripletStepSeeds"),
    MinNumberOfCrossedLayers = 3,
    hitMasks = cms.InputTag("lowPtTripletStepMasks"),
)

# tracks
lowPtTripletStepTracks = _standard.lowPtTripletStepTracks.clone(TTRHBuilder = 'WithoutRefit')

# final selection
lowPtTripletStep = _standard.lowPtTripletStep.clone()
lowPtTripletStep.vertices = "firstStepPrimaryVerticesBeforeMixing"

# Final swquence 
LowPtTripletStep = cms.Sequence(lowPtTripletStepMasks
                                +lowPtTripletStepTrackingRegions
                                +lowPtTripletStepSeeds
                                +lowPtTripletStepTrackCandidates
                                +lowPtTripletStepTracks  
                                +lowPtTripletStep   
                                )
