from flask import Flask, render_template, request, redirect, url_for, session
import UserManager as UM
import os
import housepointsManger
app = Flask(__name__)
app.secret_key='AAAAB3NzaC1yc2EAAAABJQAAAQEAvI+0heuc2jKKSiaUEMTay7xsOhEOwapBsosHgo8jFbiELcXB1gwtELKmiLdkFRoowBb2Ga1VRJVtgeLtetM4FYu7xbRtoQB/E3tbnAJbiMy4pUCGMeI2lIFTFL0vWHGsqH/5qdoXu0dFijfdyxqvj/F5SZH7vpIXNZJu9Nvsr4UEnDWl16ndcVHsel1aMdW93I2OGLpEf8yvMR+Lq7ugVldUu2dC3FJMbZ4OkQiafDqA4ulLKk1SFRC0SsFlhIm/7XZVua4ckxEYdFRAn5NIC76ARyQUBANhIHhGkdApHm4m6ykhtozEPVagjIsNtuaZKFqOESL3ltIotHIHar/HL4Q'
userManager = UM.UserManager()
userInfo = None
userName = None
@app.route('/')
def homepage():
    chouse=housepointsManger.view()
    york = chouse[0]
    stuart = chouse[3]
    lancaster = chouse[2]
    tudor = chouse[1]
    houseList = [{'house': 'York', 'points': int(york), 'color': 'yellow'}, {'house': 'Tudor', 'points': int(tudor), 'color': 'blue'}, {'house': 'Lancaster', 'points': int(lancaster), 'color': 'red'}, {'house': 'Stuart', 'points': int(stuart), 'color': 'green'}]
    sortedHouseList = housepointsManger.sort(houseList)
    if 'UserId' in session:
        userId = session['UserId']
        return render_template('home.html', userId=userId,  houseList=sortedHouseList)
    else:
        userId= ''
        return render_template('home.html', userId=userId,  houseList=sortedHouseList)
@app.route('/login')
@app.route('/auth/login')
def login():
    return render_template('login.html')
@app.route('/logout')
@app.route('/auth/logout')
def logout():
    userInfo=None
    session.pop('UserId', None)
    return render_template('logout.html')
@app.route('/service/auth', methods=['POST']) 
def auth_service():
    UserId = request.form['uname']
    Pwd = request.form['psw']
    print(UserId,Pwd)
    res = userManager.Auth(UserId, Pwd)
    userInfo = res['user'] 
    if userInfo != None:    
        userName=UserId
        session['UserId'] = UserId
        userData = userManager.getDetails(UserId)
        session['role'] = userData[2]
        return redirect(url_for('homepage'))        
        return redirect(url_for('login'))
@app.route('/HousePoints/Manage')
def manage_housepoints():
    userData = userManager.getDetails(session['UserId'])
    chouse=housepointsManger.view()
    york = chouse[0]
    stuart = chouse[3]
    lancaster = chouse[2]
    tudor = chouse[1]
    if session['role']=='teacher':
        return render_template('managehousepoints.html', york=york, lancaster=lancaster, tudor=tudor, stuart=stuart)
    elif session['role'] == 'admin' :
        return render_template('remotecmd.html', userId=session['UserId'])
@app.route('/service/housepoints/modify', methods=['POST'])
def service_house_points_modify():
    yorkP=request.form['yorkPlus']
    yorkM=request.form['yorkMinus']
    tudorP=request.form['tudorPlus']
    tudorM=request.form['tudorMinus']
    lancasterP=request.form['lancasterPlus']
    lancasterM=request.form['lancasterMinus']
    stuartP=request.form['stuartPlus']
    staurtM=request.form['stuartMinus']
    to_modify=yorkP,yorkM,tudorP, tudorM, lancasterP, lancasterM, stuartP, staurtM
    housepointsManger.modify(to_modify)
    return redirect('/')
@app.route('/auth/signup/<signup_key>')
def signup(signup_key):
    keys=open('/home/site/wwwroot/User-Info/signup_keys.keys', 'r')
    signup_keys=keys.read()
    keys.close()
    if signup_key in signup_keys:
        return render_template('signup.html')
    else:
        return render_template('access_denied.html')
@app.route('/service/signup', methods=['POST'])
def signup_service():
    userName=request.form['userName']
    password=request.form['pwd']
    userManager.Signup(userName, password,'teacher')
    return redirect('/auth/login')
@app.route('/service/housepoints/reset')
def reset_housePoints():
    housepointsManger.reset()
    return redirect('/')
@app.route('/service/housepoints/restore')
def restore_housePoints():
    housepointsManger.restore()
    return redirect('/')
@app.route('/embed/housepoints')
def house_embed():
    chouse=housepointsManger.view()
    york = chouse[0]
    stuart = chouse[3]
    lancaster = chouse[2]
    tudor = chouse[1]
    houseList = [{'house': 'York', 'points': int(york), 'color': 'yellow'}, {'house': 'Tudor', 'points': int(tudor), 'color': 'blue'}, {'house': 'Lancaster', 'points': int(lancaster), 'color': 'red'}, {'house': 'Stuart', 'points': int(stuart), 'color': 'green'}]
    sortedHouseList = sortedHouseList = housepointsManger.sort(houseList)
    return render_template('embed_pointsView.html', houseList=sortedHouseList)
@app.route('/service/auth/password',methods=['POST'])
def change_password():
    newpassword=request.form['psw']
    userManager.change_password(session['UserId'] ,newpassword)
    return redirect('/')
@app.route('/profile')
def profile():
    return render_template('editPwd.html')
@app.route('/service/housepoints/remotecmd', methods=['POST'])
def remotecmd():
    cmd=request.form['cmd']
    res=housepointsManger.cmd(cmd)
    return redirect('/HousePoints/Manage')
@app.route('/services/quicklogin/<userId>/<authKey>')
def quick_login(userId, authKey):
    res=userManager.KeyAuth(userId, authKey)
    userInfo = res['user'] 
    if userInfo != None:  
        UserId=userId  
        session['UserId'] = UserId
        userData = userManager.getDetails(UserId)
        session['role'] = userData[2]
        return redirect(url_for('homepage'))        
    else:
        return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0')