import copy
import pandas as pd


class treeNode:
    def __init__(self, nameValue, TUtilty, parentNode, num=1):
        self.item = nameValue
        self.count = TUtilty
        self.num = num
        self.parent = parentNode
        self.children = {}
        self.nodeLink = None

    def inc(self, numOccur):
        global counter
        self.count += numOccur
        counter = self.count

    def disp(self, ind=1):
        print(' '*ind, self.item, ' ', self.count, ' ', self.num)
        for child in self.children.values():
            child.disp(ind+1)


def data_extraction(transPath, profitPath):
    data1 = pd.read_csv(transPath,  header=None)
    data1.columns = ['itset']
    data2 = pd.read_csv(profitPath, header=None)
    data2.columns = ['itset']
    return data1, data2


def pre_proc(data1):
    list_data = []
    trans_listItems = []
    list_qty = []
    for i in data1['itset']:
        k = i.split(':')
        k1 = k[0].split(' ')
        k2 = k[1].split(' ')
        trans_listItems.append(k1)
        list_qty.append(k2)
    mylist = []
    for i in trans_listItems:
        for j in i:
            mylist.append(j)
    mylist1 = list(set(mylist))
    tot_listItems = []
    for i in trans_listItems:
        for j in i:
            if int(j) not in tot_listItems:
                tot_listItems.append(int(j))
    tot_listItems.sort()
    return tot_listItems, trans_listItems, list_qty


def list_profit_(data2):
    list_profit = []
    for i in data2['itset']:
        list_profit.append(i)
    return list_profit


def calc_TU(trans_listItems, list_profit, list_qty):
    TU = {}
    for i in range(len(trans_listItems)):
        total = 0
        for j in range(len(trans_listItems[i])):
            k = int(trans_listItems[i][j])-1
            total = total+(int(list_qty[i][j])*float(list_profit[k]))
        TU[i+1] = total
    return TU


def calcitem_utility(trans_listItems, list_qty, list_profit):
    trans = {}
    temp = {}
    prof = 0
    for i in range(len(trans_listItems)):
        for j in range(len(trans_listItems[i])):
            prof = int(list_qty[i][j]) * \
                float(list_profit[int(trans_listItems[i][j])-1])
            temp[trans_listItems[i][j]] = prof
        trans[i+1] = temp
        temp = {}
    return trans


def calcTWU_(tot_listItems, trans, TU):
    total = 0
    TWU_ = {}
    for i in (tot_listItems):
        for j in trans:
            if str(i) in trans[j]:
                total = total+float(TU[j])
        TWU_[i] = total
        total = 0
    return TWU_


def calcTWU_sorted(TWU_):
    import operator
    sorted_by_value = sorted(TWU_.items(), key=lambda kv: kv[1])
    TWU_sorted = {}
    for i in sorted_by_value[::-1]:
        TWU_sorted[i[0]] = i[1]
    return TWU_sorted


def calcsort_trans(trans, TWU_sorted):
    temp = {}
    count = 0
    leng = len(trans)
    trans_1 = {}
    while(count < leng):
        count += 1
        temp = {}
        for i in TWU_sorted:
            flag = 0
            for j in trans:
                if str(i) in trans[j]:
                    for k in trans[j]:
                        if str(i) == k:
                            temp[i] = trans[j][k]
                            flag = 1
                        if flag == 1:
                            break
                else:
                    break
                if flag == 1:
                    break
            trans_1[count] = temp
        if count in trans:
            del trans[count]
    return trans_1


def make_headerTable(TWU_sorted):
    headerTable = {}
    for i in TWU_sorted:
        headerTable[i] = [TWU_sorted[i], None]
    return headerTable


def updateHeader(nodeToTest, targetNode):  # this version does not use recursion
    while (nodeToTest.nodeLink != None):  # Do not use recursion to traverse a linked list!
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


# dont consider hearderTable
def updateTree(items, inTree, headerTable, count, trans_2, counte, tot_count):
    # remembers the profit till that item in perticular itemset
    tot_count = items[list(items)[0]]+tot_count
    # check if orderedItems[0] in retTree.children
    if list(items)[0] in inTree.children:
        count = items[list(items)[0]]  # incrament count
        flag = 1
        # incrament count = previous count + tot_count
        inTree.children[list(items)[0]].inc(tot_count)
        inTree.children[list(items)[0]].num += 1
        counte = items[list(items)[0]]
        count = counter
    else:  # add items[0] to inTree.children
        # create a new node children node with tot_count as count value
        counte = tot_count
        inTree.children[list(items)[0]] = treeNode(
            list(items)[0], counte, inTree)
        if headerTable[list(items)[0]][1] == None:
            headerTable[list(items)[0]
                        ][1] = inTree.children[list(items)[0]]
        else:
            updateHeader(headerTable[list(items)[0]][1],
                         inTree.children[list(items)[0]])
    if len(items) > 1:  # call updateTree() with remaining ordered items
        # 1st element before deleting it  to call it while making child node in updateTree
        par = list(items)[0]
        del items[list(items)[0]]
        updateTree(
            items, inTree.children[par], headerTable, count, trans_2, counte, tot_count)


def to_create_tree(trans_1, headerTable):
    trans_2 = copy.deepcopy(trans_1)
    # create tree                  ## dont consider hearderTable
    retTree = treeNode('Null Set', 1, None)
    counte = 0
    count = 0
    for i in trans_2:
        items = trans_2[i]
        tot_count = 0
        updateTree(items, retTree, headerTable,
                   count, trans_2, counte, tot_count)
    return retTree, headerTable, trans_1


def UPTree(transPath, profitPath):
    data1, data2 = data_extraction(transPath, profitPath)
    tot_listItems, trans_listItems, list_qty = pre_proc(data1)
    list_profit = list_profit_(data2)
    TU = calc_TU(trans_listItems, list_profit, list_qty)
    trans = calcitem_utility(trans_listItems, list_qty, list_profit)
    TWU_ = calcTWU_(tot_listItems, trans, TU)
    TWU_sorted = calcTWU_sorted(TWU_)
    trans_1 = calcsort_trans(trans, TWU_sorted)
    headerTable = make_headerTable(TWU_sorted)
    return to_create_tree(trans_1, headerTable)
