# Akkademia
Akkademia is a tool for automatically transliterating Unicode cuneiform glyphs. It is written in python script and uses HMM, MEMM and BiLSTM neural networks to determine appropriate sign-readings and segmentation.

We trained these algorithms on the RINAP corpora (Royal Inscriptions of the Neo-Assyrian Period), which are available in JSON and XML/TEI formats thanks to the efforts of the Official Inscriptions of the Middle East in Antiquity (OIMEA) Munich Project of Karen Radner and Jamie Novotny, funded by the Alexander von Humboldt Foundation, available [here](<http://oracc.org/rinap/>). We achieve accuracy rates of 89.5% with HMM, 94% with MEMM, and 96.7% with BiLSTM on the trained corpora. Our model can also be used on texts from other periods and genres, with varying levels of success.

## Getting Started
Akkademia can be accessed in three different ways:
* Website
* Python package
* Github clone

The website and python package are meant to be accessible to people without advanced programming knowledge.

## Website
Go to the [Babylonian Engine website](<https://babylonian.herokuapp.com/>) (*under development*)

Go to the "Akkademia" tab and follow the instructions there for transliterating your signs.

## Python Package
Our python package "akkadian" will enable you to use Akkademia on your local machine.

### Prerequisites
You will need a Python 3.7.x installed. Our package currently does not work with other versions of python. You can follow the installation instructions [here](<https://realpython.com/installing-python/>) or go straight ahead to [python's downloads page](<https://www.python.org/downloads/>) and pick an appropriate version.

Mac comes preinstalled with python 2.7, which may remain the default python version even after installing 3.7.x. To check, type ``python --version`` into terminal. If the running version is python 2.7, the simplest short-term solution is to type ``python3`` or ``pip3`` in Terminal throughout instead of ``python`` and ``pip`` as in the instructions below.

### Package Installation
You can install the package using the pip install function. If you do not have pip installed on your computer, or you are not sure whether it is installed or not, you can follow the instructions [here](<https://www.makeuseof.com/tag/install-pip-for-python/>)

Before installing the package akkadian, you will need to install the torch package. For Windows, copy the following into Command Prompt (CMD):

```
pip install torch==1.0.0 torchvision==0.2.1 -f https://download.pytorch.org/whl/torch_stable.html
```
For Mac and Linux copy the following into Terminal:

```
pip install torch torchvision
```
Then, type the following in Command Prompt (Windows), or Terminal (Mac and Linux):

```
pip install akkadian
```
your installation should be executed. This will take several minutes.

### Running
Open a python IDE (Integrated development environment) where a python code can be run. There are many possible IDEs, see [realpython's guide](<https://realpython.com/python-ides-code-editors-guide/>) or [wiki python's list](<https://wiki.python.org/moin/IntegratedDevelopmentEnvironments>). For beginners, we recommend using Jupyter Notebook: see downloading instructions [here](<https://jupyter.org/install>), or see downloading instructions and beginners' tutorial [here](<https://realpython.com/jupyter-notebook-introduction/>).

First, import ```akkadian.transliterate``` into your coding environment:

```
import akkadian.transliterate as akk
```

Then, you can use HMM, MEMM, or BiLSTM to transliterate the signs. The functions are:

```
akk.transliterate_hmm("Unicode_signs_here")
akk.transliterate_memm("Unicode_signs_here")
akk.transliterate_bilstm("Unicode_signs_here")
akk.transliterate_bilstm_top3("Unicode_signs_here")
```
```akk.transliterate_bilstm_top3``` gives the top three BiLSTM options, while ```akk.transliterate_bilstm``` gives only the top one.

For an immediate output of the results, put the ```akk.transliterate()``` function inside the ```print()``` function. Here are some examples with their output:
```
print(akk.transliterate_hmm("𒃻𒅘𒁀𒄿𒈬𒊒𒅖𒁲𒈠𒀀𒋾"))
ša₂ nak-ba-i-mu-ru iš-di-ma-a-ti
```
```
print(akk.transliterate_memm("𒃻𒅘𒁀𒄿𒈬𒊒𒅖𒁲𒈠𒀀𒋾"))
ša₂ SILIM ba-i-mu-ru-iš-di-ma-a-ti
```
```
print(akk.transliterate_bilstm("𒃻𒅘𒁀𒄿𒈬𒊒𒅖𒁲𒈠𒀀𒋾"))
ša₂ nak-ba-i-mu-ru iš-di-ma-a-ti 
```
```
print(akk.transliterate_bilstm_top3("𒃻𒅘𒁀𒄿𒈬𒊒𒅖𒁲𒈠𒀀𒋾"))
('ša₂ nak-ba-i-mu-ru iš-di-ma-a-ti ', 'ša₂-di-ba i mu ru-iš di ma tukul-tu ', 'MUN kis BA še-MU-šub-šah-ṭi-nab-nu-ti-')
```

This line was taken from the first line of the Epic of Gilgamesh: *ša₂ naq-ba i-mu-ru iš-di ma-a-ti*; "He who saw the Deep, the foundation of the country" (George, A.R. 2003. *The Babylonian Gilgamesh Epic: Introduction, Critical Edition and Cuneiform Texts*. 2 vols. Oxford: Oxford University Press). Although the algorithms were not trained on this text genre, they show promising, useful results.

## Github
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
You will need a Python 3.7.x installed. Our package currently does not work with other versions of python. Go to [python's downloads page](<https://www.python.org/downloads/>) and pick an appropriate version.

If you don't have git installed, install git [here](<https://git-scm.com/downloads>) (Choose the appropriate operating system).

If you don't have a Github user, create one [here](<https://github.com/join?source=header-home>).

### Installing the python dependencies

In order to run the code, you will need the torch and allennlp libraries. If you have already installed the package akkadian, these were installed on your computer and you can skip to the next step.

Install torch: For Windows, copy the following to Command Prompt
```
pip install torch===1.3.1 torchvision===0.4.2 -f https://download.pytorch.org/whl/torch_stable.html
```

for Mac and Linux, copy the following to Terminal
```
pip install torch torchvision
```

Install allennlp: copy the following to Command Prompt (with windows) or Terminal (with mac): 
```
pip install allennlp==0.8.5
```

### Cloning the project

Copy the following into Command Prompt (with windows) or Terminal (with mac) to clone the project:
```
git clone https://github.com/gaigutherz/Akkademia.git
```

### Running
Now you can develop the Akkademia repository and add your improvements!

#### Training
Use the file train.py in order to train the models using the datasets. There is a function for each model that trains, stores the pickle and tests its performance on a specific corpora.

The functions are as follows:
```
hmm_train_and_test(corpora)
memm_train_and_test(corpora)
biLSTM_train_and_test(corpora)
```

#### Transliterating
Use the file transliterate.py in order to transliterate using the models. There is a function for each model that takes Unicode cuneiform signs as parameter and returns its transliteration.

Example of usage:
```
cuneiform_signs = "𒃻𒅘𒁀𒄿𒈬𒊒𒅖𒁲𒈠𒀀𒋾"
print(transliterate(cuneiform_signs))
print(transliterate_bilstm(cuneiform_signs))
print(transliterate_bilstm_top3(cuneiform_signs))
print(transliterate_hmm(cuneiform_signs))
print(transliterate_memm(cuneiform_signs))
```

## Datasets
For training the algorithms, we used the RINAP corpora (Royal Inscriptions of the Neo-Assyrian Period), which are available in JSON and XML/TEI formats thanks to the efforts of the Humboldt Foundation-funded Official Inscriptions of the Middle East in Antiquity (OIMEA) Munich Project led by Karen Radner and Jamie Novotny, available [here](<http://oracc.org/rinap/>). The current output in our website, package and code is based on training done on these corpora alone.

For additional future training, we added the following corpora (in JSON file format) to the repository: 
		
* **RIAO** - [Royal Inscriptions of Assyria online](<http://oracc.museum.upenn.edu/riao/>)
		
* **RIBO** - [Royal Inscriptions of Babylonia online](<http://oracc.museum.upenn.edu/ribo/>)
		
* **SAAO** - [State Archives of Assyria online](<http://oracc.museum.upenn.edu/saao/>)
		
* **SUHU** - [The Inscriptions of Suhu online Project](<http://oracc.museum.upenn.edu/suhu/>)

These corpora were all prepared by the Munich Open-access Cuneiform Corpus Initiative (MOCCI) and OIMEA project teams, both led by Karen Radner and Jamie Novotny, and are fully accessible for download in JSON or XML/TEI format in their respective project webpages (see left side-panel on project webpages and look for project-name downloads).

We also included a separate dataset which includes all the corpora in XML/TEI format.

### Datasets deployment

All the dataset are taken from their respective project webpages (see left side-panel on project webpages and look for project_name downloads) and are fully accessible from there.

In our repository the datasets are located in the "raw_data" directory. They can also be downloaded from the Github repository using git clone or zip download.

## Project structure

**BiLSTM_input**: 

	Contains dictionaries used for transliteration by BiLSTM.
	
**NMT_input**:

	Contains dictionaries used for natural machine translation.
	
**akkadian.egg-info**:

	Information and settings for akkadian python package.
	
**akkadian**:

	Sources and train's output.
	
	output:	Train's output for HMM, MEMM and BiLSTM - mostly pickles.
		
	__init__.py: Init script for akkadian python package. Initializes global variables.
	
	bilstm.py: Class for BiLSTM train and prediction using AllenNLP implementation.
	
	build_data.py: Code for organizing the data in dictionaries.
	
	check_translation.py: Code for translation accuracy checking.
	
	combine_algorithms.py: Code for prediction using both HMM, MEMM and BiLSTM.
	
	data.py: Utils for accuracy checks and dictionaries interpretations.
	
	full_translation_build_data.py: Code for organizing the data for full translation task.
	
	get_texts_details.py: Util for getting more information about the text.
	
	hmm.py: Implementation of HMM for train and prediction.
	
	memm.py: Implementation of MEMM for train and prediction.
	
	parse_json: Json parsing used for data organizing.
	
	parse_xml.py: XML parsing used for data organizing.
	
	train.py: API for training all 3 algorithms and store the output.
	
	translation_tokenize.py: Code for tokenization of translation task.
	
	transliterate.py: API for transliterating using all 3 algorithms.
	
**build/lib/akkadian**:

	Information and settings for akkadian python package.
	
**dist**:

	Akkadian python package - wheel and tar.
	
**raw_data**:

	Databases used for training the models:
	
	RINAP 1, 3-5
	
	Additional databases for future training:
		
	RIAO
		
	RIBO
		
	SAAO
		
	SUHU
		
	Miscellanea:
	
	tei - the same databases (RINAP, RIAO, RIBO, SAAO, SUHU) in XML/TEI format.
	
	random - 4 texts used for testing texts outside of the training corpora. They were randomly selected from RIAO and RIBO.
		
# Licensing

This repository is made freely available under the Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0) license. This means you are free to share and adapt the code and datasets, under the conditions that you cite the project appropriately, note any changes you have made to the original code and datasets, and if you are redistributing the project or a part thereof, you must release it under the same license or a similar one.

For more information about the license, see [here](<https://creativecommons.org/licenses/by-sa/3.0/>).

# Issues and Bugs

If you are experiencing any issues with the website, the python package akkadian or the git repository, please contact us at dhl.arieluni@gmail.com, and we would gladly assist you. We would also much appreciate feedback about using the code via the website or the python package, or about the repository itself, so please send us any comments or suggestions.

### Authors
* Gai Gutherz
* Ariel Elazary
* Avital Romach
* Shai Gordin
