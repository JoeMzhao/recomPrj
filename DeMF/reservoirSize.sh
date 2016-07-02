rm memoValueImpML.txt
rm performance.txt
rm resultTimeImpML.txt

python mySVD.py 50 10 0.008 0.035
python mySVD.py 50 30 0.008 0.035
python mySVD.py 50 50 0.008 0.035
python mySVD.py 50 70 0.008 0.035
python mySVD.py 50 90 0.008 0.035
python mySVD.py 50 110 0.008 0.035