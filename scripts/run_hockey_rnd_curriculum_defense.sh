#!/bin/bash
#SBATCH --job-name=rnd_curric  # give it any name you want
#SBATCH --cpus-per-task=4   # max 24 per node
#SBATCH --partition=day     # choose out of day, week, month depending on job duration
#SBATCH --mem-per-cpu=3G    # max 251GB per node
#SBATCH --gres=gpu:1        # how many gpus to use each node has 4 gpus
#SBATCH --time=08:00:00     # job length: the job will run either until completion or until this timer runs out
#SBATCH --error=job.%J.err  # %J is the job ID, errors will be written to this file
#SBATCH --output=job.%J.out # the output will be written in this file
#SBATCH --mail-type=ALL     # write a mail if a job begins, ends, fails, gets requeued or stages out options: NONE, BE>
#SBATCH --mail-user=surabhi.s.nath@gmail.com   # your email

singularity run ../../container.sif python3 runner.py --env hockey --numepisodes 10000 --numseeds 1 --epsilon 1  --minepsilon 0.01 --epsilondecay 0.99 --savenum 174 --opponent weak --curriculum --numcurriculumepisodes 5000 --alpha 0.0002 --gamma 0.98 --alphadecay 1.0 --rnd --alpha_rnd 0.001
