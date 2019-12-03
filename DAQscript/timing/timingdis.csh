#!/bin/csh

setenv TCMRCMD "/jk/dev/operation_app/jkControl/Timing/script/MR/timing_TCMR_MR_cmd.csh"
$TCMRCMD - <<EOF
#EOF
delay tcmr3_mon_d1 6 
delay tcmr3_mon_d1 7 
EOF


