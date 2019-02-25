#python -m pip install --upgrade google-cloud-bigquery
#set GOOGLE_APPLICATION_CREDENTIALS=credentials.json

import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from google.cloud import bigquery

def main():
	client = bigquery.Client()
	df = pd.read_csv('twentysubjectnotes.csv')

	counter = Counter(df['ICD9_CODE'].tolist())
	top_10_varieties = {i[0]: idx for idx, i in enumerate(counter.most_common(20))}
	df = df[df['ICD9_CODE'].map(lambda x: x in top_10_varieties)]

	description_list = df['TEXT'].tolist()
	#clinicalTextToTest = feed_file('clinicaltext.txt')

	varietal_list = [top_10_varieties[i] for i in df['ICD9_CODE'].tolist()]
	varietal_list = np.array(varietal_list)

	count_vect = CountVectorizer()
	#count_vect2 = CountVectorizer()
	x_train_counts = count_vect.fit_transform(description_list)
	#clinicalTextToTest_counts = count_vect2.fit_transform(clinicalTextToTest)

	tfidf_transformer = TfidfTransformer()
	#tfidf_transformer2 = TfidfTransformer()
	x_train_tfidf = tfidf_transformer.fit_transform(x_train_counts)
	#clinicalTextToTest_tfidf = tfidf_transformer2.fit_transform(clinicalTextToTest_counts)

	train_x, test_x, train_y, test_y = train_test_split(x_train_tfidf, varietal_list, test_size=0.3)

	clf = MultinomialNB().fit(train_x, train_y)
	y_score = clf.predict(test_x)
	#clf.predict(clinicalTextToTest_tfidf)

	n_right = 0
	for i in range(len(y_score)):
		if y_score[i] == test_y[i]:
			n_right += 1

	print("Accuracy: %.2f%%" % ((n_right/float(len(test_y)) * 100)))

	probs = clf.predict_proba(test_x)
	#probs = clf.predict_proba(clinicalTextToTest_tfidf)
	best_n = np.argsort(probs, axis=1)[-1:]
	inv_map = {v: k for k, v in top_10_varieties.items()}
	result = [[inv_map[r] for r in res] for res in best_n]
	print(result)

	for predictions in result:
		for prediction in predictions:
			query_description = client.query("""
				SELECT DISTINCT d.desc_icd9_code, d.desc_short_title, d.desc_long_title
				FROM `medappjam2019.icd_diagnoses.desc` as d
				WHERE d.desc_icd9_code = %s
			""" % ("'" + prediction + "'"))
			description = [d.desc_short_title for d in query_description.result()][0]
			print(prediction + ": " + description)
		print("ok")

def feed_file(path_name):
	with open(path_name, 'r') as myfile:
		data = myfile.read().replace('\n', '')
	return [data]

if __name__ == '__main__':
	main()
