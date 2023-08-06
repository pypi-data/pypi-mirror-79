class Number:
    
    #normalize
    def norm(x,min,max):
        n = (x-min)/(max - min)
        return n


if __name__ == "__main__":
   n =  Number.norm(0,-10,1000)
   print(n)
