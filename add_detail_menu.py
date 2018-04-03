def add_detail(t1,l):
	for i in range(1,len(l)+1):
		food_type=t1.loc[[i],["type"]].values[0][0]
		veg=t1.loc[[i],["veg"]].values[0][0]
		name=l[i]
		name=str(i)+":  "+name
		if food_type !="beverage":
			name+="  (non-veg) " if veg==0 else "  (veg) "
		name+="  "+str(t1.loc[[i],["price"]].values[0][0])+"/-"
		l[i]=name
	return (l[t1["type"]=="appetizer"],l[t1["type"]=="main_course"],l[t1["type"]=="beverage"])