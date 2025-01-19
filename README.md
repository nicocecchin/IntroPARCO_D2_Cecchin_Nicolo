# IntroPARCO D2


## Description
This repo is the collection of codes related to the project "Parallel Matrix Transposition using MPI". The following are the instruction to replicate the results presented in the report.

Disclaimer: I used **WSL** (Windows subsystem for Linux) on my local machine to run all the codes (i. e. python codes for the graphs), so this tutorial uses Linux commands.
To run the Python files you need to have Python installed. (version 3.8.10, modules: pandas, matplotlib.pyplot).


## Environment setup
The first thing you have to do is clone this repo on your computer. Inside the repo there are three folders and this **README.md**:
- **codes_and_jobs**: is the folder where the three C++ implementations are, together with the PBS files to run the jobs in the cluster.
- **graphs_data**: is the folder where you will put the CSV results files once the jobs will be complete. There are also the python files that generate the graphs.
- **graphs_data_report**: is the folder with the data showed in the report, as well as the photos of the graphs of the report.

To perfectly replicate this project, you need to have access to the HPC cluster of the University of Trento, and login in it, either being connected to the university wifi or using the VPN.
Use this command on another terminal to access the university cluster:
```
ssh your.username@hpc.unitn.it
```
After you put your Unitn password, you should log in.

Discleimer: you can run all the codes also on your local machine, using the commands and compiler version specified in the report.


## Load into HPC cluster
You should now open your local terminal and navigate it up to the repository folder. Now to load every C++ code and the PBS job submissions you have to use the command
```
scp ./codes_and_jobs/* your.username@hpc.unitn.it:/home/your.usename/
```
in the terminal. You will be asked to put your unitn password. Then the copy to the cluster will be completed.


## Jobs submission
Move now to the cluster terminal, where now you can start to submit the jobs.
To avoid conversion problem, you should add a *dos2unix* command before running the jobs.

### Sequential implementation
This job will compile the C++ code *seq.cpp*
- We submit the job described in *job_submission_seq.pbs*, that will provide us a CSV file with the times of the functions *checkSym* and *matTranspose*. This job will run in the **short_cpuQ**. to run the job use this code in the cluster terminal:
    ```
    dos2unix job_submission_seq.pbs
    qsub job_submission_seq.pbs
    ```

### OpenMP implementation
This job will compile the C++ code *omp.cpp*
- We submit the job described in *job_submission_omp.pbs*, that will provide us a pbs file with the times of the functions *checkSym* and *matTranspose*, using 1, 2, 4, 8, 16 and 32 threads. This job will run in the **short_cpuQ**. to run the job use this code in the cluster terminal:
    ```
    dos2unix job_submission_omp.pbs
    qsub job_submission_omp.pbs
    ```

### MPI implementation
This job will compile the C++ code *mpi.cpp*
- We submit the job described in *job_submission_mpi.pbs*, that will provide us a pbs file with the times of the functions *checkSym* and *matTranspose*, using 1, 2, 4, 8, 16 and 32 processes. This job will run in the **short_cpuQ**. to run the job use this code in the cluster terminal:
    ```
    dos2unix job_submission_mpi.pbs
    qsub job_submission_mpi.pbs
    ```

You can check at any time the status of your jobs using the command
```
qstat -u your.username
```


## Data collection and graphs
Once you are sure that **every** job has finished in the cluster, use this command on your local terminal (that by now should be pointing inside the directory *IntroPARCO_D2_Cecchin_Nicolò*, if not, be sure to get there before continuing) to download every CSV output file.
```
scp your.username@hpc.unitn.it:/home/your.username/*.csv ./graphs_data/
```

### Graphs 
The following instructions are for the graphs included in the report, and for other graphs mentioned on the report.
Once again, be sure to have all the CSV file inside the directory. Then, use this command to enter the graphs directory:
```
cd graphs_data
```
Then use this commands to get the graphs:
- **Sequential times**
    ```
    python3 sequential.py
    ```
- **MPI times**
    ```
    python3 mpi.py
    ```
- **OpenMP times**
    ```
    python3 omp.py
    ```
- **Strong scaling and efficiency of MPI**
    ```
    python3 strong_scaling_mpi.py
    ```
- **Strong scaling and efficiency of OMP**
    ```
    python3 strong_scaling_omp.py
    ```
- **Weak scaling**
    ```
    python3 weak_scaling.py
    ```
- **Times showed on the report**
    ```
    python3 report_times.py
    ```
- **Strong scaling and efficiency showed on the report**
    ```
    python3 report_strong_scaling_efficiency.py
    ```

## Conclusion
That was all for what concerned the data collection and processing.