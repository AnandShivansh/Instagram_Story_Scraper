import sqlite3
def viewer_who_viewed_each_story():
	conn=sqlite3.connect('record.db')
	query="select name from sqlite_master where type='table';"
	tbl=conn.execute(query)
	table_name=[]
	for x in tbl:
		table_name.append(x[0])
	for x in table_name:
		query='select name from pragma_table_info("'+x+'") where name!="ID";'
		col=conn.execute(query)
		column_name=[]
		for y in col:
			column_name.append(y[0])
		query="select ID from "+x+" where "
		for y in range(len(column_name)):
			query+=column_name[y]+"=1"
			if(y!=(len(column_name)-1)):
				query+=" and "
			else:
				query+=";"
		acc_id=conn.execute(query)
		viewer_list=[]
		for y in acc_id:
			viewer_list.append(y[0])
		print("For userID "+x+"Viewers who viewed all the stories")
		for y in range(len(viewer_list)):
			print(y+1,"  ",viewer_list[y])
		print()
viewer_who_viewed_each_story()