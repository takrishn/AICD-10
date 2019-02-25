MACHINE LEARNING ATTEMPT

the MIMICIII (relavent) data is stored on GCP (Google Cloud Platform). The credentials are in this folder. To run any of that, you should:

python -m pip install --upgrade google-cloud-bigquery
set GOOGLE_APPLICATION_CREDENTIALS=credentials.json

note: those commands are for windows.

ml.py was used to run queries from the databases stored in GCP, and the results were used to create a mapping that I could use for the machine learning algorithm. This mapping was then stored in tensubjectsnotes.csv.
However, these files are not here because Git doesnt appriciate any files above 100MB.

The actual machine learning is done in bayes.py. It works for the test data, and I was able to output its top ICD9 code predictions (and their corresponding ICD9 titles and descriptions by tapping into the GCP database I mentioned earlier), but I was not able to get it to work for custom text.