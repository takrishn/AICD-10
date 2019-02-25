#python -m pip install --upgrade google-cloud-bigquery
#set GOOGLE_APPLICATION_CREDENTIALS=credentials.json

#get the first 10 icd9_diagnoses
#SELECT *
#FROM `medappjam2019.icd_diagnoses.diag`
#LIMIT 10

#get all icd9_codes for the subject_id 256
#SELECT diagnoses.diag_icd9_code
#FROM `medappjam2019.icd_diagnoses.diag` as diagnoses
#WHERE 256 = diagnoses.diag_subject_id

#so all I have to do is say for each note, find all
#the icd9 codes and give them as a list. then i can feed them
#into the neural net???
from google.cloud import bigquery
import csv

def query_diagnoses():
	client = bigquery.Client()
	codes = []
	notes = []
	subjects = []
	rows = []
	rowCounter = 1;

	#all unique subject_id's that have notes
	query_unique_subject_id = client.query("""
		SELECT DISTINCT noteevent.note_subject_id
		FROM `medappjam2019.icd_diagnoses.note` AS noteevent
	""")
	subject_ids = [s.note_subject_id for s in query_unique_subject_id.result()][0:20]
	
	for subject in subject_ids:
		#all notes associated with the subject_id. 
		#identified by their primary key = note_row_id
		query_notes = client.query("""
			SELECT noteevent.note_row_id, noteevent.note_text
			FROM `medappjam2019.icd_diagnoses.note` AS noteevent
			WHERE noteevent.note_subject_id = %d
		""" % (subject))
		note_texts = [n.note_text for n in query_notes.result()]

		#all icd9_codes associated with the subject_id. 
		#identified by diag_icd9_code
		query_codes = client.query("""
			SELECT diagnoses.diag_icd9_code
			FROM `medappjam2019.icd_diagnoses.diag` as diagnoses
			WHERE diagnoses.diag_subject_id = %d
		""" % (subject))
		code_ids = [c.diag_icd9_code for c in query_codes.result()]

		for code in code_ids:
			for note in note_texts:
				codes.append(str(code))
				notes.append(note)
				subjects.append(subject)
				rows.append(rowCounter)
				rowCounter += 1

	with open('twentysubjectnotes.csv', 'w', newline='') as f:
	    writer = csv.writer(f)
	    writer.writerows(zip(rows, subjects, codes, notes))

	#the actual query
	# query_job = client.query("""
	# 	SELECT diagnoses.diag_icd9_code, diagnoses.diag_subject_id
	# 	FROM `medappjam2019.icd_diagnoses.diag` as diagnoses
	# 	WHERE 256 = diagnoses.diag_subject_id
	# """)

	# results = query_job.result()  # Waits for job to complete.

	# for row in results:
	# 	print("{} : {}".format(row.diag_icd9_code, row.diag_subject_id))

def main():
	pass

if __name__ == '__main__':
	main()
	query_diagnoses()

#must refactor data:
#code1: note1_id, note2_id, note3_id, note4_id, etc.
#code2: note3_id, note4_id, note1_id, etc.
#code3: note3_id, note45_id, etc.



