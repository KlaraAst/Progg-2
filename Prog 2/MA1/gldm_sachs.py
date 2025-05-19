


#%%

def countPalindromes(s):

    pal = []

    for i in range(len(s)):
        pal.append(s[i])   #add all individual letters

    for i in range(len(s)-1):
        for k in range(i+1, len(s)+1):
            sub = s[i:k]
            if sub == sub[::-1]:
                if len(sub) > 1:   #already added individual letters
                    pal.append(sub)
                else:
                    pass

    nr_pal = len(pal)
    return nr_pal

s = 'tacocat'
print(countPalindromes(s))

