import vpython
import numpy
import math

# Zmienne
# fi1, fi2, fi3
fi1 = 0
fi2 = 0
fi3 = 0

# Stale - dlugosc ramion
# L1, L2, L3
l1 = 8
l2 = 13
l3 = 12.5

# Poczatkowa pozycja ramienia robota w przestrzeni roboczej
position_x = 0
position_y = 8
position_z = 4

input_x : vpython.winput = None
input_y : vpython.winput = None
input_z : vpython.winput = None

input_x_plus = None
input_x_minus = None

slider1 = None
slider2 = None
slider3 = None

podloga : vpython.box = None

working_space : vpython.cylinder = None
working_space_radius = 6
working_space_height = 11

arrow_x : vpython.arrow = None
arrow_y : vpython.arrow = None
arrow_z : vpython.arrow = None

napis_arrow_x : vpython.text = None
napis_arrow_z : vpython.text = None
error_message = None

r1 : vpython.cylinder = None
r2 : vpython.cylinder = None
r3 : vpython.cylinder = None

def drawMeARobot(scene):
    
# Inicjalizacja oraz rysowanie sceny i osi wspolrzednych
    
# Modyfikacja położenia kamery

    scene.camera.pos = vpython.vector(0, 0, 8)
    
    global podloga
    podloga = vpython.box(pos=vpython.vector(0, 0, 0), length=20, height=0, width=20)
    global arrow_x
    arrow_x = vpython.arrow(pos=vpython.vector(0,0,0), axis=vpython.vector(3,0,0), shaftwidth=0, opacity=0.6)
    global arrow_y
    arrow_y = vpython.arrow(pos=vpython.vector(0,0,0), axis=vpython.vector(0,3,0), shaftwidth=0, opacity=0.6)
    global arrow_z
    arrow_z = vpython.arrow(pos=vpython.vector(0,0,0), axis=vpython.vector(0,0,3), shaftwidth=0, opacity=0.6)
    
    global napis_arrow_y
    napis_arrow_y = vpython.text(pos=vpython.vector(3.1,0,0), axis=vpython.vector(0,0,0.02), text='y',align='center', color=vpython.color.white, up=vpython.vector(0,0,-1))
    global napis_arrow_x
    napis_arrow_x = vpython.text(pos=vpython.vector(0,0,3.4), axis=vpython.vector(0,0,0.02), text='x',align='center', color=vpython.color.white, up=vpython.vector(0,0,-1))
    
# Inicjalizacja oraz rysowanie przestrzeni roboczej
    
    global working_space
    working_space = vpython.cylinder(pos=vpython.vector(0, 0, 0), axis=vpython.vector(0, working_space_height, 0), radius=working_space_radius, opacity=0.3)
    
# Inicjalizacja oraz rysowanie ramienia robota RRR (trzy segmenty)
    
    global r1
    r1 = vpython.cylinder(pos=vpython.vector(0, 0, 0), axis=vpython.vector(0, l1, 0), radius=0.5)
    global r2
    r2 = vpython.cylinder(pos=vpython.vector(0, l1, 0), axis=vpython.vector(l2, 0, 0), radius=0.5)
    global r3
    r3 = vpython.cylinder(pos=vpython.vector(l2, l1, 0), axis=vpython.vector(l3, 0, 0), radius=0.5)
    
# Pokolorowanie poszczegolnych elementow
    
    podloga.color = vpython.color.white
    working_space.color = vpython.color.white
    r1.color = vpython.color.red
    r2.color = vpython.color.blue
    r3.color = vpython.color.green

# Kinematyka prosta

def Update_position_by_angle():
    
# Aktualizacja R2 - pozycja jest taka sama kąt się zmienia

    r2_angle = vpython.vector(math.cos(fi1) * math.cos(fi2) * l2, 
                                math.sin(fi2) * l2 , 
                                math.sin(fi1) * math.cos(fi2) * l2)
    r2.axis = r2_angle

# Aktualizacja R3 - pozycja i kąt się zmieniają

    r3_pos = vpython.vector(math.cos(fi1) * math.cos(fi2) * l2,
                            math.sin(fi2) * l2 + l1 ,
                            math.sin(fi1) * math.cos(fi2) * l2)
    r3_angle = vpython.vector(math.cos(fi1) * math.cos(fi3 + fi2) * l3,
                              math.sin(fi3 + fi2) * l3 ,
                              math.sin(fi1) * math.cos(fi3 + fi2) * l3)

    r3.pos = r3_pos
    r3.axis = r3_angle

# Kinematyka odwrotna

def Update_displayed_xyz():
    global position_z
    position_z = math.sin(fi2) * l2 + l1 + math.sin(fi2 + fi3) * l3
    global position_y
    position_y = math.cos(fi1) * math.cos(fi2) * l2 + math.cos(fi1) * math.cos(fi2 + fi3) * l3
    global position_x
    position_x = math.sin(fi1) * math.cos(fi2) * l2 + math.sin(fi1) * math.cos(fi2 + fi3) * l3

    global input_x
    input_x.text = position_x
    global input_y
    input_y.text = position_y
    global input_z
    input_z.text = position_z

    Update_checkError()

def Update_angles_based_on_xyz():
    r = math.sqrt(math.pow(position_x,2) + math.pow(position_y,2))
    phi = math.atan2(position_x, position_y)

    global fi3
    global fi2
    global fi1
    fi3 = - math.acos((math.pow(r,2) + math.pow(position_z - l1,2) - math.pow(l2, 2) - math.pow(l3, 2)) / (2*l2*l3))
    fi2 = math.atan2(position_z - l1, r) - math.atan2(l3 * math.sin(fi3), l2 + l3 * math.cos(fi3))
    fi1 = phi

    Update_displayed_xyz()
    Update_position_by_angle()
    Update_fi()

# Wyswietlanie informacji o tym, czy ramie robota pracuje w przestrzeni roboczej

def Update_checkError():
    global position_x
    global position_y
    global position_z
    r = math.sqrt( math.pow(position_x,2) + math.pow(position_y,2) )
    h = position_z

    global error_message
    if (r > working_space_radius or h > working_space_height or h < 0):
        error_message.text = "Wykroczenie poza obszar roboczy"
    else:
        error_message.text = "Praca w obszarze roboczym"

# Suwaki zmieniajace nastawy fi1, fi2, fi3

def Update_fi():
    global slider1
    slider1.value = fi1/(2*math.pi)
    global slider2
    slider2.value = fi1/math.pi + 0.5
    global slider3
    slider3.value = fi1/math.pi + 0.5

# Zdefiniowanie maksymalnego zakresu obrotu podstawy (pierwszy element robota RRR): 0 - 2pi
# Printowanie w konsoli informacji o zmianie kata fi1
    
def R1_change_angle(s):
    global fi1
    fi1 = s.value * 2 * math.pi
    Update_position_by_angle()
    Update_displayed_xyz()
    print("Debug - zmieniono fi1: ", s.value)

# Zdefiniowanie maksymalnego zakresu obrotu ramienia (drugi element robota RRR): - pi/2 - pi/2
# Printowanie w konsoli informacji o zmianie kata fi2
    
def R2_change_angle(s):
    global fi2
    fi2 = s.value * math.pi
    Update_position_by_angle()
    Update_displayed_xyz()
    print("Debug - zmieniono fi2: ", s.value)

# Zdefiniowanie maksymalnego zakresu obrotu przedramienia (trzeci element robota RRR): - pi/2 - pi/2
# Printowanie w konsoli informacji o zmianie kata fi3
    
def R3_change_angle(s):
    global fi3
    fi3 = (s.value - 0.5) * math.pi
    Update_position_by_angle()
    Update_displayed_xyz()
    print("Debug - zmieniono fi3: ", s.value)

def change_x(s):
    print(s.value)
def change_y(s):
    print(s.value)
def change_z(s):
    print(s.value)

# Zdefiniowanie zakresu skoku zmiany poszczegolnych wspolrzednych pozycji robota

def change_x_plus():
    global position_x
    position_x = position_x + 0.1
    Update_angles_based_on_xyz()

def change_x_minus():
    global position_x
    position_x = position_x - 0.1
    Update_angles_based_on_xyz()

def change_y_plus():
    global position_y
    position_y = position_y + 0.1
    Update_angles_based_on_xyz()

def change_y_minus():
    global position_y
    position_y = position_y - 0.1
    Update_angles_based_on_xyz()

def change_z_plus():
    global position_z
    position_z = position_z + 0.1
    Update_angles_based_on_xyz()

def change_z_minus():
    global position_z
    position_z = position_z - 0.1
    Update_angles_based_on_xyz()

def errorMessageDummyBind():
    
    return
    Update_angles_based_on_xyz()
    
# Rozmieszczenie oraz zdefiniowanie poszczegolnych elemntow GUI (informacja o tym, czy robot pracuje w przestrzeni roboczej; suwaki; przyciski)
    
def DrawMeAInput(scene):
    
# Z paska otrzymujemy wartość kata od 0 do 1.

    global error_message
    scene.append_to_caption('\n\n')
    error_message = vpython.wtext(bind=errorMessageDummyBind)
    error_message.text = "Poza zakresem"
    scene.append_to_caption('\n\n')

    global slider1
    scene.append_to_caption('\n\n Nastawa fi_1')
    slider1 = vpython.slider(bind=R1_change_angle)

    global slider2
    scene.append_to_caption('\n\n Nastawa fi_2')
    slider2 = vpython.slider(bind=R2_change_angle)
    slider2.value = 0.5

    global slider3
    scene.append_to_caption('\n\n Nastawa fi_3')
    slider3 = vpython.slider(bind=R3_change_angle)
    slider3.value = 0.5

    global input_x
    scene.append_to_caption('\n\n x')
    input_x = vpython.winput( bind=change_x )
    input_x.text = position_x
    input_x_plus = vpython.button( bind=change_x_plus, text="+" )
    input_x_minus = vpython.button( bind=change_x_minus, text="-" )

    global input_y
    scene.append_to_caption('\n\n y')
    input_y = vpython.winput( bind=change_x )
    input_y.text = position_y
    input_y_plus = vpython.button( bind=change_y_plus, text="+" )
    input_y_minus = vpython.button( bind=change_y_minus, text="-" )

    global input_z
    scene.append_to_caption('\n\n z')
    input_z = vpython.winput( bind=change_z )
    input_z.text = position_z
    input_z_plus = vpython.button( bind=change_z_plus, text="+" )
    input_z_minus = vpython.button( bind=change_z_minus, text="-" )

def main():
    scene = vpython.canvas()

    print("DEBUG: 1 - Drawing a robot")
    drawMeARobot(scene)
    print("DEBUG: 2 - Drawing input methods")
    DrawMeAInput(scene)


if __name__ == "__main__":
    main()
