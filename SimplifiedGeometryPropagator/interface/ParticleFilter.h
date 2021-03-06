#ifndef FASTSIM_PARTICLEFILTER
#define FASTSIM_PARTICLEFILTER

#include "DataFormats/Math/interface/LorentzVector.h"
#include <vector>

namespace edm
{
    class ParameterSet;
}

namespace fastsim
{
    class Particle;
    class ParticleFilter
    {
    public:
	ParticleFilter(const edm::ParameterSet & cfg);
	bool accepts(const Particle & particle) const;
	bool acceptsEn(const Particle & particle) const;
	bool acceptsVtx(const math::XYZTLorentzVector & originVertexPosition) const;

    private:
	// see constructor for comments
	double chargedPtMin2_, EMin_, protonEMin_;
	double cos2ThetaMax_;
	double vertexRMax2_,vertexZMax_;
	std::vector<int> skipParticles_;
    };
}

#endif
