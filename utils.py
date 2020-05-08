def and_two_list(l1, l2):
    l3 = []
    for i in range(len(l1)):
        l3.append(l2[i] & l1[i])
    return l3
