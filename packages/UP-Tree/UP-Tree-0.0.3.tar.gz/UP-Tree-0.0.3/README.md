# UP Tree (Utility Pattern Tree)

> > This is a simple module which takes input of transactions and provides it's UP-Tree, HeaderTable, and transactions along with their item-utilities. Each node N of a UP-Tree has six entries: N.item is the item name of N; N. count is the node utility of N; N.num is the support count of N; N.parent indicates the parent node of N; N.nextNode is a node link which may point to a node having the same item name as N.item; N.children which is a dictionary, it contains item name as key and Node as value of all nodes whoes parent is N. The Header table is a structure employed to facilitate the traversal of the UP-Tree. A header table entry contains an item name, an estimated utility value, and a link. The link points to the first node in the UP-Tree having the same item name as the entry. The nodes whose item names are the same can be traversed efficiently by following the links in header table and the node links in the UP-Tree.

Github: https://github.com/miths/UPTree

## How to use

1.  copy contents of src folder to your project folder.

2.  run**init**.py file

> UPTree.py contains all functions used and**init**.py contains main function which can execute the code.

## usage and functions

`upTree, headerTable, transanctions= UPTree(`transaction File path`, `profit file path`)`

`upTree.disp()` # prints UP-Tree

### eg:

`upTree, headerTable, transactions = UPTree('D:\user\data_proj_1.txt', 'D:\user\profit1.txt')`

## input format:

> Two text files required. One for transactions(items and quantity) and the other for profit(for each item).

### eg:

> **format:**

item1 item2 item3 item4 **:** quantity(item1) quantity(item2) quantity(item3) quantity(item4)

..

..

..

![transaction.txt](https://github.com/miths/UPTree/raw/master/img/transactions.png)

> **format:**

profit(item1)

profit(item2)

profit(item3)

profit(item4)

..

![profit.txt](https://github.com/miths/UPTree/raw/master/img/profit.png)

Note: all item names should be numericals. Profit can be float or int. Profit value should be positive for all items. All quantity values should be greater than 0. All items must have a valid quantity in every transaction. All items must have profit value.

## Output:

function returns

1. upTree
2. headertable
3. transactions

### upTree

can be printed by: `upTree.disp()`

![UPtree](https://github.com/miths/UPTree/raw/master/img/uptree.png)

Each Node of UP-Tree displays following information: <item><item utility><number of occurences in database>

### headerTable

can be printed by: `print(headerTable)`

![headerTable](https://github.com/miths/UPTree/raw/master/img/headerTable.png)

headerTable is a dictionary.
key: item, value: [transaction weighted utility, head Node of item(Node.nextNode points to other node of same item)]

### transactions

can be printed by: `print(transactions)`

![transaction](https://github.com/miths/UPTree/raw/master/img/final_transaction.png)

transactions is a dictionary in decending order according to each item's transaction weighted utility

key: transaction number, value: dictionary(item : item utility)

## Some useful definitions

### Transaction Weighted Utility

definition

> ![TWU_def](https://github.com/miths/UPTree/raw/master/img/TWU_def.png)

eg for this case

> ![TWU_ex.txt](https://github.com/miths/UPTree/raw/master/img/TWU_ex.png)

### Item Utility

definition

> The absolute utility of an item I in a transaction T is denoted as IU(I)= Quantity(I) \* Profit(I)
