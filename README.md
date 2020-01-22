# IBM-project-Technion
Characterizing quantum noise via Randomized Benchmarking with restricted gate set by the advisors: Shelly Garion and ehuda Naveh


adding CNOTPauli and Pauli group

the place of the files in the code 
these files :
 
CNOTpauli_utils.py 
pauli_utils.py
circuits.py
 
should be here qiskit-ignis/qiskit/ignis/verification/randomized_benchmarking/ 

these files : 

test_CNOTpauli_random_expected.txt
test_CNOTpauli_tables_expected.txt
test_pauli_random_expected.txt
test_pauli_tables_expected.txt
test_CNOTpauli.py
test_pauli.py 

should be here qiskit-ignis/test/rb/

these files : 

Pauli_tutorial.ipynb
CNOTPauli_tutorial.ipynb
Pauli_tutorial.py
CNOTPauli_tutorial.py
and all the files in the directory Expermints

should be here qiskit-community-tutorials/ignis/ 

the files CheckIndexes.ipynb and theBug.ipynb helped us to understand a bug in the code that we fixed no need to add them but they were here :qiskit-ignis/qiskit/ignis/verification/randomized_benchmarking/ 

in order to run the code you should install qiskit and its file you can git clone from these links
https://github.com/Qiskit/qiskit-community-tutorials 
https://github.com/Qiskit/qiskit-ignis
and then move those files to their place as explained above 


in the files CNOTpauli_utils.py and pauli_utils.py we have the group utils containing functions that are used in for random benchmarking 
in circuits.py we have added a support for the groups we added ( CNOTpauli and pauli ) , 
we added in the function randomized_benchmarking_seq a code that will allow it to work with the groups we added

we wrote tests for the groups utiles 
thoes are the test files : test_CNOTpauli.py and test_pauli.py
and to check if the output is right we compared it with those files that we wrote accordingly : 
test_CNOTpauli_random_expected.txt to check the function random in CNOTpauli
test_CNOTpauli_tables_expected.txt to check the table of the members of the CNOTpauli
test_pauli_random_expected.txt to check the function random in pauli
test_pauli_tables_expected.txt to check the table of the members of the pauli

in the files Pauli_tutorial.ipynb and CNOTPauli_tutorial.ipynb we wrote tutorials for the CNOTpauli and pauli groups 
we wrote the tutorials in jupyter notebook and generated RB circuits for the groups and added a noise to it.
we wrote then in python files as well in order to run them on python also in these files CNOTPauli_tutorial.py and Pauli_tutorial.py

we wrote the file CheckIndexes.ipynb to check and print all the indexes of the CNOTPauli groups and its members 
and we found a bug and in order to explane it we wrote this file theBug.ipynb

and then there are the directory Expermints that contain all the expermints we have done on the groups with different noises 

