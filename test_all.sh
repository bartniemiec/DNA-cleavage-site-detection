echo "=========== Kryterium podzialu ============="
echo "================================="
echo "D O N O R S"
echo "================================="
python3 ./main.py donors.txt 0 0 1
echo "================================="
python3 ./main.py donors.txt 1 0 1
echo "================================="
echo "A C C E P T O R S"
echo "================================="
python3 ./main.py acceptors.txt 0 0 1
echo "================================="
python3 ./main.py acceptors.txt 1 0 1
echo "================================="

echo "=========  procent zbioru =============="
echo "D O N O R S"
echo "============================================="
python3 ./main.py donors.txt 1 1 0 0 0.99 0.0
echo "============================================="
python3 ./main.py donors.txt 1 1 0 0 0.95 0.0
echo "============================================="
python3 ./main.py donors.txt 1 1 0 0 0.90 0.0
echo "============================================="
python3 ./main.py donors.txt 1 1 0 0 0.85 0.0
echo "============================================="
echo "A C C E P T O R S"
echo "============================================="
python3 ./main.py acceptors.txt 1 1 0 0 0.99 0.0
echo "============================================="
python3 ./main.py acceptors.txt 1 1 0 0 0.95 0.0
echo "============================================="
python3 ./main.py acceptors.txt 1 1 0 0 0.90 0.0
echo "============================================="
python3 ./main.py acceptors.txt 1 1 0 0 0.85 0.0
echo "============================================="

echo "=========  procent klas =============="
echo "D O N O R S"
echo "============================================="
python3 ./main.py donors.txt 1 1 0 0 1.0 0.005
echo "============================================="
python3 ./main.py donors.txt 1 1 0 0 1.0 0.01
echo "============================================="
python3 ./main.py donors.txt 1 1 0 0 1.0 0.02
echo "============================================="
python3 ./main.py donors.txt 1 1 0 0 1.0 0.05
echo "============================================="
echo "A C C E P T O R S"
echo "============================================="
python3 ./main.py acceptors.txt 1 1 0 0 1.0 0.005
echo "============================================="
python3 ./main.py acceptors.txt 1 1 0 0 1.0 0.01
echo "============================================="
python3 ./main.py acceptors.txt 1 1 0 0 1.0 0.02
echo "============================================="
python3 ./main.py acceptors.txt 1 1 0 0 1.0 0.05
echo "============================================="

echo "=========== Kryterium stopu zwykle i dodatkowe ============ "

echo "================================="
echo "D O N O R S"
echo "================================="
python3 ./main.py donors.txt 1 0 0
echo "================================="
python3 ./main.py donors.txt 1 2 0 3
echo "================================="
python3 ./main.py donors.txt 1 2 0 5
echo "================================="
python3 ./main.py donors.txt 1 2 0 7
echo "================================="
echo "A C C E P T O R S"
echo "================================="
python3 ./main.py acceptors.txt 1 0 0
echo "================================="
python3 ./main.py acceptors.txt 1 2 0 3
echo "================================="
python3 ./main.py acceptors.txt 1 2 0 5
echo "================================="
python3 ./main.py acceptors.txt 1 2 0 6
echo "================================="

echo "=========== Kryterium stopu luzne dodatkowe ============ "

echo "================================="
echo "D O N O R S"
echo "================================="
python3 ./main.py donors.txt 1 3 0 2 0.85 0.005
echo "================================="
python3 ./main.py donors.txt 1 3 0 3 0.85 0.005
echo "================================="
python3 ./main.py donors.txt 1 3 0 4 0.85 0.005
echo "================================="
echo "A C C E P T O R S"
echo "================================="
python3 ./main.py acceptors.txt 1 3 0 2 0.85 0.005
echo "================================="
python3 ./main.py acceptors.txt 1 3 0 3 0.85 0.005
echo "================================="
python3 ./main.py acceptors.txt 1 3 0 4 0.85 0.005
echo "================================="