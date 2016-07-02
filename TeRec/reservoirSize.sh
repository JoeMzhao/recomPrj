rm memoValueImpML.txt
rm performance.txt
rm resultTimeImpML.txt

python mySVD.py 40 10 0.001 0.04
python mySVD.py 40 30 0.001 0.04
python mySVD.py 40 50 0.001 0.04
python mySVD.py 40 70 0.001 0.04
python mySVD.py 40 90 0.001 0.04
python mySVD.py 40 110 0.001 0.04