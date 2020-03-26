# Setup Notes for XCarve CNC
I made my own CNC Machine based on the X-Carve. Use these settings in the $$ menu.

## $$ Menu (at GRBL v0.9)
```
1=100 (step idle delay, msec)
$2=0 (step port invert mask:00000000)
$3=0 (dir port invert mask:00000000)
$4=0 (step enable invert, bool)
$5=0 (limit pins invert, bool)
$6=0 (probe pin invert, bool)
$10=3 (status report mask:00000011)
$11=0.010 (junction deviation, mm)
$12=0.002 (arc tolerance, mm)
$13=0 (report inches, bool)
$20=0 (soft limits, bool)
$21=0 (hard limits, bool)
$22=0 (homing cycle, bool)
$23=0 (homing dir invert mask:00000000)
$24=25.000 (homing feed, mm/min)
$25=500.000 (homing seek, mm/min)
$26=250 (homing debounce, msec)
$27=1.000 (homing pull-off, mm)
$100=40.000 (x, step/mm)
$101=46.800 (y, step/mm)
$102=755.790 (z, step/mm)
$110=8000.000 (x max rate, mm/min)
$111=8000.000 (y max rate, mm/min)
$112=500.000 (z max rate, mm/min)
$120=50.000 (x accel, mm/sec^2)
$121=50.000 (y accel, mm/sec^2)
$122=10.000 (z accel, mm/sec^2)
$130=200.000 (x max travel, mm)
$131=200.000 (y max travel, mm)
$132=200.000 (z max travel, mm)
```

## $$ Menu (at GRBL v1.1)
```
$1=100
$2=0
$3=0
$4=0
$5=0
$6=0
$10=0
$11=0.010
$12=0.002
$13=0
$20=0
$21=0
$22=0
$23=0
$24=25.000
$25=500.000
$26=250
$27=1.000
$30=1000
$31=0
$32=0
$100=40.000
$101=46.800
$102=755.790
$110=8000.000
$111=8000.000
$112=500.000
$120=50.000
$121=50.000
$122=10.000
$130=200.000
$131=200.000
$132=200.000
```