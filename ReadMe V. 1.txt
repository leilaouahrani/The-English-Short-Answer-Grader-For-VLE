The Arabic Short Answer Grader For Virtual Learning Environment using Arabic NLP Computation 
                                    Version 1.0
This work is supported by the Ministry of Higher Education
and Scientific Research in Algeria (Project C00L07UN100120180002)
Conception & Supervision : L. Ouahrani & D. Bennouar
   
CONTENTS
1. Introduction
2. The Folder Structure
2.a. The Moodle Plugin ShortAnswer V1
2.b. Grader code on Distant server
3. How to deploy ?
4. Feedback
5. Acknowledgments


=======================
1. Introduction

This README v1.0 (June, 2020) is for The Arabic Short Answer Grader For Virtual Learning Environment 
using Arabic Linguistic statistical computations.

The grader is implemented as a plugin Moodle which extends the question_type_Engine of Moodle to grade open-ended short answers
formulated in natural language.   
We use a semantic space for Word distribution based on word cooccurrences in text corpora to capture similarity. 
The approach does not require word data models(WordNet, ArabicWordNet,  ....).  
It is particularly suitable in situations where no large, publicly available, linguistic resources can be found
for the desired language such as the Arabic Language. 
 
Actually the Grader is used on Moodle Bouira University Plateform for the learning and the assessment of 
the CyberCrimes Course in Computer Science Department.

=======================
2. Folder Structure (Plugin Moodle + Grader code on distant server)

==================
2.a. The Moodle Plugin ShortAnswer V1 (arabicanswer1) 

This is a Moodle Plugin using  moodle question type template* and adapted to grade Arabic short answers scoring using NLP computation. 

* Please see here for more information about : Moodle-Short Answer Question Type : 
https://docs.moodle.org/37/en/Short-Answer_question_type
* Please see here for a Moodle Question-Type Template https://github.com/jamiepratt/moodle-qtype_TEMPLATE

======================
2.b. Grader code on Distant server

The Approach used for the grader is described here : https://ieeexplore.ieee.org/document/8672717

The grader function is deployed on a distant server (Pythonanywhere) to release the platform 
from the assessment task for this question type, 
particularly when scoring a large number of online students at the same time.

The code in this folder + the semantic space are déployed via a web application on Pythonanywhere using the framework Flask.  
A PHP cURL script is used to connect the plugin to the Flask API which deploys the grader on PythonanyWhere.
=======================
3. How to deploy ?

- The Plugin must be installed on a Moodle plateforme to be used:
(Install the arabicanswer1.zip)
  (Dashboard / Site administration / Plugins / Install plugins). 
- A PHP cURL script is used to connect the plugin to the Flask API which deploys the grader on PythonanyWhere(all is donne in the plugin).

=======================
4. Feedback

For further questions or inquiries, you can contact:
l_ouahrani@univ-blida.dz  
 
=======================
5. Acknowledgments

We are grateful to Atoub Yasmine, Benayad Asma for their help in the first stage of the project.  

