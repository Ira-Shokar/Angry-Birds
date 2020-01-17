import numpy as np #import the fuctions from Numpy and V Python to suppliment our python capablities
from vpython import sphere, color, rate, canvas, vector, curve, label, box, cross, mag, random, local_light, cylinder, ellipsoid, cone

#Input initial object properties  to set the scene.
scene = canvas(width=1000, height=760, center=vector(8,5,0),range=8)
sky = box(pos= vector(10,10,-1), length= 30, height=20, width= 0.5, color=color.cyan)
grass = box(pos= vector(10,0,0), length= 30, height=0.1, width= 20, color=color.green)
ground = box(pos= vector(8,0,0), length= 16, height=0.3, width= 1, color=color.gray(0.5))
sun = sphere(pos=vector(-2.5,10,0),radius= 0.75, color=color.yellow)
light = local_light(pos=vector(100,5,0), color=color.white)
label(pos=vector(3,10,0), text="Hit the Orange Target!", height= 30, color=color.yellow) 

#Input initial properties of the bird.
ball = sphere(pos = vector(0,0.3,0),radius = 0.3, color=color.red) #initial position and nature of the ball.
eye = sphere(pos = vector(0.3,0.6,0.2),radius = 0.1, color=color.white)
pupil= sphere(pos = vector(0.39,0.63,0.3),radius = 0.05, color=color.black)
nose= cone(pos=vector(0.25,0.25,-.050), axis=vector(0.3,-0.05,0),radius=.15, color= color.orange)

#Set random values for the x postions of the target as well as the obstacles, 1 unit =1m.
x1=5*random()+10 #target x value
x2= x1- 2*random()-2 #obstacle 1 x value
x3= x2- 2*random()-2 #obstacle 2 x vlaue

# The random values for the width of the two obstacles, 1 unit =1m.
x4= 3*random() #width of obstacle 1
x5= 3*random() #width of obstacle 2

#The distance between the edge of the obstacles to their centres, 1 unit =1m.
x6= x2- (x2-x4/2) #obstacle 1
x7= x3- (x3-x5/2) #obstacle 2

#The random heights of the obstacles, 1 unit =1m
y1= height=3*random()+3 #height of obstacle 1
y2= height=3*random()+3 #height of obstacle 2

#As the obstacles are half visible, their heights above the groud are, 1 unit =1m:
y1_=y1/2 #visible height of obstacle 1
y2_=y2/2 #visible height of obstacle 2

#The objects to represent the obstacles and the target. 1 unit =1m.
target = box(pos= vector(x1,1,0), length= 0.5, height=2, width= 0.5, color=color.orange)
obstacle1 = ellipsoid(pos= vector(x2,0,0), length= x4, height= y1, width= 0.5, color=color.blue)
obstacle2 = ellipsoid(pos= vector(x3,0,0), length= x5, height= y2, width= 0.5, color=color.magenta)

# Initial parameters
x0= 0 #initial x coordinate, m
y0= 0.6 #initial y coordinate, m
g = 9.81 # gravitational acceleration, m/s^2
t = 0 # initial time, s
dt = 0.00001 # time interval for loop animation, in seconds
hit_tolerance= np.abs(x1-x0) #the difference between the centre of the mass and the target to determine if a collision had taken place.

#Inputs for the user for to obtain the inital angle and velocity of the mass.
dtheta = float(input("Input the initial angle in degrees: ")) 
theta = np.radians(dtheta) #converting input in degrees to radians
v0 = float(input("Input the initial speed in metres/second: "))
vx=v0*np.cos(theta) #Horizontal component of speed of the mass, this stays constant throughout the motion.

#Statement for while the mass is in a certain position range that it will follow the motion outlined.
while (y0>=0) and (x0<=(x1+3)): # loop to animate the mass
    rate(50000)   # restricts animation to 50000 updates per second 
    t= t+dt     #change in time
    x0= v0*t*np.cos(theta)                      # x position of the ball
    y0= v0*t*np.sin(theta) - (0.5*g*(t**2))     # y postion of the ball under gravity
    ball.pos = vector(x0,y0,0)                  # postion of the ball at time t as a vector.
    vy = v0*np.sin(theta)-9.8*t                 # vertical component of speed of the masss at time t
    
    #Positions of the other features of the bird.
    eye.pos = vector(x0+0.16,y0+0.25,0.1)       
    pupil.pos= vector(x0+0.18,y0+0.26,0.2)
    nose.pos= vector(x0+0.25,y0-0.05,-0.05)
    
#To determine whether the target will topple.
    Dx=(x1+0.25)-x0 #the x component of the vector from the point of impact to the centre of rotation
    D= vector(Dx, y0, 0) #the vector from the point of impact to the centre of rotation
    m= 0.1 #mass of object
    deltat= 0.10 # collision time 
    P= vector(m*vx,m*vy, 0) #momentum vector umpon impact.
    F_applied = vector(m*vx/deltat, m*vy/deltat, 0) # equal to momentum vector divided by the contact time of 0.01s
    
    #The applied torque is the cross product of F x D, this only acts in the z direction as it will be perpendicular 
    #to both and this is:
    T_applied= 10*vx*y0- 10*vy*Dx
    #The restoring torque is |F(gravity) x The  base width| = mgw/2, with an arbirtary mass of 30kg asigned. 
    T_restoring=30*9.8*0.5/2
    
    #If statements for of the mass strikes one of the obsticles or fails to strike anything.
    if (x0>=(x1+0.55)) or ((y0<=y2_) and (np.abs(x3-x0)<=x7)) or ((y0<=y1_) and (np.abs(x2-x0)<=x6)) or ((x0<=x1-0.55) and (y0<=0)):
        label(pos=vector(4.5,8,0), text="Try again!", height= 50, color=color.yellow)
        ball.pos = vector(-1,-2,0)
        v0=0

    #Statement for of the mass strikes srikes the target
    elif (np.abs(x1-x0) <= 0.55 and (y0<=2.15)): 
        ball.pos = vector(x0,y0,0)
        
        if T_applied>=T_restoring: #if the applied torque is greater than the restoring torque the target will topple
            label(pos=vector(11,8,0), text="HIT!", height= 50, color=color.yellow)
            label(pos=vector(4.5,8,0), text="Well Done!", height= 50, color=color.yellow)
            ball.pos = vector(x1,0.6,0)
            
            #Positions of the target and the mass after the collison.
            fallen_target= box(pos = vector(x1+1,0.25,0), length= 2, height=0.5, width= 0.2, color=color.orange)
            target.pos = vector(x1,-2,0)
            eye.pos = vector(x1+0.16,0.55,0.1)
            pupil.pos= vector(x1+0.18,0.56,0.2)
            nose.pos= vector(x1+0.25,0.35,-0.05)
            
            #Print statements to indicate properties of the collision.
            print("Height of impact with the target,",y0/10, "m" )
            print("Bird's momentum upon striking the target,",mag(P), "kgm/s")
            print("Torque applied by the brid upon impact,", T_applied/10, "Nm")
            print("Torque applied by the brid upon impact,", 2.4525/10, "Nm")
               
        elif T_applied<=T_restoring: # if the applied torque is not great enough the targer will not topple.
            label(pos=vector(4.5,8,0), text="Try again!", height= 50, color=color.yellow)
            ball.pos = vector(-1,-2,0)
