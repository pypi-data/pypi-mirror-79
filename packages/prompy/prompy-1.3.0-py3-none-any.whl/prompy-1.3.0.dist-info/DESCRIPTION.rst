# prompy

prompy is a library developed as an assisting tool for writing scripts to be executed by the ProM CLI. The ProM CLI is the commandline interface variant of ProM, which is on its own a GUI based extensible framework that supports a wide variety of process mining techniques. prompy is always used in combination with ProM, hence this should be installed beforehand, which can be done from its website [www.promtools.org/doku.php](www.promtools.org/doku.php). The ProM CLI takes Java scripts as input which contains runtime interpreted Java code and could include functions from the CLI variants of ProM plugins. For various reasons, it could be a tedious task to write these scripts, with which prompy could help by implementing functions that generate the Java code for often used plugins like importing event log data, petrinets, soundness checking, conformance checking and process discovery. Furthermore, it offers the functionality of generating template Python implementations for each available ProM plugin function which allows for using an IDE with autocomplete. An extensive list of examples can be found in the 'examples' directory on the gitlab page [https://gitlab.com/dominiquesommers/prompy](https://gitlab.com/dominiquesommers/prompy).

prompy can be easily installed by `pip install prompy`.


