update-conda:
	conda env update --file environment.yml --prune

create-conda: 
	conda env create -f environment.yml
