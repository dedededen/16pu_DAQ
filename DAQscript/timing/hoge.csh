#!/bin/csh

setenv TCMRCMD "/jk/dev/operation_app/jkControl/Timing/script/MR/timing_TCMR_MR_cmd.csh"


$TCMRCMD - <<EOF
#EOF
set tcmr3_mon_d1 6 A $1
set tcmr3_mon_d1 7 BCD $2
EOF
e

