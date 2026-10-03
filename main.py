import heapq
from itertools import count
from collections import Counter
import os 

class Node:
    def __init__(self , val : str , index : int , freq : int) -> None:
        self.val : str = val
        self.freq = freq
        self.index = index
        self.left : Node | None  = None
        self.right : Node | None  = None

    def __lt__(self , other):
        if self.freq != other.freq:
            return self.freq < other.freq

        if self.val != other.val:
            return self.val < other.val
            

        return self.index < other.index

class HuffmanCoding:
    def __init__(self , word) -> None:
        self.word = word
        self.old_word = word
        self.freqency = None
        self.counter = count()
        self.node_by_freq = []
        self.root = None
        self.codes = {}
        self.encoded_string = ""
        self.decoded_string = ""

    def init_freqency(self):
        self.freqency = Counter(self.word)
        self.word = list(self.freqency.keys())

    def init_heap(self):
        for char in self.word:
            heapq.heappush(self.node_by_freq , Node(val = char , index=next(self.counter) , freq = self.freqency[char]))

    def showNodes(self):
        print((" - ".join([f"{node.val}[{node.freq}]" if node.val != "" else f"{node.freq}"  for node in self.node_by_freq])).center(200))

    def merge(self, a : Node , b : Node) -> Node:
        newFreq = a.freq + b.freq
        newNode = Node(val = "", index = next(self.counter) , freq = newFreq)
        newNode.left = a 
        newNode.right = b 
        return newNode

    def build(self) -> Node: 
        while len(self.node_by_freq) > 1:
            self.showNodes()

            a = heapq.heappop(self.node_by_freq)
            b = heapq.heappop(self.node_by_freq)

            newNode = self.merge(a , b)

            heapq.heappush(self.node_by_freq , newNode)

        self.root = self.node_by_freq[0]
        return self.root

    def encode_helper(self , root : Node , code : str = ""):
        if root.left is None and root.right is None:
            self.codes[root.val] = code if code else "0"
            return

        if root.left:
            self.encode_helper(root.left, code + '0')
        if root.right:
            self.encode_helper(root.right, code + '1')


    def encode(self , root : Node , code : str = ""):
        self.encode_helper(root , code)

        for char in self.old_word : 
            self.encoded_string += self.codes[char]
            
        return self.encoded_string

    def decode(self):
        if self.root and self.encoded_string: 
            current_node = self.root
            for bit in self.encoded_string:
                if bit == '0':
                    if current_node.left : 
                        current_node = current_node.left
                    else : 
                        continue
                else:
                    if current_node.right : 
                        current_node = current_node.right
                    else : 
                        continue

                if current_node.left is None or current_node.right is None:
                    self.decoded_string += current_node.val
                    current_node = self.root

            return self.decoded_string
        else:
            raise Exception("you need to encode first to encode")


filePath = "./file.txt"

def parse_file(path : str) -> list[str]: 
    words = []
    seen = set() 

    with open(path , "r" , encoding="utf-8") as f : 
        lines = f.readlines()

        for line in lines:
            for word in line.split(" "): 
                if word in seen : 
                    continue

                if "\n" in word : 
                    word = word[:-1]
                if word : 
                    seen.add(word)
                    words.append(word)

    return words
            


if os.path.exists(filePath) : 
    words = parse_file(filePath)        

    for word in words:
        tree = HuffmanCoding(word)

        tree.init_freqency()
        tree.init_heap()

        root = tree.build()
        tree.showNodes()
        print(tree.encode(root))
        print(tree.decode())
        print("=" * 30)
else:
    raise FileNotFoundError("the provided path doesn't exist") 

