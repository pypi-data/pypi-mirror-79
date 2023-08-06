import pickle
from sklearn.feature_extraction.text import CountVectorizer
import re
import warnings
import pkg_resources
import os

warnings.filterwarnings("ignore")



def pred(question,comments):
	comm = []
	resource_package = 'ICHT_PatientExperience'
	
	for text in comments:
		text = text.strip().lower()
		text = text.strip()
		text = re.sub('[0-9]+', '' ,text)
		comm.append(text)
		
	if question == 1:
		
		resource_path = '/'.join(('models','feature11.pkl'))
		feature_path1 = pkg_resources.resource_filename(resource_package, resource_path)
			
		resource_path = '/'.join(('models','tfidftransformer11.pkl'))
		tfidftransformer_path1 = pkg_resources.resource_filename(resource_package, resource_path)

		resource_path = '/'.join(('models','feature12.pkl'))
		feature_path2 = pkg_resources.resource_filename(resource_package, resource_path)
			
		resource_path = '/'.join(('models','tfidftransformer12.pkl'))
		tfidftransformer_path2 = pkg_resources.resource_filename(resource_package, resource_path)
		
		resource_path = '/'.join(('models','Q1Senti.pkl'))
		clf1_path = pkg_resources.resource_filename(resource_package, resource_path)
		with open(clf1_path,'rb') as clf1_file:
			clf1 = pickle.load(clf1_file)
			
		resource_path = '/'.join(('models','Q1Topic.pkl'))
		clf2_path = pkg_resources.resource_filename(resource_package, resource_path)
		with open(clf2_path,'rb') as clf2_file:
			clf2 = pickle.load(clf2_file)
		
	else:
		resource_path = '/'.join(('models','feature21.pkl'))
		feature_path1 = pkg_resources.resource_filename(resource_package, resource_path)
			
		resource_path = '/'.join(('models','tfidftransformer21.pkl'))
		tfidftransformer_path1 = pkg_resources.resource_filename(resource_package, resource_path)


		resource_path = '/'.join(('models','feature22.pkl'))
		feature_path2 = pkg_resources.resource_filename(resource_package, resource_path)
			
		resource_path = '/'.join(('models','tfidftransformer22.pkl'))
		tfidftransformer_path2 = pkg_resources.resource_filename(resource_package, resource_path)

		resource_path = '/'.join(('models','Q2Senti.pkl'))
		clf1_path = pkg_resources.resource_filename(resource_package, resource_path)
		with open(clf1_path,'rb') as clf1_file:
			clf1 = pickle.load(clf1_file)
			
		resource_path = '/'.join(('models','Q2Topic.pkl'))
		clf2_path = pkg_resources.resource_filename(resource_package, resource_path)
		with open(clf2_path,'rb') as clf2_file:
			clf2 = pickle.load(clf2_file)
	
	loaded_vec1 = CountVectorizer(decode_error= "replace", vocabulary = pickle.load(open(feature_path1, 'rb')))
	tfidftransformer1 = pickle.load(open(tfidftransformer_path1, 'rb')) 
	temp1 = loaded_vec1.transform(comm)
	test_tfidf1 = tfidftransformer1.transform(temp1)
	
	y_pred1 = clf1.predict(test_tfidf1)


	loaded_vec2 = CountVectorizer(decode_error= "replace", vocabulary = pickle.load(open(feature_path2, 'rb')))
	tfidftransformer2 = pickle.load(open(tfidftransformer_path2, 'rb')) 
	temp2 = loaded_vec2.transform(comm)
	test_tfidf2 = tfidftransformer2.transform(temp2)

	y_pred2 = clf2.predict(test_tfidf2)
	
	return y_pred1, y_pred2