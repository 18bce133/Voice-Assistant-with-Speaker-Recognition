# PYTHON-PROJECT
PSC project

Topic: Voice Assistant with Speaker Recognition

Group Members: NIHAR THAKKAR 18BCE133
	             MEET MAVANI 18BCE118
	             KHUSHAL ASAWA 18BCE094

Details:

Description of the project:

#Acts as voice assistant which can perform the following FEATURES:

_______________________________________________________________________________________________________________________________________
		                   FEATURE	          |		         VOICE COMMANDS
__________________________________________________________|____________________________________________________________________________
							  |
1) Wikipedia search					  |	Wikipedia "......."         e.g. Wikipedia Nirma university
   				        	          |
2) open Youtube			                          |	Open "Youtube"  
                                                          |
3) Search Youtube                                         |     Search youtube "......."    e.g. search youtube nirma university
 							  |
4) open Google						  |	Open "Google"  
 	                                                  |
5) search google                                          |     Search google "....."       e.g. search google nirma university
                                                          |
6) Open any website as mentioned by user                  |	Open "........."            e.g. open facebook.com
							  |
7) Lock the computer					  |	Lock
		                                          |
8) Can show news			                  |	Show News
                                                          |
9) Test speed of internet connection	                  |	Test Speed of Internet
					                  |
10) Check internet connection(connected or not) 	  |	Check Internet Connection
				                          |
11) Can show current location of the user	          |	Show Location
			                                  |
12) Shows RAM Usage			                  |	Memory Usage
					                  |
13) Speaker recognition(RECOGNIZE,ADD USER)               |	(a)RECOGNIZE: To recognize the existing user(if user is not there 'user                                                           |                   not recognized')
						          |	(b)Add User: To add new user 
                                               		  |
14) Ask any general knowledge question          	  |       E.g. What is capital of India
                                                	  |
15) Ask any mathematical calculation question   	  |       e.g. what is 5+6     e.g. what are roots of x^2 - 2x + 1. 
                                                	  |
16) Weather condition of any place              	  |       e.g. What is temperature in America
                                                	  |
17) General statements                          	  |       e.g. How are you ?
__________________________________________________________|______________________________________________________________________



FUNCTIONS:

#Speech Recognition using unsupervised ML model gaussian mixture model(GMM):

-->A Gaussian mixture model(GMM) is a probabilistic model that assumes all the data points are generated from a mixture of a finite number of Gaussian distributions with unknown 
   parameters. One can think of mixture models as generalizing k-means clustering to incorporate information about the covariance structure of the data as well as the centers 
   of the latent Gaussians.



#Process:
-->First audio is converted into MFCC features then from it delta is extracted of the given feature.Then both MFCC and extracted delta are combined to provide input to GMM model.

#ADD USER feature:
-->User have to speak his/her name one time at a time the system ask the user and after that the program will ask the user to say its name 3 times. It saves three voice smaples 
   of the user.

#RECOGNIZE feature:

1)This function of the program  recognizes voice of the user as the user have to speak his/her name as the system asks. 
2)As the user speaks his/her name the function saves the voice sample as a test.wav file and than Reads it to extract MFCC features.
3)Load all the pre-trained gmm models and passes the new extracted MFCC vector into the gmm.score(vector) function checking with each model one-by-one and sums the scores to
  calculate log_likelihood of each model. Takes the argmax value from the log_likelihood which provides the prediction of the user with highest prob distribution.


#Libraries included:
1) os 
2) glob
3) pickle
4) time
5) pyttsx3
6) speech_recognition
7) sys
8) wave
9) Sklearn ==> gaussian_mixture
10) scipy
11) pyaudio
12) python_speech_features etc








