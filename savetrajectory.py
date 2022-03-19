def trajectorysave(list1,list2,list3,title1,title2):
    list4 = []
    for i in range(len(list1)):
        list4.append(round(list1[i],1))
        list4.append(round(list2[i],1))
        list4.append(round(list3[i],1))
    file= open('./trajectory/{}{}.txt'.format(title1,title2), 'w')
    counter = 0
    for fp in list4:
        counter+=1
        file.write(str(fp))
        file.write(" ")
        if counter==3:
            counter =0
            file.write('\n')
    file.close()