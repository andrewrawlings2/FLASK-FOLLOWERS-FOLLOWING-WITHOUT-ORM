
#EXPLORE PAGE WHERE YOU CAN FOLLOW NEW PEOPLE

@app.route('/explore/', methods=["GET", "POST"])
@login_required
def explore():
	try:
		accounts = []
		c, conn = connection()
		x = int(c.execute("SELECT uid FROM accounts ORDER BY uid DESC"))
		for num in range(1, x+1):
			account=[]
			
			username=c.execute("SELECT username FROM accounts WHERE uid = {}".format(num))
			username=str(c.fetchone()[0])
			account.append(username)
			
			name=c.execute("SELECT name FROM accounts WHERE uid = {}".format(num))
			name=str(c.fetchone()[0])
			account.append(name)
			
			accounts.append(account)
			
			followers = c.execute("SELECT followers FROM accounts WHERE uid = '{}'".format(num))
			followers = str(c.fetchone()[0])
			followers = followers.split("|")
			if session['username'] in followers:
				session[username]=True
		
		if request.method == "POST":
			user = request.form["Username"]
			followers = c.execute("SELECT followers FROM accounts WHERE username = '{}'".format(user))
			followers = str(c.fetchone()[0])
			followers = followers + ("|" + session['username'])
			c.execute("UPDATE accounts SET followers = '{}' WHERE username = '{}'".format(followers, user))
			
			following = c.execute("SELECT following FROM accounts WHERE username = '{}'".format(session['username']))
			following = str(c.fetchone()[0])
			following = following + ("|" + user)
			c.execute("UPDATE accounts SET following = '{}' WHERE username = '{}'".format(following, session['username']))
			conn.commit()
		c.close()
		conn.close()
		return render_template("explore.html", title="explore", accounts=accounts)
	except Exception as e:
		return str(e)
    
#PROFILE PAGE WHERE YOU CAN SEE YOUR FOLLOWERS, FOLLOWING, AND OLD POSTS
		
@app.route('/profile/')
@login_required
def profile():
	try:
		dash=[]
		c, conn = connection()
		x = int(c.execute("SELECT pid FROM posts ORDER BY pid DESC"))
		for num in range(1,x+1):
			posts=[]
			username = c.execute("SELECT username FROM posts WHERE pid = {}".format(num))
			username = str(c.fetchone()[0])
			posts.append(username)
			
			author = c.execute("SELECT author FROM posts WHERE pid = {}".format(num))
			author = str(c.fetchone()[0])
			posts.append(author)
			
			title = c.execute("SELECT title FROM posts WHERE pid = {}".format(num))
			title = (str(c.fetchone()[0]).decode("string_escape"))
			posts.append(title)
			
			body = c.execute("SELECT body FROM posts WHERE pid = {}".format(num))
			body = (str(c.fetchone()[0])).decode("string_escape")
			posts.append(body)
			
			dash.append(posts)
			
		followers = c.execute("SELECT followers FROM accounts WHERE username = '{}'".format(session['username']))
		followers = str(c.fetchone()[0])
		followers = followers.split("|")	
		followers = len(followers)
		
		following = c.execute("SELECT following FROM accounts WHERE username = '{}'".format(session['username']))
		following = str(c.fetchone()[0])
		following = following.split("|")
		following=len(following)
		return render_template("profile.html", title="Profile", postings=dash, followers=followers, following=following)
	except Exception as e:
		return(str(e))


#SHOWS YOUR FOLLOWERS IN A LIST

@app.route('/followers/')
@login_required
def followers():
	try:
		c, conn = connection()
		followers = c.execute("SELECT followers FROM accounts WHERE username = '{}'".format(session['username']))
		followers = str(c.fetchone()[0])
		followers = followers.split("|")
		return render_template("followers.html", title="Followers", followers=followers)
	except Exception as e:
		return str(e)

#SHOWS FOLLOWING IN A LIST
@app.route('/following/')
@login_required
def following():
	try:
		c, conn = connection()
		following = c.execute("SELECT following FROM accounts WHERE username = '{}'".format(session['username']))
		following = str(c.fetchone()[0])
		following = following.split("|")
		return render_template("following.html", title="Following", following=following)
	except Exception as e:
		return str(e)
