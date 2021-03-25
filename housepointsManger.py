def modify(to_modify):
    pointread=open(r'House-Data/Points.txt', 'r')
    current_points=pointread.read()
    points=current_points.split(',')
    york_add=int(to_modify[0])-int(to_modify[1])
    tudor_add=int(to_modify[2])-int(to_modify[3])
    lancaster_add=int(to_modify[4])-int(to_modify[5])
    stuart_add=int(to_modify[6])-int(to_modify[7])
    pointread.close()
    print(points)
    york_current=int(points[0])
    tudor_current=int(points[1])
    lancaster_current=int(points[2])
    stuart_current=int(points[3])
    york=york_current+york_add
    lancaster=lancaster_current+lancaster_add
    tudor=tudor_current+tudor_add
    stuart=stuart_add+stuart_current
    to_write=str(york)+','+str(tudor)+','+str(lancaster)+','+str(stuart)
    pointwrite=open(r'House-Data/Points.txt', 'w')
    pointwrite.write(to_write)
    pointwrite.close()
def view():
    pointread=open(r'House-Data/Points.txt', 'r') 
    current_points=pointread.read()
    points=current_points.split(',')
    pointread.close()
    return points
def sort(houseList):
    sortedHouseList = []
    while len(houseList) > 0:
        top = {'points': -999999}
        for house in houseList:
            if house['points'] > top['points']:
                top = house
        sortedHouseList.append(top)
        houseList.remove(top)
    return sortedHouseList
def reset():
    housepoints=open('/home/site/wwwroot/House-Data/Points.txt', 'r')
    points=housepoints.read()
    housepoints.close()
    housepoints=open('/home/site/wwwroot/House-Data/Points.txt', 'w')
    housepoints.write('0,0,0,0')
    housepoints.close()
    housepointsBackup=open('/home/site/wwwroot/House-Data/BackupPoints.txt', 'w')
    housepointsBackup.write(points)
    housepointsBackup.close()
def restore():
    housepointsBackup=open('/home/site/wwwroot/House-Data/BackupPoints.txt', 'r')
    points=housepointsBackup.read()
    housepointsBackup.close()
    housepoints=open('/home/site/wwwroot/House-Data/Points.txt', 'w')
    housepoints.write(points)
    housepoints.close()
def cmd(cmd):
    if cmd == 'house.restore':
        restore()
    elif cmd == 'house.reset':
        reset()
    else:
        return 'UnKnown cmd'