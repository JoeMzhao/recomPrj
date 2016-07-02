# DeMF: an online recommender systems based on matrix factorisation

Capturing users' preferences drift is a crucial property of a successful recommender systems. Based on TeRec, proposed by [Chen et al.](http://www.vldb.org/pvldb/vol6/p1254-chen.pdf), we propose DeMF, which is an online recommender system based on matrix factorisation technique, introduced by [Koren et al.](https://datajobs.com/data-science-repo/Recommender-Systems-[Netflix].pdf). We evaluated performance of both two models on [MovieLens-100k](http://grouplens.org/datasets/movielens/100k/) and [Ciao](http://www.jiliang.xyz/trust.html). The results show that compared with TeRec, DeMF show its superior properties in following aspects:

* Lower mean square error (MAE).
* Lower trend to diverge.


### Structure
----------------------
	  
Files are organised in following manner:

 |-DeMF
 
		|-mySVD.py
		
		|-sampleInput.py
		
		|-demfNoffline.sh
		
		|-iteration.sh
		
		|-cvxMAE.sh
		
		|-reservoirSize.sh
		

 |-TeRec
 
		|-mySVD.py
		
		|-sampleInput.py
		
		|-demfNoffline.sh
		
		|-iteration.sh
		
		|-cvxMAE.sh
		
		|-reservoirSize.sh
		
### To run
--------------------------------------
Requirements: 

 * Python2.7
 * NumPy 
 * SciPy 

 
`sh cvxMAE.sh` generates the convex figures.

`sh iteration.sh` generates the effects of T.

`sh reservoirSize.sh` generates the effects of size of reservoir.

`sh demfNoffline.sh` generates time and memory consumption comparison.



Experimental results will be written in following .txt file:

* memoValueImpML.txt: 
 * memory consumption of users. Offline result is shown on terminal console.
* resultTimeImpML.txt: 
 * time consumption of users. Offline result is shown on terminal console.
* performance.txt:
	* each row has format:
 		* $\alpha$, $\beta$, sizeofResv, numEpoches, iteration, pureMFmae, improvedMAE, maeImprovements
*  mae_distribution.txt:
 *   MAE improvements of each user.

_**Please note that running a new shell file will remove results of previous experiment!**_

### To Plot
-----------------------------
Using MATLAB to generate all plots:

* demfNoffline.m:
	*  Comparison of memory and time consumption between online and offline
* cvxMAE.m:
	*  MAE performance with various $\alpha$ and $\beta$
* maeDisDec.m:
	*  MAE improvements for each user
* iteration.m:
	*  MAE various with iteration
* reservoirSize.m:
	*  MAE various with reservoir size


The memory and time consumption for each user is written in files `memoValueImpML.txt` and `resultTimeImpML.txt`. To run this some manual actions have to be made since every time the number of rating events could be different. However, this figure is intuitive and simple thus not included a .m file.  

 



