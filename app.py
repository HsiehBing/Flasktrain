###
import pymongo
client = pymongo.MongoClient("mongodb+srv://root:root123@mycluster.t2ueosu.mongodb.net/?retryWrites=true&w=majority")
db=client.blog


from flask import *
app=Flask(__name__, 
	static_folder="static",
	static_url_path="/"
)
app.secret_key="Only for Bing Blog"
###
 


@app.route("/")
def route():
	collection2=db.article
	all_article=collection2.find()
	if "nickname" in session:
		guests=session["nickname"]
	else:
		guests="guests"
	return render_template("index.html",guests=guests,a_a=all_article)

@app.route("/error")
def error():
	message=request.args.get("msge","The system get wrong")
	return render_template("error.html",messageh=message)

@app.route("/signin")
def signin():
	return render_template("signin.html")
@app.route("/checksignin", methods=["POST"])
def checksignin():
	email=request.form["email"]
	password=request.form["password"]
	collection=db.user
	result=collection.find_one({"$and":[{"email":email},{"password":password}]})
	if result==None:
		return redirect ("/error?msge=E-mail or password get wrong")
	else:
		
		session["nickname"]=result["nickname"]
		return redirect("/member")
@app.route("/logout")
def logout():
	del session["nickname"]
	return redirect("/")

@app.route("/signup")
def signup():	
	return render_template("signup.html")

@app.route("/checksignup", methods=["POST"])
def checksignup():
	nickname=request.form["nickname"]
	email=request.form["email"]
	password=request.form["password"]
	collection=db.user
	result=collection.find_one({"email":email})
	if result!=None:
		return redirect("/error?msge=The email is used")
	else:
		collection.insert_one({"nickname":nickname,"email":email,"password":password})
		return redirect("/confirm")
	
@app.route("/confirm")
def confirm():
	return render_template("confirm.html")

@app.route("/member")
def member():
	if "nickname" in session:
		nickname=session["nickname"]
		return render_template("member.html",nic=nickname)
	else:
		return redirect("/")
@app.route("/post")
def postlist():
	title=request.args.get("title","defaulttitle")
	content=request.args.get("content","defaultcontent")
	collection2=db.article
	collection2.insert_one({"title":title, "content":content})	
	
	return render_template("post.html", ti=title, con=content)

@app.route("/admin")
def admin():
	collection=db.user
	all_users=collection.find()
	if "admin" in session["nickname"]:
		return render_template("admin.html",users=all_users)
	else:
		return redirect("/member")


if __name__ =="__main__":
	app.run(debug=True,host="192.168.50.58",port=3050)
