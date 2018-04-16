## Instructions to run the code

The files you will need:
* requirements.txt - Python dependencies and packages that need to be installed.
* run_job.sh - Shell script to set up the environment and run the code.
* companylist.txt - List of companies, whose 10-K reports are used to perform sentiment analysis.
* SECEdgar.py - To scrape and dowload the 10-K reports.
* polarity.py - Computing sentiment polarities, and plotting their graphs.
* polarity10K.py - Running SECEdgar and polarity together.
* .pem - Your EC2 Instance key-pair file if you want to run the code on an EC2 Instance.

If you want to run it locally, then:
1. Run `chmod a+x run_job.sh`
2. Followed by: `./run_job.sh`

If you want to run it on an EC2 instance:
1. Setup an EC2 instance [here](https://aws.amazon.com/ec2/).
2. SSH into the EC2 instance, instructions can be found [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html)
3. SCP the above files (except the .pem) file to the EC2 instance, the instructions can be found in the above link.
4. Run `chmod a+x run_job.sh`
5. Followed by `./run_job.sh`

Please note, you need a minimum of 4 GB RAM to run this code.

