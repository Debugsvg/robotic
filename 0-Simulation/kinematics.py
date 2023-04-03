import math
from constants import *

# Dimensions used for the PhantomX robot :
#constL1 = 54.8
#constL2 = 65.3
#constL3 = 133
#theta2Correction = 0  # A completer
#theta3Correction = 0  # A completer

# Dimensions used for the simple arm simulation
# bx = 0.07
# bz = 0.25
# constL1 = 0.085
# constL2 = 0.18
# constL3 = 0.250


# cette fonction permet d'utiliser le théoréme d'alkashi  

def alkashi(a, b,c,sing =1):
    if a * b == 0:
        print("La produit est null car A ou B est null")
        return 0
    return sing * math.acos(min(1,max(-1,(a ** 2 + b ** 2 - c ** 2) / (2 * a * b))))


# cette fontion n'est autre qu'une autre forme d'alkashi 

def alkashi2(a,b , thehta,sing=- 1):
    if a * b == 0:
        print("Le produit est null car A ou B est null")
        return 0
    return sing * math.sqrt(a ** 2 + b ** 2 + - 2 * a * b * math.cos(thehta))


# fonction computeDK avec les offeset 

def computeDK(theta1, theta2, theta3, l1=constL1, l2=constL2, l3=constL3):
    # A completer
    #offsetthehta2 = theta1 / (360/(2*math.pi)) 
    #offsetthehta3 = theta1 / (360/(2*math.pi)) 
    #offsetthehta2  = 16
    #offsetthehta3  = 43.76
    
    #theta1 = theta1 / (360/(2*math.pi)) 
    #theta2 = ((theta2- offsetthehta2) / (360/(2*math.pi)) ) 
    #theta3 = ((theta3 - offsetthehta3) / (360/(2*math.pi)) )
    
    x = ((l1 + l2 * math.cos(theta2) + l3 * math.cos(theta2 + theta3)) * math.cos(theta1)) 
    y = ((l1 + l2 * math.cos(theta2) + l3 * math.cos(theta2 + theta3)) * math.sin(theta1))
    z = (-(l3 * math.sin(theta2 + theta3) + l2 * math.sin(theta2)) ) 
    #print(x , y , z)
    
    return [x, y, z]



# La fonction computeIk permet de calculer les angles des servomoteurs
# a partir du point de la patte 
# voir la fiche calcul exam 




def computeIK(x, y, z, l1=constL1, l2=constL2, l3=constL3):

    d13 = (math.sqrt((x * x) + (y * y))) -l1
    d = (math.sqrt((z * z)+ (d13 * d13)))

    theta1 = math.atan2(y,x)
    theta2 = (math.atan2(-z , d13)) + alkashi(l2 , d , l3)
    theta3 = alkashi(l2,l3,d) + math.pi
    
    if d > l2 + l3:
        print ("*erreure")
    elif d < l2 + l3:
        if x == 0 and y == 0 : 
            theta1 = 0 

    return [theta1, theta2, theta3]


# fonction computeDK sans les offset 

def computeDKsimple(theta1, theta2, theta3, l1=constL1, l2=constL2, l3=constL3):
    # A completer
    theta1 = theta1 / (360/(2*math.pi)) 
    theta2 = theta2 / (360/(2*math.pi))
    theta3 = theta3 / (360/(2*math.pi))
    x = (l1 + l2 * math.cos(theta2) + l3 * math.cos(theta2 + theta3)) * math.cos(theta1)
    y = (l1 + l2 * math.cos(theta2) + l3 * math.cos(theta2 + theta3)) * math.sin(theta1)
    z = (l3 * math.sin(theta2 + theta3) + l2 * math.sin(theta2)) 

    return [x, y, z]


# fonction qui permet de dessiner un  cercle avec le simultateur 
# on à besoin de deux paramétres pour tracer une cercle 
# on a besoin de y  qui correspond au rayon du cercle 
# on a besoin de z qui correspond à la hauteur du cercle 

def circle(x,z,r,t,duration):
    position_cercle = (t % 360)
    angle = position_cercle
    dy = math.cos(angle) / 10
    dz = math.sin(angle) / 10 + z
    x = 0.5

    return computeIK(x,dy,dz)


# fonction qui permet de generer un segment à l'écran on a besoins de 
#  de la coordonnées du point en x 
#  de la coordonées du point en y 
#  de la coordonées du point en z 


def segment (x1, y1, z1, x2, y2, z2, t, duration) :
    t = t % duration
    k = t / duration
    x = k * (x2 - x1) + x1
    y = k * (y2 - y1) + y1
    z = k * (z2 - z1) + z1

    #if t > duration:
        #return computeIK(x2, y2, z2)

    return computeIK (x, y, z)


#Fonction qui permet de generer un triangle à l'écran on à besoin de 
# 1 
# 2 
# 3
def triangle (x, z, h, w, t):
    duration = 12
    t = t % duration
    x1 = x
    x2 = x
    x3 = x
    y1 = - w / 2
    y2 = w / 2
    y3 = 0
    z1 = 0
    z2 = 0
    z3 = h + z

    if t <= duration / 3 :
        return segment (x1, y1, z1, x2, y2, z2, t, duration/3)
    elif t <= 2 * (duration / 3) : 
        return segment (x2, y2, z2, x3, y3, z3, t - (duration / 3) , duration/3)
    else:
        return  segment (x3, y3, z3, x1, y1, z1, t - 2*(duration / 3), duration/3)




def main():
    print("Testing the kinematic funtions...")
    print(
        "computeDK(0, 0, 0) = {}".format(
            computeDKsimple(0, 0, 0, l1=constL1, l2=constL2, l3=constL3)
           
        )
    )
    print("")
    print(
        "computeDKsimple(0, 0, 0) = {}".format(
            computeDK(0, 0, 0, l1=constL1, l2=constL2, l3=constL3)
           
        )
    )


if __name__ == "__main__":
    main()

