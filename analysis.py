#!/usr/bin/python3

from web3 import Web3
import matplotlib.pyplot as mplot
import collections
import statistics

def make_stats(flist, name):
    filename = name + '_output.txt'
    f = open(filename, 'w')
    f.write('Median ' + "{0:.3f}".format(statistics.median(flist)) + '\n')
    statrange = max(flist) - min(flist)
    f.write('Range ' + "{0:.3f}".format(statrange) + '\n')
    f.write('Mean ' + "{0:.3f}".format(statistics.mean(flist)) + '\n')
    f.write('Variance ' + "{0:.3f}".format(statistics.variance(flist)) + '\n')
    f.write('Standart deviation ' + "{0:.3f}".format(statistics.stdev(flist)) + '\n')

def make_graph(flist, name, x_axis, y_axis):
    list_cnt = collections.Counter(flist)
    mplot.scatter(list_cnt.keys(), list_cnt.values())
    mplot.title(name)
    mplot.xlabel(x_axis)
    mplot.ylabel(y_axis)
    savename = name + '.jpg'
    mplot.savefig(savename)
    mplot.close()

endpoint = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/51e26ee00e1b41bea5c825923d606446"))
n = 8908400
block_gasUsed = []
block_price = []

for i in range(1000):
    print("Current block: ", endpoint.eth.getBlock(n+i)['number'], ' (', str(i+1), ')')
    price = []
    gasUsed = []
    for j in endpoint.eth.getBlock(n+i)['transactions']:
        tran = endpoint.eth.getTransaction(j)
        receipt = endpoint.eth.getTransactionReceipt(j)
        gasUsed.append(receipt['gasUsed'])
        price.append(tran['gasPrice'])
    block_gasUsed.append(gasUsed)
    block_price.append(price)

block_num = []
block_commision = []
block_relative = []

for i in range(1000):
   commision = 0
   for j in range(len(block_price[i])):
       commision = commision + block_price[i][j] * block_gasUsed[i][j] / (10**18)
   block_num.append(i+n)
   block_commision.append(round(commision, 3))
   block_relative.append(round(((commision / (commision + 2)) * 100), 3))

make_stats(block_commision, 'absolute')
make_stats(block_relative, 'relative')

make_graph(block_commision, 'Groups of the blocks with the same comission', 'Comission in ETH', 'Number of the blocks in the group')
make_graph(block_relative, 'Groups of the blocks with the same comission percentage', 'Comission in percents', 'Number of the blocks in the group')

