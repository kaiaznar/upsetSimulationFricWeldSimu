## Automatically adapted for numpy.oldnumeric Feb 23, 2010 by upgradeScript.pyc

# utility functions


##
## Replace the geometry for a part with a boundary based
## on the deformed configuration of the part instance in
## an earlier job
##

tolerance = 1.e-8

def updateGeometry(partName,instanceName,odbFileName,featureAngle):
    from abaqus import *
    from part import *
    import abaqus
    model=mdb.models['Model-1']
    deformed = model.PartFromOdb(name='orphan',
                                 fileName=odbFileName,
                                 instance=instanceName,
                                 shape=DEFORMED,
                                 twist=ON)
    try:
	p1 = model.Part2DGeomFrom2DMesh(name=partName,
                                        part=deformed,
                                        featureAngle=featureAngle,
                                        twist=ON)
    except:
	#
	# Assume failure means the feature angle is too big
	# and results in an invalid part
	#
	print "Trying a feature angle of ",featureAngle/2
	try:
	    p1 = model.Part2DGeomFrom2DMesh(name=partName,
                                            part=deformed,
                                            featureAngle=featureAngle/2,
                                            twist=ON)
	except:
	    print "Trying a feature angle of ",featureAngle/4
	    try:
		p1 = model.Part2DGeomFrom2DMesh(name=partName,
                                                part=deformed,
                                                featureAngle=featureAngle/4,
                                                twist=ON)
	    except:
		print "Trying a feature angle of ",featureAngle/8
		try:
		    p1 = model.Part2DGeomFrom2DMesh(name=partName,
                                                    part=deformed,
                                                    featureAngle=featureAngle/8,
                                                    twist=ON)
		except:
		    print "Trying a feature angle of ",0
		    try:
			p1 = model.Part2DGeomFrom2DMesh(name=partName,
                                                        part=deformed,
                                                        featureAngle=0,
                                                        twist=ON)
		    except:
			pass

##
## Return the block location of the first occurence a keyword in the input file
##
def whereIsBlock(keyword):
    from abaqus import *
    blocks = mdb.models['Model-1'].keywordBlock.sieBlocks
    for i in range(len(blocks)):
         b=blocks[i]
         if b[:len(keyword)] == keyword:
             break
    return i

##
## Return the block location of the last occurence a keyword in the input file
##
def whereIsLastBlock(keyword):
    from abaqus import *
    blocks = mdb.models['Model-1'].keywordBlock.sieBlocks
    for i in range(len(blocks)):
         b=blocks[i]
         if b[:len(keyword)] == keyword:
             blockFound = i
    return blockFound

##
## Assign a set to the ref point on a
## part instance
##
def refSet(instanceName,setName):
    from abaqus import *
    from part import *
    import abaqus
    a = mdb.models['Model-1'].rootAssembly
    r = a.instances[instanceName].referencePoints
    featureId = r.keys()[0]
    refPoint=(r[featureId], )
    a.Set(referencePoints=refPoint, name=setName)

##
## Assign an edge set to the highest (greatest y) edge on a
## part instance
##
def highestEdgeSet(instanceName,setName):
    from abaqus import *
    from part import *
    import abaqus
    a = mdb.models['Model-1'].rootAssembly
    e = a.instances[instanceName].edges
    highestLocation = -99999
    sideEdge = []
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if y > highestLocation:
	    highestLocation = y
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if abs(y-highestLocation) < tolerance:
	    sideEdge.append(e[k:k+1])
    a.Set(edges=sideEdge, name=setName)

##
## Assign a surface to the highest (greatest y) edge on a
## part instance
##
def highestSurface(instanceName,surfaceName):
    from abaqus import *
    from part import *
    import abaqus
    a = mdb.models['Model-1'].rootAssembly
    e = a.instances[instanceName].edges
    highestLocation = -99999
    sideEdge = []
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if y > highestLocation:
	    highestLocation = y
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if abs(y-highestLocation) < tolerance:
	    sideEdge.append(e[k:k+1])
    a.Surface(side1Edges=sideEdge, name=surfaceName)

##
## Assign a surface to the perimeter of a part instance
##
def perimeterSurface(instanceName,surfaceName):
    from abaqus import *
    from part import *
    import abaqus
    a = mdb.models['Model-1'].rootAssembly
    e = a.instances[instanceName].edges
    sideEdges = e[0:len(e)]
    a.Surface(side1Edges=sideEdges, name=surfaceName)


##
## Assign an edge set to the lowest (lowest y) edge on a
## part instance
##
def lowestEdgeSet(a,instanceName,setName):
    from abaqus import *
    e = a.instances[instanceName].edges
    lowestLocation = 99999
    sideEdge = []
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if y < lowestLocation:
	    lowestLocation = y
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if abs(y-lowestLocation) < tolerance:
	    sideEdge.append(e[k:k+1])
    a.Set(edges=sideEdge, name=setName)


def openLogFile(name):
    from sys import *
    import osutils
    try:
	osutils.remove(name + "_simulation.log")
    except:
	pass
    logFile = open(name + "_simulation.log",'w')
    return logFile

def appendLogFile(name):
    from sys import *
    import osutils
    logFile = open(name + "_simulation.log",'a')
    return logFile

def writeHeading(logFile):
    from sys import *
    logFile.write('******************************************\n')
    logFile.write('*** Weld simulation job log           ****\n')
    logFile.write('******************************************\n')
    logFile.write(' \n')
    logFile.flush()

def writeRestartHeading(logFile,remeshNumber):
    from sys import *
    timeStamp(logFile)
    logFile.write('\n')
    logFile.write('*** Restarting the simulation         ****\n')
    logFile.write('*** with remesh ' + '%i' % (remeshNumber+1) + '\n')
    logFile.write('\n')
    logFile.flush()

def writeEnding(logFile):
    from sys import *
    logFile.write(' \n')
    logFile.write(' \n')
    logFile.write('******************************************\n')
    logFile.write('*** Weld simulation complete          ****\n')
    logFile.write('******************************************\n')
    logFile.flush()

def writeRestartHeading(logFile,remeshNumber):
    from sys import *
    timeStamp(logFile)
    logFile.write('\n')
    logFile.write('*** Restarting the simulation         ****\n')
    logFile.write('*** with remesh ' + '%i' % (remeshNumber+1) + '\n')
    logFile.write('\n')
    logFile.flush()

##
## Determine simulation time up to now in a restart situation
##
def accumulatedTime(primaryJobName):
    import os
    f = open(primaryJobName+"_simulation.log","r")
    a = ""
    for line in f.readlines():
       if 'total simulation time' in line:
          a = line.replace('total simulation time elapsed     =','')
#        if regex.search('total simulation time',line) != -1:
#           a = regsub.gsub('total simulation time elapsed     =','',line)
    f.close()
    return float(a[0])

def writeModelInfo(logFile,name,timeRemaining,remeshNumber):
    from sys import *
    timeStamp(logFile)
    if remeshNumber > 0:
	logFile.write('Remesh ' + '%g' % remeshNumber + '\n')
    logFile.write('Running job ' + name + '\n')
    logFile.write('for an attempted duration of ' + '%g' % timeRemaining + '\n')
    logFile.flush()

def writeAnalysisInfo(logFile,name,totalTime,timeRemaining):
    from sys import *
    timeStamp(logFile)
    logFile.write('Completed job ' + name + '\n')
    logFile.write('\n')
    logFile.write('flywheel velocity                 = ' + 
		  '%g' % currentFlywheelVelocity(name) + '\n')
    logFile.write('\n')
    elapsed = elapsedTime(name)
    increments = numberOfIncrements(name)
    iterations = numberOfIterations(name)
    logFile.write('simulation time elapsed           = ' + '%g' % elapsed + '\n')
    logFile.write('total simulation time elapsed     = ' + '%g' % totalTime + '\n')
    logFile.write('simulation time remaining         = ' + '%g' % timeRemaining + '\n')
    logFile.flush()

def timeStamp(logFile):
    from sys import *
    import time
    logFile.write(' \n')
    logFile.write(' >>>>> ' + time.ctime(time.time()) + '\n')
    logFile.write(' \n')

##
## Search msg file
##
def searchMsgFile(jobName,searchStr,beginLoc,endLoc):
    import os
    a = "0"
    try:
        f = open(jobName+".msg","r")
    except:
        return 0
    for line in f.readlines():
        if searchStr in line:
          a = line[beginLoc:endLoc]
    f.close()
    return float(a)

##
## Determine the elapsed time for a job
##
def elapsedTime(jobName):
    return  searchMsgFile(jobName,"STEP TIME COM",22,36)

##
## Determine the number of increments for a job
##
def numberOfIncrements(jobName):
    import os
    a = "0"
    try:
        f = open(jobName+".msg","r")
    except:
        return 0
    for line in f.readlines():
        if 'TOTAL OF' in line and 'INCREMENT' in line:
          a = line[15:25]
    f.close()
    return float(a)

##
## Determine the number of iterations for a job
##
def numberOfIterations(jobName):
    import os
    a = '0'
    try:
        f = open(jobName+".msg","r")
    except:
        return 0
    for line in f.readlines():
        if 'PASSES' in line:
          a = line[15:25]
    f.close()
    print "Total number of iterations:", a
    return float(a)

##
## Determine the flywheel velocity at the end of a job
## -
def currentFlywheelVelocity(jobName):
    return  searchMsgFile(jobName,'FLYWHEEL VELOCITY',29,41)

##
## Determine the wallclock time
## -
def wallClockTime(jobName):
    return  searchMsgFile(jobName,'WALLCLOCK TIME',32,42)

##
## Determine if a restart can be made
## -
def restartAvailable(primaryJobName):
    import os
    try:
        f = open(primaryJobName+"_simulation.log","r")
    except:
        return 0
    a = " "
    for line in f.readlines():
        if 'Remesh' in line:
            a = line.replace('Remesh','')
    f.close()
    
    try:
	remeshNumber = int(a)
    except:
	remeshNumber = 0

    if remeshNumber > 0:
	remeshJobName = primaryJobName + "_remesh_" + '%i' % remeshNumber
        searchString = 'Completed job ' + remeshJobName
        f = open(primaryJobName+"_simulation.log","r")
        found = 0
        for line in f.readlines():
            if searchString in line:
             found = 1
        if not found:
           remeshNumber = remeshNumber + 1 
        f.close()
	remeshJobName = primaryJobName + "_remesh_" + '%i' % remeshNumber
	if not os.path.exists(remeshJobName + ".res"):
	    remeshNumber = 0
	if not os.path.exists(remeshJobName + ".odb"):
	    remeshNumber = 0
	if not os.path.exists(remeshJobName + ".mdl"):
	    remeshNumber = 0
	if not os.path.exists(remeshJobName + ".stt"):
	    remeshNumber = 0

    return remeshNumber
    
##
## Determine simulation time up to now in a restart situation
## -
def accumulatedTime(primaryJobName):
    import os
    f = open(primaryJobName+"_simulation.log","r")
    a = "0"
    for line in f.readlines():
        if 'total simulation time' in line:
            a = line.replace('total simulation time elapsed     =','')
    f.close()
    return float(a)

##
## Determine the name of the new job
##
def newJobName(referenceName,remeshNumber):
    return referenceName + "_remesh_" + '%i' % remeshNumber
    
##
## Determine the name of the prior-model ODB
##
def priorJobName(referenceName,remeshNumber):
    ancestorResultsName = referenceName
    if remeshNumber > 1:
	priorRemesh = remeshNumber - 1
	ancestorResultsName = referenceName + "_remesh_" + '%i' % priorRemesh
    ancestorResultsName = ancestorResultsName
    return ancestorResultsName
    

##
## Clean up old files
## -
def cleanupOldFiles(logFile,referenceName,remeshNumber):
    if remeshNumber > 1:
	import osutils
	grandfatherJobName = referenceName
	if remeshNumber > 2:
	    priorPriorRemesh = remeshNumber - 2
	    grandfatherJobName = referenceName + "_remesh_" + '%i' % priorPriorRemesh
        logFile.write('Remove old files of ' +grandfatherJobName + '\n')
	try:
	    osutils.remove(grandfatherJobName + ".stt")
	except:
	    pass
	try:
	    osutils.remove(grandfatherJobName + ".mdl")
	except:
	    pass
	try:
	    osutils.remove(grandfatherJobName + ".size")
	except:
	    pass
	try:
	    osutils.remove(grandfatherJobName + ".ipm")
	except:
	    pass
	try:
	    osutils.remove(grandfatherJobName + ".stt")
	except:
	    pass
	try:
	    osutils.remove(grandfatherJobName + ".res")
	except:
	    pass
	try:
	    osutils.remove(grandfatherJobName + ".dat")
	except:
	    pass
	try:
	    osutils.remove(grandfatherJobName + ".prt")
	except:
	    pass
	try:
	    osutils.remove(grandfatherJobName + ".msg")
	except:
	    pass
	try:
	    osutils.remove(grandfatherJobName + ".jnl")
	except:
	    pass
	try:
	    osutils.remove(grandfatherJobName + ".lck")
	except:
	    pass
    
##
## Create a graphic of the deformed configuration
## -
def plotShape(jobName):
    from abaqus import *
    from visualization import *
    odbname = jobName + '.odb'
    o = session.openOdb(odbname)
    session.viewports['Viewport: 1'].setValues(displayedObject=o)
    frames_in_step=o.steps['Weld step'].frames
    scratchOdb = session.ScratchOdb(odb=o)
    session.viewports['Viewport: 1'].setValues(displayedObject=o)
    try:
        sessionStep = scratchOdb.Step(name='Session Step', 
                                      description='Step for Viewer non-persistent fields', domain=TIME, 
                                      timePeriod=1.0)
    except:
        sessionStep = scratchOdb.steps['Session Step']
    finalFrame = o.steps['Weld step'].getFrame(100.0)
    s0f2_ACYIELD=finalFrame.fieldOutputs['AC YIELD']
    tmpField_ACYIELD = s0f2_ACYIELD
    s0f2_NT11=finalFrame.fieldOutputs['NT11']
    tmpField_NT11 = s0f2_NT11
    s0f2_PEEQ=finalFrame.fieldOutputs['PEEQ']
    tmpField_PEEQ = s0f2_PEEQ
    s0f2_S=finalFrame.fieldOutputs['S']
    tmpField_S = s0f2_S
    s0f2_U=finalFrame.fieldOutputs['U']
    tmpField_U = s0f2_U
    reservedFrame = sessionStep.Frame(frameId=0, frameValue=0.0, 
                                      description='Session Frame')
    sessionFrame = sessionStep.Frame(frameId=1, frameValue=0.0, 
                                     description='The sum of values over all selected frames')
    sessionField = sessionFrame.FieldOutput(name='NT11', 
                                            description='Nodal temperature', field=tmpField_NT11)
    sessionField = sessionFrame.FieldOutput(name='PEEQ', 
                                            description='Equivalent plastic strain', field=tmpField_PEEQ)
    sessionField = sessionFrame.FieldOutput(name='U', 
                                            description='Spatial displacement', field=tmpField_U)
    frame1 = session.scratchOdbs[odbname].steps['Session Step'].frames[1]
    session.viewports['Viewport: 1'].odbDisplay.setFrame(frame=frame1)
    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
        variableLabel='NT11', outputPosition=NODAL)
    session.viewports['Viewport: 1'].setValues(displayedObject=o)
#    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
#        DEFORMED, ))
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=118.348, 
                                                    farPlane=156.96,
                                                    width=61.694,
                                                    height=36.3733,
                                                    viewOffsetX=16.7469, 
                                                    viewOffsetY=-2.23545)
    session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(triad=OFF, 
                                                                         legend=OFF,
                                                                         title=OFF,
                                                                         state=OFF,
                                                                         annotations=OFF,
                                                                         compass=OFF)
    session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
        maxAutoCompute=OFF, maxValue=1300, minAutoCompute=OFF, minValue=0)
    session.printOptions.setValues(rendition=COLOR, vpDecorations=OFF, 
				   vpBackground=OFF)
    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
        variableLabel='NT11', outputPosition=NODAL)
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
        CONTOURS_ON_DEF, ))
    session.viewports['Viewport: 1'].setValues(width=95.3125)
    session.viewports['Viewport: 1'].setValues(origin=(0.0, -27.8125), 
                                               height=208.125)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=142.859, 
    farPlane=219.367, width=15.8049, height=34.0207, viewOffsetX=16.4369, 
    viewOffsetY=-0.157545)
    session.printToFile(fileName=jobName + '.png', format=PNG, canvasObjects=(
	session.viewports['Viewport: 1'], ))
    session.printToFile('latest.png', format=PNG, canvasObjects=(
	session.viewports['Viewport: 1'], ))
    session.viewports['Viewport: 1'].maximize()
    o.close()
    

##
## Apply seeds within a specified y-distance from zero
##
def seedNearZero(instanceName,elementSize,distance):
    from abaqus import *
    from assembly import *
    from mesh import *
    assembly = mdb.models['Model-1'].rootAssembly
    e = assembly.instances[instanceName].edges
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if (abs(y) <= distance):
	    edges = (e[k],)
	    assembly.seedEdgeBySize(edges=edges, size=elementSize)


##
## Delete all edge seeds
##
def removeEdgeSeeds(instanceName):
    from abaqus import *
    from assembly import *
    assembly = mdb.models['Model-1'].rootAssembly
    e = assembly.instances[instanceName].edges
    for k in range(len(e)):
	assembly.deleteSeeds(regions=(e[k],))

##
## Partition an upper part while trying to avoid existing vertices
## + -
def sliceTopInstance(instanceName,cutPosition):
    from abaqus import *
    from assembly import *
    from part import *
    a = mdb.models['Model-1'].rootAssembly
	#-
    execfile('inertiaweld_job_param.py')
    #
    # Move the cut position to avoid cutting too near an existing vertex
    while nearestVertexDistance(cutPosition,instanceName) < nearWeldMeshSize:
	cutPosition = cutPosition + nearWeldMeshSize/10.
    a.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=cutPosition)
    d1 = a.datums
    datumList = d1.keys()
    datumList.sort()
    thisPlane = datumList[len(datumList)-1]
    f = a.instances[instanceName].faces
    faceLength = len(f)
    for j in range(faceLength):
	try:
	    a.PartitionFaceByDatumPlane(faces=f[j], datumPlane=d1[thisPlane])
	    a.regenerate()
	except:
	    pass
    return cutPosition

##
## Partition a lower part while trying to avoid existing vertices
## + -
def sliceBottomInstance(instanceName,cutPosition):
    from abaqus import *
    from assembly import *
    from part import *
    a = mdb.models['Model-1'].rootAssembly
	# -
    execfile('inertiaweld_job_param.py')
    #
    # Move the cut position to avoid cutting too near an existing vertex
    while nearestVertexDistance(cutPosition,instanceName) < nearWeldMeshSize:
	cutPosition = cutPosition - nearWeldMeshSize/10.
    a.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=cutPosition)
    d1 = a.datums
    datumList = d1.keys()
    datumList.sort()
    thisPlane = datumList[len(datumList)-1]
    f = a.instances[instanceName].faces
    faceLength = len(f)
    for j in range(faceLength):
	try:
	    a.PartitionFaceByDatumPlane(faces=f[j], datumPlane=d1[thisPlane])
	    a.regenerate()
	except:
	    pass
    return cutPosition

##
## Create a surface comprised of edges near the top of a part
##
def surfaceNearTop(instanceName,surfaceName,distance):
    from abaqus import *
    from assembly import *
    #
    # Note: This isn't useful for defining contact surfaces
    # since it will pick up internal edges generally
    # 
    assembly = mdb.models['Model-1'].rootAssembly
    e = assembly.instances[instanceName].edges
    sideEdges = []
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if (y >= distance):
	    sideEdges.append(e[k:k+1])
    assembly.GeometrySurface(name=surfaceName, geometrySurfaceSeq=((sideEdges, SIDE1), ))
##
## Create a surface comprised of edges near the bottom of a part
##
def surfaceNearBottom(instanceName,surfaceName,distance):
    from abaqus import *
    from assembly import *
    #
    # Note: This isn't useful for definining contact surfaces
    # since it will pick up internal edges generally
    # 
    assembly = mdb.models['Model-1'].rootAssembly
    e = assembly.instances[instanceName].edges
    sideEdges = []
    for k in range(len(e)):
	((x,y,z),) = e[k].pointOn
	if (y <= distance):
	    sideEdges.append(e[k:k+1])
    assembly.GeometrySurface(name=surfaceName, geometrySurfaceSeq=((sideEdges, SIDE1), ))

##
## Return the elevation difference to the nearest vertex
##
def nearestVertexDistance(position,instanceName):
    from abaqus import *
    from assembly import *
    a = mdb.models['Model-1'].rootAssembly
    v = a.instances[instanceName].vertices
    nearestDistance = 99999
    for k in range(len(v)):
	((x,y,z),) = v[k].pointOn
	distance = abs(position-y)
	if distance < nearestDistance:
	    nearestDistance = distance
    return nearestDistance

#
# Add U displacement field without rotation angle to ODB
# with a new field name UNEW in ODB
#
def add_unew_odb(odbName):

    from odbAccess import *
    import sys, numpy.oldnumeric as Numeric
    from textRepr import prettyPrint

    odb = openOdb(odbName + ".odb")

    for step in odb.steps.values():
        for frame in step.frames:
            try:
                frame.FieldOutput(name='UNEW', field=frame.fieldOutputs['U'])
            except KeyError:
                pass
