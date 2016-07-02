rm memoValueImpML.txt
rm performance.txt
rm resultTimeImpML.txt

python mySVD.py 1 40 0.001 0.04
python mySVD.py 3 40 0.001 0.04
python mySVD.py 5 40 0.001 0.04
python mySVD.py 7 40 0.001 0.04
python mySVD.py 9 40 0.001 0.04
python mySVD.py 11 40 0.001 0.04
python mySVD.py 13 40 0.001 0.04
python mySVD.py 15 40 0.001 0.04
