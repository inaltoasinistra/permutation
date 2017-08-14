#!/bin/sh
PYTHONPATH=.

SEEDS="tragedia,malinteso,attorno attorno,lacuna,invece,michele,produrre,vispo tragedia,malinteso,attorno,lacuna,invece,michele,produrre,vispo,brillante,buio,valgo,umano"

for seed in $SEEDS
do
    enc=$(./scripts/permutation --password-unsafe test:1 --seed-unsafe $seed --sep , encode)
    dec=$(./scripts/permutation --password-unsafe test:1 --permutation-unsafe "$enc" --language italian --sep , decode)
    
    echo $dec
    if [ $seed != $dec ]
    then
	echo Error $seed
	exit 1
    fi
done
