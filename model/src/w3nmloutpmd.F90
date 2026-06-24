#include "w3macros.h"
!/ ------------------------------------------------------------------- /
MODULE W3NMLOUTPMD
  !/
  !/                  +-----------------------------------+
  !/                  | WAVEWATCH III           NOAA/NCEP |
  !/                  |           E. Rainville            |
  !/                  |                                   |
  !/                  |                        FORTRAN 90 |
  !/                  | Last update :         24-Jun-2026 |
  !/                  +-----------------------------------+
  !/
  !/    For updates see subroutines.
  !/
  !  1. Purpose :
  !
  !     Manages namelists from configuration file ww3_outp.nml for ww3_outp program
  !
  !/ ------------------------------------------------------------------- /

  ! module defaults
  IMPLICIT NONE

  PUBLIC
