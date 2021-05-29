from flask import Flask, render_template, request, redirect, url_for, session
import UserManager as UM
import os
import housepointsManger
import requests
app = Flask(__name__)
app.secret_key='AAAAB3NzaC1yc2EAAAABJQAAAQEAvI+0heuc2jKKSiaUEMTay7xsOhEOwapBsosHgo8jFbiELcXB1gwtELKmiLdkFRoowBb2Ga1VRJVtgeLtetM4FYu7xbRtoQB/E3tbnAJbiMy4pUCGMeI2lIFTFL0vWHGsqH/5qdoXu0dFijfdyxqvj/F5SZH7vpIXNZJu9Nvsr4UEnDWl16ndcVHsel1aMdW93I2OGLpEf8yvMR+Lq7ugVldUu2dC3FJMbZ4OkQiafDqA4ulLKk1SFRC0SsFlhIm/7XZVua4ckxEYdFRAn5NIC76ARyQUBANhIHhGkdApHm4m6ykhtozEPVagjIsNtuaZKFqOESL3ltIotHIHar/HL4Q'
userManager = UM.UserManager()
userInfo = None
userName = None
house1Name='York'
house2Name='Tudor'
house3Name='Lancaster'
house4Name='Stuart'
# Notes:
#
# House ids are...
# House 1 is York
# House 2 is Tudor
# House 3 is Lancaster
# House 4 is Stuart
#
# This is a Flask based web app
@app.route('/')
def homepage():
    winning='no one'
    chouse=housepointsManger.view()
    house1 = chouse[0]
    house4 = chouse[3]
    house3 = chouse[2]
    house2 = chouse[1]
    houseList = [{'house': house1Name, 'points': int(house1), 'color': 'yellow'}, {'house': house2Name, 'points': int(house2), 'color': 'blue'}, {'house': house3Name, 'points': int(house3), 'color': 'red'}, {'house': house1Name, 'points': int(house4), 'color': '#00FF00'}]
    sortedHouseList = housepointsManger.sort(houseList)
    winner=sortedHouseList[0]
    if str(winner['points']) != '0':
        winning = winner['house']+' with ' + str(winner['points'])+ ' points'
    else:
        winner={'house':winner['house'], 'points':1}
        winning='no one'
    if 'UserId' in session:
        userId = session['UserId']
        return render_template('home.html', userId=userId,  houseList=sortedHouseList, winning=winning, winningPoints=winner['points'])
    else:
        userId= ''
        return render_template('home.html', userId=userId,  houseList=sortedHouseList, winning=winning, winningPoints=winner['points'])
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
    else:   
        return redirect(url_for('login'))
@app.route('/HousePoints/Manage')
def manage_housepoints():
    pointsFile=open(r'House-Data/Points.txt','r')
    points=pointsFile.read()
    pointsFile.close()
    try:
        requests.get('https://westlodgeHPbackuprestore.azurewebsites.net/backup/8432658q647q259/'+points)
    except:
        print('INFO: WEB BACKUP ERR')
    chouse=housepointsManger.view()
    york = chouse[0]
    stuart = chouse[3]
    lancaster = chouse[2]
    tudor = chouse[1]
    if session['role']=='teacher':
        return render_template('managehousepoints.html', york=york, lancaster=lancaster, tudor=tudor, stuart=stuart)
    elif session['role'] == 'admin' :
        return render_template('remotecmd.html', userId=session['UserId'],york=york, lancaster=lancaster, tudor=tudor, stuart=stuart)
@app.route('/service/housepoints/modify', methods=['POST'])
def service_house_points_modify():
    house1P=request.form['yorkPlus']
    house1M=request.form['yorkMinus']
    house2P=request.form['tudorPlus']
    house2M=request.form['tudorMinus']
    house3P=request.form['lancasterPlus']
    house3M=request.form['lancasterMinus']
    house4P=request.form['stuartPlus']
    house4M=request.form['stuartMinus']
    to_modify=house1P,house1M,house2P, house2M, house3P, house3M, house4P, house4M
    housepointsManger.modify(to_modify)
    return redirect('/')
@app.route('/auth/signup/<signup_key>')
def signup(signup_key):
    keys=open(r'User-Info/signup_keys.keys', 'r')
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
    house1 = chouse[0]
    house4 = chouse[3]
    house3 = chouse[2]
    house2 = chouse[1]
    houseList = [{'house': house1Name, 'points': int(house1), 'color': 'yellow'}, {'house': house2Name, 'points': int(house2), 'color': 'blue'}, {'house': house3Name, 'points': int(house3), 'color': 'red'}, {'house': house1Name, 'points': int(house4), 'color': '#00FF00'}]
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
@app.route('/embed/calculator')
def calculator():
    return render_template('calculator.html')
@app.route('/services/restore/<points>')
def restoreDataFromBR(points):
    print('INFO: Sys engaging restore')
    pointsFile=open(r'House-Data/Points.txt','w')
    pointsFile.write(points)
    pointsFile.close()
if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0')
