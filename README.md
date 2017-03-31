# How to install

```
cmsrel CMSSW_9_1_0_pre1
cd CMSSW_9_1_0_pre1/src
cmsenv
git clone git@github.com:angirar/FastSimPhase1PixelUpgrade.git FastSimulation
scram b -rj32
```

# How to run

```
# create a file with generated events
source FastSimulation/SimplifiedGeometryPropagator/test/gen.sh
# pass the generated events to simulation
cmsRun FastSimulation/SimplifiedGeometryPropagator/python/conf_cfg.py
# to run validation do instead
cmsRun FastSimulation/SimplifiedGeometryPropagator/python/conf_validation_cfg.py
```
