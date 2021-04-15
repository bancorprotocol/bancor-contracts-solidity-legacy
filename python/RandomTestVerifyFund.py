import sys
import random
import FormulaSolidityPort


from decimal import Decimal
from decimal import getcontext
getcontext().prec = 80 # 78 digits for a maximum of 2^256-1, and 2 more digits for after the decimal point


def formulaTest(supply, balance1, weight1, balance2, weight2, amount0):
    amount1 = FormulaSolidityPort.fundCost(supply, balance1, weight1 + weight2, amount0)
    amount2 = FormulaSolidityPort.fundCost(supply, balance2, weight1 + weight2, amount0)
    amount3 = FormulaSolidityPort.purchaseTargetAmount(supply, balance1, weight1, amount1)
    amount4 = FormulaSolidityPort.purchaseTargetAmount(supply + amount3, balance2, weight2, amount2)
    return Decimal(amount0) / Decimal(amount3 + amount4)


size = int(sys.argv[1]) if len(sys.argv) > 1 else 0
if size == 0:
    size = int(input('How many test-cases would you like to execute? '))


minRatio = Decimal('+inf')
maxRatio = Decimal('-inf')
numOfFailures = 0


for n in range(size):
    supply = random.randrange(2, 10 ** 26)
    balance1 = random.randrange(1, 10 ** 23)
    weight1 = random.randrange(1, 1000000)
    balance2 = random.randrange(1, 10 ** 23)
    weight2 = random.randrange(1, 1000000)
    amount0 = random.randrange(1, supply // 10)
    try:
        ratio = formulaTest(supply, balance1, weight1, balance2, weight2, amount0)
        minRatio = min(minRatio, ratio)
        maxRatio = max(maxRatio, ratio)
    except Exception as error:
        ratio = 0
        numOfFailures += 1
    print('Test #{}: ratio = {:.24f}, minRatio = {:.24f}, maxRatio = {:.24f}, num of failures = {}'.format(n, ratio, minRatio, maxRatio, numOfFailures))
