import random
import extra_functions.color as color


def banner():
    r = random.random()
    if r > 0.5:
        draw1()
    else:
        draw3()
    print("""\n Authors: Josue Encinar & Antonio Marcos
   >>> Conceived by Pablo Gonzalez \n""")

def draw1():
    print("""
          xx                  xx
         xxxx                xxxx
         xxxxx              xxxxx
         xxxxxxx         xxxxxxx
        xxxxxxxxxxx    xxxxxxxxxxx
         xx    xxxxxxxxxxxx    xx
                %s
                xxxxxxxxx
               xxxx   xxxxx
           xxxxxxx      xxxxxxx
         xxxxxxx          xxxxxxx
        xxxxxxx            xxxxxxx
         xxxxxx            xxxxxx
           xx                xx
    """ %(color.RED + "__BoomER_" + color.RESET))

def draw3():
    print("""
        
         ▌▌  ▄▌▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
      ▄▄██▌█   --- %s ---                   
   ▄▄▄▌|·█▌█ 
   ████ ██▌▌          _%s_              
   ███████▌█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌  ~~~
   ▀(·)▀▀▀▀▀▀▀(·)(·)▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀(·)▀▀▀ ~~~
--------------------------------------------------
    """%(color.YELLOW + "L0c4l Expl0iting" + color.RESET, color.RED + "BoomER" + color.RESET ))
