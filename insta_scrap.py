import os,time, getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sqlite3
options = webdriver.ChromeOptions()
options.add_argument('--headless')
stream = os.popen('echo $USER')
output = stream.read()
userr=output.split('\n')[0]
options.add_argument("user-data-dir=/home/"+userr+"/.config/google-chrome/Default")
driver = webdriver.Chrome("/home/"+userr+"/Documents/chromedriver",chrome_options=options)
def login():
	driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
	time.sleep(4)
	Handle = input("Phone number, user name, or email : \t")
	Pass = getpass.getpass(prompt="Password : \t")
	driver.find_element(By.XPATH, "/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input").send_keys(Handle)
	driver.find_element(By.XPATH, "/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input").send_keys(Pass)
	driver.find_element(By.XPATH, "/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button/div").click()
	time.sleep(4)
	try:
		driver.find_element(By.XPATH,"/html/body/div[4]/div/div/div[3]/button[2]").click()
	except:
		e=1
def get_reel_id():
	time.sleep(4)
	driver.get("view-source:https://www.instagram.com/")
	q=driver.find_element(By.XPATH,"/html").text
	time.sleep(3)
	q=q.split(',')
	reel_id=""
	for x in q:
		t=x.split(':')
		if len(t)>=2:
			if t[0]=='"viewerId"':
				reel_id=t[1].replace('"','')
				reel_id=reel_id.replace('}','')
	return reel_id
def get_query_hash():
	driver.get("https://www.instagram.com/static/bundles/es6/Consumer.js/fc33de492943.js")
	q=driver.find_element(By.XPATH,"/html/body/pre").text
	q=q.split(',')
	query_hash=""
	for x in q:
		t=x.split('=')
		if len(t)>=2:
			if t[0]=='h' and t[1][0]=='"':
				query_hash=t[1].replace('"','')
	return query_hash
def get_unique_reel(query_hash,reel_id):
	url="https://www.instagram.com/graphql/query/?query_hash="+query_hash+"&variables=%7B%22reel_ids%22%3A%5B%22"+reel_id+"%22%5D%2C%22tag_names%22%3A%5B%5D%2C%22location_ids%22%3A%5B%5D%2C%22highlight_reel_ids%22%3A%5B%5D%2C%22precomposed_overlay%22%3Afalse%2C%22show_story_viewer_list%22%3Atrue%2C%22story_viewer_fetch_count%22%3A1%2C%22story_viewer_cursor%22%3A%22%22%2C%22stories_video_dash_manifest%22%3Afalse%7D"
	driver.get(url)
	time.sleep(5)
	q=driver.find_element(By.XPATH,"/html/body/pre").text
	q=q.split(',')
	unique_reel=""
	for x in q:
		x=x.replace('{','')
		x=x.replace('}','')
		x=x.replace('"','')
		x=x.replace('[','')
		x=x.replace(']','')
		t=x.split(':')
		if len(t)>=2:
			if t[0]=='latest_reel_media':
				unique_reel=t[1]
	return unique_reel
def getting_total_seens_count(query_hash,reel_id):
	url="https://www.instagram.com/graphql/query/?query_hash="+query_hash+"&variables=%7B%22reel_ids%22%3A%5B%22"+reel_id+"%22%5D%2C%22tag_names%22%3A%5B%5D%2C%22location_ids%22%3A%5B%5D%2C%22highlight_reel_ids%22%3A%5B%5D%2C%22precomposed_overlay%22%3Afalse%2C%22show_story_viewer_list%22%3Atrue%2C%22story_viewer_fetch_count%22%3A1%2C%22story_viewer_cursor%22%3A%22%22%2C%22stories_video_dash_manifest%22%3Afalse%7D"
	driver.get(url)
	q=driver.find_element(By.XPATH,"/html/body/pre").text
	q=q.split(',')
	count=""
	for x in q:
		x=x.replace('{','')
		x=x.replace('}','')
		x=x.replace('"','')
		x=x.replace('[','')
		x=x.replace(']','')
		t=x.split(':')
		if len(t)>=3:
			if t[1]=='count':
				count=t[2]
	if count=="":
		return 0
	else:
		return int(count)
def getting_seens(query_hash,reel_id,count):
	seen_list=[]
	cursor_pos=0
	while (cursor_pos+50)<=count:
		url="https://www.instagram.com/graphql/query/?query_hash="+query_hash+"&variables=%7B%22reel_ids%22%3A%5B%22"+reel_id+"%22%5D%2C%22tag_names%22%3A%5B%5D%2C%22location_ids%22%3A%5B%5D%2C%22highlight_reel_ids%22%3A%5B%5D%2C%22precomposed_overlay%22%3Afalse%2C%22show_story_viewer_list%22%3Atrue%2C%22story_viewer_fetch_count%22%3A50%2C%22story_viewer_cursor%22%3A%22"+str(cursor_pos)+"%22%2C%22stories_video_dash_manifest%22%3Afalse%7D"
		driver.get(url)
		time.sleep(4)
		q=driver.find_element(By.XPATH,"/html/body/pre").text
		q=q.split(',')
		for x in q:
			x=x.replace('{','')
			x=x.replace('}','')
			x=x.replace('"','')
			x=x.replace('[','')
			x=x.replace(']','')
			t=x.split(':')
			if len(t)>=2:
				if t[0]=='username':
					seen_list.append(t[1])
		cursor_pos+=50	
	fpos=count-cursor_pos
	url="https://www.instagram.com/graphql/query/?query_hash="+query_hash+"&variables=%7B%22reel_ids%22%3A%5B%22"+reel_id+"%22%5D%2C%22tag_names%22%3A%5B%5D%2C%22location_ids%22%3A%5B%5D%2C%22highlight_reel_ids%22%3A%5B%5D%2C%22precomposed_overlay%22%3Afalse%2C%22show_story_viewer_list%22%3Atrue%2C%22story_viewer_fetch_count%22%3A"+str(fpos)+"%2C%22story_viewer_cursor%22%3A%22"+str(cursor_pos)+"%22%2C%22stories_video_dash_manifest%22%3Afalse%7D"
	driver.get(url)
	q=driver.find_element(By.XPATH,"/html/body/pre").text
	q=q.split(',')
	for x in q:
		x=x.replace('{','')
		x=x.replace('}','')
		x=x.replace('"','')
		x=x.replace('[','')
		x=x.replace(']','')
		t=x.split(':')
		if len(t)>=2:
			if t[0]=='username':
				seen_list.append(t[1])
	rmv=seen_list[0]
	try:
		while True:
			seen_list.remove(rmv)
	except ValueError:
		pass
	return seen_list
def get_query_hashf():
	driver.get("https://www.instagram.com/static/bundles/es6/Consumer.js/fc33de492943.js")
	q=driver.find_element(By.XPATH,"/html/body/pre").text
	q=q.replace(';',',')
	q=q.split(',')
	query_hashf=""
	i=0
	for x in q:
		t=x.split('=')
		if len(t)>=2:
			if t[0]=='const t' and t[1][0]=='"':
				tt=q[i+1].split('=')
				if tt[0]=='n':
					query_hashf=t[1].replace('"','')
		i+=1
	return query_hashf
def get_followers(query_hashf,idf):
	url="https://www.instagram.com/graphql/query/?query_hash="+query_hashf+"&variables=%7B%22id%22%3A%22"+idf+"%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A50%7D"
	driver.get(url)
	q=driver.find_element(By.XPATH,"/html/body/pre").text
	end_cursor=""
	follow_list=[]
	q=q.split(',')
	for x in q:
		x=x.replace('{','')
		x=x.replace('}','')
		x=x.replace('"','')
		x=x.replace('[','')
		x=x.replace(']','')
		t=x.split(':')
		if len(t)>=2:
			if t[0]=='end_cursor':
				end_cursor=t[1]
	end_cursor=end_cursor.replace('=','')
	for x in q:
		x=x.replace('{','')
		x=x.replace('}','')
		x=x.replace('"','')
		x=x.replace('[','')
		x=x.replace(']','')
		t=x.split(':')
		if len(t)>=2:
			if t[0]=='username':
				follow_list.append(t[1])
	message=""
	while(True):
		time.sleep(4)
		url="https://www.instagram.com/graphql/query/?query_hash="+query_hashf+"&variables=%7B%22id%22%3A%22"+idf+"%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A50%2C%22after%22%3A%22"+end_cursor+"%3D%3D%22%7D"
		driver.get(url)
		qq=driver.find_element(By.XPATH,"/html/body/pre").text
		qq=qq.split(',')
		for x in qq:
			x=x.replace('{','')
			x=x.replace('}','')
			x=x.replace('"','')
			x=x.replace('[','')
			x=x.replace(']','')
			t=x.split(':')
			if len(t)>=2:
				if t[0]=='message':
					message=t[1]
		message=message.replace(' ','')
		if(message=="executionfailure"):
			break
		for x in qq:
			x=x.replace('{','')
			x=x.replace('}','')
			x=x.replace('"','')
			x=x.replace('[','')
			x=x.replace(']','')
			t=x.split(':')
			if len(t)>=2:
				if t[0]=='end_cursor':
					end_cursor=t[1]
		end_cursor=end_cursor.replace('=','')
		for x in qq:
			x=x.replace('{','')
			x=x.replace('}','')
			x=x.replace('"','')
			x=x.replace('[','')
			x=x.replace(']','')
			t=x.split(':')
			if len(t)>=2:
				if t[0]=='username':
					follow_list.append(t[1])
	follow_list=set(follow_list)
	return follow_list
def logout():
	driver.get("https://www.instagram.com/")
	time.sleep(4)
	driver.find_element(By.XPATH,"/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[3]/a").click()
	time.sleep(4)
	driver.find_element(By.XPATH,"/html/body/div[1]/section/main/div/header/section/div[1]/div/button/span").click()
	time.sleep(4)
	driver.find_element(By.XPATH,"/html/body/div[4]/div/div/div/button[9]").click()
	driver.quit()
def create_database(seen_list,follow_list,unique_reel):
	conn=sqlite3.connect('record.db')
	query='CREATE TABLE IF NOT EXISTS TB(ID PRIMARY KEY);'
	conn.execute(query)
	conn.commit()
	for x in follow_list:
		query="SELECT EXISTS(SELECT 1 FROM TB WHERE ID='%s' LIMIT 1);"%(x)
		AS=conn.execute(query)
		ck=0
		for row in AS:
			ck=row[0]
		if ck==0:
			query="INSERT INTO TB (ID) VALUES ('%s');"%(x)
			conn.execute(query)
			conn.commit()
	uu="S"+unique_reel
	query="SELECT "+uu+" FROM TB LIMIT 1;"
	try:
		ax=conn.execute(query)
	except:
		query="ALTER TABLE TB ADD %s INT DEFAULT 0;"%(uu)
		conn.execute(query)
		conn.commit()
	for x in seen_list:
		query="UPDATE TB SET %s=1 WHERE ID='%s';"%(uu,x)
		conn.execute(query)
		conn.commit()
	query='SELECT * FROM TB;'
	aaa=conn.execute(query)
	query='SELECT * FROM TB;'
	cr=conn.execute(query)
	col_name=[description[0] for description in cr.description]
	fcl=[]
	fcl.append('SL.NO')
	for x in col_name:
		fcl.append(x)
	final_col=[]
	final_col.append(fcl)
	lf=len(fcl)
	i=1
	for x in aaa:
		tl=[]
		tl.append(i)
		for y in x:
			tl.append(y)
		final_col.append(tl)
		i+=1
	ps="{: >3} {: >25} "
	for x in range(lf-2):
		ps+="{: >20} "

	for x in final_col:
		print(ps.format(*x))
login()
print("Login : Done")
reel_id=get_reel_id()
print("Getting reel_id : Done")
idf=reel_id
query_hash=get_query_hash()
print("Getting query_hash_for_story : Done")
count=getting_total_seens_count(query_hash,reel_id)
print("Getting Seen Count : Done")
unique_reel=get_unique_reel(query_hash,reel_id)
print("Getting unique_reel : Done")
seen_list=[]
if count!=0:
	seen_list=getting_seens(query_hash,reel_id,count)
	print("Getting seen_list : Done")
query_hashf=get_query_hashf()
print("Getting query_hash_for_followers : Done")
follow_list=get_followers(query_hashf,idf)
print("Getting followers_list : Done")
logout()
print("Log Out : Done")
if len(seen_list)!=0 and unique_reel!="":
	create_database(seen_list,follow_list,unique_reel)
	print("Creating Database : Done")
	print("Viewers Count : ",count)