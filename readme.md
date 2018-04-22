# HIV-1 Incidence and Infection Time Estimator

HIITE designates the infection stage as either being chronic or incident, and approximates the infection time of those incident subjects. Users can directly upload a single fasta file (number of sequences > 4) onto HITTE for instantaneous processing and output execution. HIITE takes two types of input: i) full envelope gene sequences and ii) envelope gene segment of HXB2 7134-7499 (check “HXB2 7134-7499” option). Check the “Align” command if input sequences need to be aligned. Alignment is done using a [context dependent align algorithm](https://link.springer.com/chapter/10.1007/3-540-58094-8_5). HIITE’s output includes the stage of infection (chronic or incident) along with the Hamming distance distribution plot, diversity, genome similarity index [GSI](http://p512.usc.edu/request/GSI/), and variance. For incident infection cases, estimated days post infection with 95% prediction intervals are provided.

The application is deployed [here](http://p512.usc.edu/request/)

### Reference:
[S. Y. Park, T. M. T. Love, S. Kapoor, and H. Y. Lee, HIITE: HIV-1 Incidence and Infection Time Estimator - Bioinformatics](https://www.ncbi.nlm.nih.gov/pubmed/29438560)

### Release Notes:
HIITE release supports python 2.7 only.
HITTE requires the following third-party python modules:
1. Scikit-learn (>=0.18.1)
2. Numpy (>=1.8.2)
3. Scipy (>=0.13.3)
4. Biopython (>=1.68)

### License:
HIITE is released udner the "BSD 3-clause license" as follows:
Copyright (c) 2018 All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
   * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
   * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
   * Neither the name of the copyright holder nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.



