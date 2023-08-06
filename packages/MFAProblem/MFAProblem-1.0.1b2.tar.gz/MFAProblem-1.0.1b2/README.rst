MFA Problem
***********
Prerequisite
------------
Git and Python installed. Preferably installed with conda and inside a virtual environment.
The virtual environment must be  activated:

.. code-block:: bash

  $conda activate "my_env"

Installation
------------
In a shell, in a working folder type:

.. code-block:: bash

  $git clone https://gitlab.com/libeigen/eigen.git

On linux or MAC: 

.. code-block:: bash

  $export EIGEN_INCLUDE=D:/TerriFlux/eigen 

(replace D:/TerriFlux/eigen by real path which includes eigen (without quote). No spaces around the equal sign. To know the path type 'pwd' on linux or mac)

On windows:

.. code-block:: bash

  $set EIGEN_INCLUDE=D:/TerriFlux/eigen 

(replace D:/TerriFlux/eigen by real path which includes eigen (without quote). To know the path type 'pwd' on linux or mac or cd on windows)

.. code-block:: bash

  pip install MFAProblem (on mac CFLAGS=-stdlib=libc++ pip install MFAProblem) (sometimes )

Test
----
To run the tests:

.. code-block:: bash

  $python -m unittest discover mfa_problem.tests.unit
  $python -m unittest discover mfa_problem.tests.integration

Run exemples
------------
Get the examples: 

.. code-block:: bash

  $git clone https://gitlab.com/greel/mfa-problem-test.git

Run the examples (modify file path):

.. code-block:: bash

  $run_mfa_problem_main_with_excel.py --input_file reconciliation/pommes_poires.xlsx
  $run_create_empty_ter.py --input_file create/pommes_poires.xlsx
  $run_mfa_problem_check_input.py --input_file check/orge_new_segm.xlsx


There may be issues on mac or linux with line return coded with windows convention, 
you need to replace CRLF by LF using Notepad++ for example. Otherwise you run the executable through python
like this:

.. code-block:: bash

  $python mfa_problem/bin/run_mfa_problem_main_with_excel.py .... (change the path)

Modify options:

.. code-block:: bash

  $run_mfa_problem_main_with_excel.py --input_file reconciliation/pommes_poires.xlsx --output_dir input
  $run_mfa_problem_main_with_excel.py --input_file reconciliation/pommes_poires.xlsx --output_dir path C:/users/julie
  $run_create_empty_ter.py --input_file create/pommes_poires.xlsx --output_dir input
  $run_create_empty_ter.py --input_file create/pommes_poires.xlsx --output_dir C:/users/julie
  $run_mfa_problem_check_input.py --input_file check\orge_new_segm.xlsx --output_dir input
  $run_mfa_problem_check_input.py --input_file check\orge_new_segm.xlsx --output_dir path C:/users/julie

Standalone to see doc:

.. code-block:: bash

  $run_mfa_problem_main_with_excel.py
  $run_create_empty_ter.py
  $run_mfa_problem_check_input.py

Notebooks
---------
In a shell in the same folder as above:

.. code-block:: bash

  $pip install jupyter
  $pip install ipyfilechooser
  $install_mfa_problem_notebook.py
  $cd ~/mfa_problem_notebook
  $jupyter notebook basic_workflow.ipynb

Project
-------
* https://gitlab.com/su-model/mfa_problem