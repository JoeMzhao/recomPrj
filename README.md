# DeMF: an online recommender systems based on matrix factorisation
### Structure
----------------------
The folder includes related codes for DeMF and TeRec. Following is structure of this folder
 |-DeMF
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-mySVD.py
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-sampleInput
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-demfNoffline.sh
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-iteration.sh
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-cvxMAE.sh
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-reservoirSize.sh
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-u.data

 |-TeRec
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-mySVD.py
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-sampleInput
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-demfNoffline.sh
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-iteration.sh
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-cvxMAE.sh
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-reservoirSize.sh
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-u.data
### To run
--------------------------------------
`sh cvxMAE.sh` generates the convex figures
`sh iteration.sh` generates the effects of T
`sh reservoirSize.sh` generates the effects of size of reservoir
`sh demfNoffline.sh` generates time and memory consumption comparison

Experimental results will be written in following .txt file:
* memoValueImpML.txt => memory consumption of users. Offline result is shown on terminal console.
* resultTimeImpML.txt => time consumption of users. Offline result is shown on terminal console.
* performance.txt => each row has format: 
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $\alpha$, $\beta$, sizeofResv, numEpoches, iteration, pureMFmae, improvedMAE, maeImprovements
*  mae_distribution.txt => MAE improvements of each user.

_**Please note that running a new shell file will remove results of previous experiment!**_

### To Plot
-----------------------------
Using MATLAB to generate all plots:
* demfNoffline.m => Comparison of memory and time consumption between online and offline
* cvxMAE.m => MAE performance with various $\alpha$ and $\beta$
* maeDisDec.m => MAE improvements for each user
* iteration.m => MAE various with iteration
* reservoirSize.m => MAE various with reservoir size
The memory and time consumption for each user is written in files `memoValueImpML.txt` and `resultTimeImpML.txt`. To run this some manual actions have to be made since every time the number of rating events could be different. However, this figure is intuitive and simple thus not included a .m file.  

 



