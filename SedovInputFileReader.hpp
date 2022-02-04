#include <cstddef>
#include <iostream>
#include <cmath>
#include "ParticlesData.hpp"
#include "IFileReader.hpp"

namespace sphexa
{

template <typename Dataset>
struct SedovInputFileReader : IFileReader<Dataset>
{
    using T = double;
    using I = uint64_t;
    Dataset readParticleDataFromBinFile(const std::string &path, const size_t noParticles) const override
    {
        Dataset pd;
        const size_t noParticles3d = noParticles * noParticles * noParticles;
        pd.n = noParticles3d;
        pd.resize(noParticles3d);
        pd.count = pd.x.size();

        try
        {
            printf("Loading input file with %lu particles for Sedov at path '%s'... ", pd.n, path.c_str());
            fileutils::readParticleDataFromBinFile(path, pd.x, pd.y, pd.z, pd.vx, pd.vy, pd.vz, pd.ro, pd.u, pd.p, pd.h, pd.m);
            printf("OK\n");

            init(pd);
        }
        catch (FileNotOpenedException &ex)
        {
            printf("ERROR: %s. Terminating\n", ex.what());
            exit(EXIT_FAILURE);
        }

        return pd;
    }

    Dataset readParticleDataFromCheckpointBinFile(const std::string &path) const override
    {
        Dataset pd;
        std::ifstream inputfile(path, std::ios::binary);

        if (inputfile.is_open())
        {
            inputfile.read(reinterpret_cast<char *>(&pd.n), sizeof(size_t));

            pd.resize(pd.n);

            pd.n = pd.x.size();
            pd.count = pd.x.size();

            printf("Loading checkpoint file with %lu particles for Sedov... ", pd.n);

            inputfile.read(reinterpret_cast<char *>(&pd.ttot), sizeof(pd.ttot));
            inputfile.read(reinterpret_cast<char *>(&pd.minDt), sizeof(pd.minDt));

            fileutils::details::readParticleDataFromBinFile(inputfile, pd.x, pd.y, pd.z, pd.vx, pd.vy, pd.vz, pd.ro, pd.u, pd.p, pd.h, pd.m,
                                                            pd.temp, pd.mue, pd.mui, pd.du, pd.du_m1, pd.dt, pd.dt_m1, pd.x_m1, pd.y_m1,
                                                            pd.z_m1);
            inputfile.close();

            std::fill(pd.grad_P_x.begin(), pd.grad_P_x.end(), 0.0);
            std::fill(pd.grad_P_y.begin(), pd.grad_P_y.end(), 0.0);
            std::fill(pd.grad_P_z.begin(), pd.grad_P_z.end(), 0.0);

            pd.etot = pd.ecin = pd.eint = pd.egrav = 0.0;

            printf("OK\n");
        }
        else
            printf("ERROR: Can't open file %s\n", path.c_str());
        return pd;
    }

public:
    static inline const T gamma         = 5./3.;
    static inline const T omega         = 0.;
    static inline const T r0            = 0.;
    static inline const T r1            = 0.5;
    static inline const T mTotal        = 1.;
    static inline const T energyTotal   = 1.;
    static inline const T width         = 0.1;
    static inline const T ener0         = energyTotal / std::pow(M_PI,1.5) / 1. / std::pow(width,3.0);
    static inline const T rho0          = 1.;
    static inline const T u0            = 1.e-08;
    static inline const T p0            = 0.;
    static inline const T vr0           = 0.;
    static inline const T cs0           = 0.;
    static inline const T firstTimeStep = 1.e-6;

protected:
    void init(Dataset &pd) const
    {
        const T step  = (2. * r1) / pd.side;    //
        const T mPart = mTotal / pd.n;          //
        const T gamm1 = gamma - 1.;             //

        for (size_t i = 0; i < pd.count; i++)
        {
            pd.x[i] = pd.x[i] - 0.5;
            pd.y[i] = pd.y[i] - 0.5;
            pd.z[i] = pd.z[i] - 0.5;
            //pd.h[i] = pd.h[i] / 10.;
            const T radius = std::sqrt(std::pow(pd.x[i],2) + std::pow(pd.y[i],2) + std::pow(pd.z[i],2));

            pd.m[i]        = mPart;
            pd.ro[i]       = rho0;
            pd.u[i]        = ener0 * exp(-(std::pow(radius,2) / std::pow(width,2))) + u0;
            pd.p[i]        = pd.u[i] * rho0 * gamm1;

            pd.mui[i]      = 10.;

            pd.du[i]       = 0.;
            pd.du_m1[i]    = 0.;

            pd.dt[i]       = firstTimeStep;
            pd.dt_m1[i]    = firstTimeStep;
            pd.minDt       = firstTimeStep;

            pd.grad_P_x[i] = 0.;
            pd.grad_P_y[i] = 0.;
            pd.grad_P_z[i] = 0.;

            pd.x_m1[i]     = pd.x[i] - pd.vx[i] * firstTimeStep;
            pd.y_m1[i]     = pd.y[i] - pd.vy[i] * firstTimeStep;
            pd.z_m1[i]     = pd.z[i] - pd.vz[i] * firstTimeStep;
        }

        pd.etot = 0.;
        pd.ecin = 0.;
        pd.eint = 0.;
        pd.ttot = 0.;
    }
};

#ifdef USE_MPI
template <typename Dataset>
struct SedovMPIInputFileReader : SedovInputFileReader<Dataset>
{
    Dataset readParticleDataFromBinFile(const std::string &path, const size_t noParticles) const override
    {
        Dataset d;
        const size_t noParticles3D = noParticles * noParticles * noParticles;
        d.n = noParticles3D;
        initMPIData(d);

        try
        {
            fileutils::readParticleDataFromBinFileWithMPI(path, d, d.x, d.y, d.z, d.vx, d.vy, d.vz, d.ro, d.u, d.p, d.h, d.m);
            if (d.rank == 0) printf("Loaded input file with %lu particles for Sedov from path '%s' \n", d.n, path.c_str());
        }
        catch (MPIFileNotOpenedException &ex)
        {
            if (d.rank == 0) fprintf(stderr, "ERROR: %s. Terminating\n", ex.what());
            MPI_Abort(d.comm, ex.mpierr);
        }

        this->init(d);

        return d;
    }

    Dataset readParticleDataFromCheckpointBinFile(const std::string &path) const override
    {
        Dataset d;
        initMPIData(d);

        try
        {
            fileutils::readParticleCheckpointDataFromBinFileWithMPI(path, d, d.x, d.y, d.z, d.vx, d.vy, d.vz, d.ro, d.u, d.p, d.h, d.m,
                                                                    d.temp, d.mue, d.mui, d.du, d.du_m1, d.dt, d.dt_m1, d.x_m1, d.y_m1,
                                                                    d.z_m1);
            if (d.rank == 0) printf("Loaded checkpoint file with %lu particles for Sedov from path '%s'\n", d.n, path.c_str());
        }
        catch (MPIFileNotOpenedException &ex)
        {
            if (d.rank == 0) fprintf(stderr, "ERROR: %s. Terminating\n", ex.what());
            MPI_Abort(d.comm, ex.mpierr);
        }

        std::fill(d.grad_P_x.begin(), d.grad_P_x.end(), 0.0);
        std::fill(d.grad_P_y.begin(), d.grad_P_y.end(), 0.0);
        std::fill(d.grad_P_z.begin(), d.grad_P_z.end(), 0.0);

        d.etot = d.ecin = d.eint = d.egrav = 0.0;

        return d;
    }

private:
    void initMPIData(Dataset &d) const
    {
        d.comm = MPI_COMM_WORLD;
        MPI_Comm_size(d.comm, &d.nrank);
        MPI_Comm_rank(d.comm, &d.rank);
        MPI_Get_processor_name(d.pname, &d.pnamelen);
    }
};
#endif
} // namespace sphexa
