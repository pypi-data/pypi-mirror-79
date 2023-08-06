
/****************************************************************/
/*                                                              */
/*  Copyright (C) 2018, M. Andelkovic, L. Covaci, A. Ferreira,  */
/*                    S. M. Joao, J. V. Lopes, T. G. Rappoport  */
/*                                                              */
/****************************************************************/

#include <Eigen/Dense>
#include <string>
#include <vector>
#include <iostream>
#include "H5Cpp.h"
#include "parse_input.hpp"
#include "systemInfo.hpp"
#include "functions.hpp"
#include "cond_2order/conductivity_2order.hpp"
#include <omp.h>

template <typename U, unsigned DIM>
Eigen::Matrix<std::complex<U>, -1, -1> conductivity_nonlinear<U, DIM>::Gamma2shgcontractAandR(){
  int NumMoments1 = NumMoments; U beta1 = beta; U e_fermi1 = e_fermi;
  std::function<U(int, U)> deltaF = [beta1, e_fermi1, NumMoments1](int n, U energy)->U{
    return delta(n, energy)*U(1.0/(1.0 + U(n==0)))*fermi_function(energy, e_fermi1, beta1)*kernel_jackson<U>(n, NumMoments1);
  };

  // Delta matrix of chebyshev moments and energies
  Eigen::Matrix<std::complex<U>,-1, -1, Eigen::RowMajor> DeltaMatrix;
  DeltaMatrix = Eigen::Matrix<std::complex<U>, -1, -1, Eigen::RowMajor>::Zero(N_energies, NumMoments);
  for(int n = 0; n < NumMoments; n++)
    for(int e = 0; e < N_energies; e++)
      DeltaMatrix(e,n) = deltaF(n, energies(e)); 

  Eigen::Matrix<std::complex<U>, -1,-1> cond; 
  
  cond = Eigen::Matrix<std::complex<U>, -1, -1>::Zero(N_energies, N_omegas);
  int N_threads;
  int thread_num;
  int local_NumMoments;
  omp_set_num_threads(systemInfo.NumThreads);
#pragma omp parallel shared(N_threads, cond) firstprivate(thread_num, DeltaMatrix)
{
#pragma omp master
{
  N_threads = omp_get_num_threads();
  // check if each thread will get the same number of moments
  if(NumMoments%N_threads != 0){
    std::cout << "The number of Chebyshev moments in the nonlinear conductivity must"
      "be a multiple of the number of threads\n" << std::flush;
    exit(1);
  }
}
#pragma omp barrier


#pragma omp for schedule(static, 1) nowait
  for(int i = 0; i < N_threads; i++){
    local_NumMoments = NumMoments/N_threads;
    thread_num = omp_get_thread_num();

    // The Gamma matrix has been divided among the threads
    // Each thread has one section of that matrix, called local_Gamma
    Eigen::Matrix<std::complex<U>, -1, -1> local_Gamma;
    local_Gamma = Gamma2.matrix().block(0, local_NumMoments*thread_num, 
        NumMoments, local_NumMoments);
    
    // Result of contracting the indices with the delta function
    Eigen::Matrix<std::complex<U>, -1, -1, Eigen::RowMajor> GammaEM;
    GammaEM = DeltaMatrix*local_Gamma;

    Eigen::Matrix<std::complex<U>, -1, -1> local_cond; 
    local_cond = Eigen::Matrix<std::complex<U>, -1, -1>::Zero(N_energies, N_omegas);
    
    // Loop over the frequencies
    //U w1, w2;
    U w1, w2;
    std::complex<U> GammaEp, GammaEn, GammaE;
    for(int w = 0; w < N_omegas; w++){
      w1 = frequencies2(w,0);
      w2 = frequencies2(w,1);

      for(int e = 0; e < N_energies; e++){
        GammaEp = 0;
        GammaEn = 0;
        for(int m = 0; m < local_NumMoments; m++){
          GammaEp += GammaEM(e, m)*greenAscat<U>(scat)(local_NumMoments*thread_num + m, energies(e) + w2);      // contracting with the positive frequencies
          GammaEn += GammaEM(e, m)*greenAscat<U>(scat)(local_NumMoments*thread_num + m, energies(e) - w2);      // contracting with the negative frequencies

        }
        GammaE = GammaEn - std::conj(GammaEp);     // This is equivalent to the two frequency-dependent terms in the formula
        local_cond(e,w) = GammaE;
      }    
    }

    
#pragma omp critical
    {
      cond += local_cond;
    }
  }
#pragma omp barrier
}

  return cond;
}

template Eigen::Matrix<std::complex<float>, -1, -1> conductivity_nonlinear<float, 1u>::Gamma2shgcontractAandR();
template Eigen::Matrix<std::complex<float>, -1, -1> conductivity_nonlinear<float, 2u>::Gamma2shgcontractAandR();
template Eigen::Matrix<std::complex<float>, -1, -1> conductivity_nonlinear<float, 3u>::Gamma2shgcontractAandR();

template Eigen::Matrix<std::complex<double>, -1, -1> conductivity_nonlinear<double, 1u>::Gamma2shgcontractAandR();
template Eigen::Matrix<std::complex<double>, -1, -1> conductivity_nonlinear<double, 2u>::Gamma2shgcontractAandR();
template Eigen::Matrix<std::complex<double>, -1, -1> conductivity_nonlinear<double, 3u>::Gamma2shgcontractAandR();

template Eigen::Matrix<std::complex<long double>, -1, -1> conductivity_nonlinear<long double, 1u>::Gamma2shgcontractAandR();
template Eigen::Matrix<std::complex<long double>, -1, -1> conductivity_nonlinear<long double, 2u>::Gamma2shgcontractAandR();
template Eigen::Matrix<std::complex<long double>, -1, -1> conductivity_nonlinear<long double, 3u>::Gamma2shgcontractAandR();
