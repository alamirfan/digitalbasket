#Digital Basket User Interface
import serial
from Tkinter import *

#SMS Imports
import urllib2
import cookielib
from getpass import getpass
import sys
from random import randint

#Create the window
root = Tk()

#Modify root window
root.title("Digital Basket GUI")
root.geometry("1050x1050")

emp_data=['3B004D69130C','3B004D8FF20B','3B004D6D4C57','3B004D95BE5D','3B004D846E9C','3B004D8A36CA']
products={'3B004DAAF12D':"Flipkart Smartbuy In-Ear Wired Earphone",'3B004D8F29D0':"Rich Club Smart Watch",'3B004D741715':"Rich Club Smart Watch",'3B004DB6DD1D':"Accezory Stylish wallet for Men",'3B004D9805EB':"Kurkure",
   '3B004D69130C':'IRFAN ALAM','3B004D8FF20B':'SUCHITRA SINGH','3B004D6D4C57':'RAKESH KUMAR SAH','3B004D95BE5D':'BIKRANT SINGH THAPA','3B004D846E9C':'Mr PUNEET PALAGI','3B004D8A36CA':'Mrs SOJHA RANI'}
quantity={'3B004DAAF12D':"1",'3B004D8F29D0':"1",'3B004D741715':"1",'3B004DB6DD1D':"1",'3B004D9805EB':"1"}
quantityunit={'3B004DAAF12D':"Pc",'3B004D8F29D0':"Pc",'3B004D741715':"Pc",'3B004DB6DD1D':"Pc",'3B004D9805EB':"Pc"}
price={'3B004DAAF12D':"449",'3B004D8F29D0':"1499",'3B004D741715':"1499",'3B004DB6DD1D':"399",'3B004D9805EB':"25"}
mobile={'3B004D69130C':'7411848140','3B004D8FF20B':'9379691899','3B004D6D4C57':'8660114827','3B004D95BE5D':'7259240944','3B004D846E9C':'9844672400'}

#Variables to hold values
r = 2                                   #Row number
Total=0                                 #Grand Total Price
data=["","","","","","","","","",""]    #To hold RFID Tags ID
name=["","","","","","","","","",""]    #To hold name of products matching RFID Tags ID

#Device physical address to read Serial data
ser = serial.Serial("/dev/ttyUSB0",baudrate = 9600,timeout=1)

#Function to read RFID Tags
def read_rfid():
   data = ser.read(12)
   return data

#Digital Basket Green Heading
Label(text="Digital Basket Billing System",font=(None, 25), bg="green").grid(row=0,column=0, columnspan=5)
Label(text="Welcome, Please put item in the basket!", fg="black").grid(row=30,column=0, columnspan=5)


def gui():
    global r               #r is declare above. It should be called as Global variable because it is declared outside the function
    global Total           #Total is declare above. It should be called as Global variable because it is declared outside the function
    id=read_rfid()

    
    if len(id)!=0:         #To check if lenght of the id is not 0.
       
       #Column Title
       Label(text="Product Name", width=0).grid(row=1,column=0)
       Label(text="Unit Price", width=0).grid(row=1,column=1)
       Label(text="Quantity", width=0).grid(row=1,column=2)
       Label(text="Final Price", width=0).grid(row=1,column=3)
       
       if id in data:                                #To check if the scanned RFID ID is present in the data, it PRESENT then REMOVE the items from basket
          r = data.index(id)                         #Getting index of RFID ID in data variable
          data[r]=""                                 #Replacing RFID ID with ""      
          itemname=products[id]                      #Getting item name from products
          itemquantity=quantity[id]                  #Getting item quantity from quantity
          itemquantityunit=quantityunit[id]          #Getting item quantity unit from qtyunit
          itemprice=price[id]                        #Getting item price from price
          
          #If item is already present, reduce the quantity and change the price
          if name.count(itemname) > 1:                                              
             rpos=max(test for test, val in enumerate(name) if val == itemname)     #Getting index of the matching name present in the last
             name[rpos]=""                                                          #Replacing the name with ""
             r = name.index(itemname)                                               #Getting the index of the item for row
             count= name.count(itemname)                                            #Counting the number of item for quantity and price multiplication
             r = r+2                                                                #Adding 2 to rows, because first two rows are busy with Greeting message and column
             
             pname = Entry(root,width=50)                                           #Product name column
             pname.grid(row=r,column=0)
             pname.insert(0,itemname)
             
             uprice = Entry(root,width=20)                                          #Product unit price column
             uprice.grid(row=r,column=1)
             uprice.insert(0,itemprice)
             
             pqty = Entry(root,width=20)                                            #Product quantity column
             pqty.grid(row=r,column=2)
             cqty=int(count)*int(itemquantity)
             pqty.insert(0,str(cqty)+" "+itemquantityunit)
             
             fprice = Entry(root,width=20)                                          #Product final price
             fprice.grid(row=r,column=3)
             fprice.insert(0,int(itemprice)*int(count))
             
             Total=Total-int(price[id])
             
             #Empty Field side to Grand Total
             e = Entry(root)
             e.grid(row=17,column=3,columnspan=2)
             e.insert(0,Total)

             #If item is not present then delete the rows elements
          else:
             r = name.index(itemname)
             name[r]=""
             r = r+2
             
             pname = Entry(root,width=50)
             pname.grid(row=r,column=0)
             pname.delete(0,END)
             
             uprice = Entry(root,width=20)
             uprice.grid(row=r,column=1)
             uprice.delete(0,END)
             
             pqty = Entry(root,width=20)
             pqty.grid(row=r,column=2)
             pqty.delete(0,END)
             
             fprice = Entry(root,width=20)
             fprice.grid(row=r,column=3)
             fprice.delete(0,END)
             
             Total=Total-int(price[id])
             
             #Empty Field side to Grand Total
             e = Entry(root)
             e.grid(row=17,column=3,columnspan=2)
             e.insert(0,Total)
             
          #Digital Basket Green Heading
          action = Label(text="Last Action: Item removed from basket",font=(None, 15), fg="red")
          action.grid(row=30,column=0, columnspan=5)

          #If user scans employee card, then print goodbye message
       elif id in emp_data:

          #SMS System Starts

          #Verify OTP
          def checkotp():
             userotp = otpentry.get()
             uotp = str(userotp)
             gotp = str(otp)
             if uotp == gotp:
                bye = Label(text="OTP Validation Successfull",font=(None, 15), bg="green")
                bye.grid(row=50,column=0, columnspan=5)
                bye = Label(text="Thank you for shopping with us: "+products[id],font=(None, 15), bg="blue")
                bye.grid(row=51,column=0, columnspan=5)
                pay = Label(text="You have made a purchase of Rs: "+str(Total),font=(None, 15), bg="purple")
                pay.grid(row=52,column=0, columnspan=5)

                ser = serial.Serial("/false/dev/ttyUSB0",baudrate = 9600,timeout=1)   #This will show error but will not cause problem

             else:
                bye1 = Label(text="X Wrong OTP. Re Enter X",font=(None, 15), bg="red")
                bye1.grid(row=50,column=0, columnspan=5)

                #Generate and send OTP
          def randnum(n):
             range_start = 10**(n-1)
             range_end = (10**n)-1
             return randint(range_start,range_end)
          otp = randnum(6)
          print(otp)

          username = "7277773073"
          passwd = "M2598Q"
          number = mobile[id]
          message = "Digital Basket Billing System\nYour OTP is: "+str(otp)+"\nOTP valid for 15 minutes. Please enter OTP to validate transaction."
 
          #Logging into the SMS Site
          url = 'http://site24.way2sms.com/Login1.action?'
          logininfo = 'username='+username+'&password='+passwd+'&Submit=Sign+in'
 
          #For Cookies:
          cj = cookielib.CookieJar()
          opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
 
          # Adding Header detail:
          opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')]
 
          try:
             usock = opener.open(url, logininfo)
          except IOError:
             print "Error while logging in."

 
 
          jession_id = str(cj).split('~')[1].split(' ')[0]
          send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
          send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+number+'&message='+message+'&msgLen=136'
          opener.addheaders = [('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
 
          try:
             sms_sent_page = opener.open(send_sms_url,send_sms_data)
          except IOError:
             print "Error while sending message"
    
          print "SMS has been sent."


          

          #OTP Field
          otplable = Label(text="Enter OTP to validate transaction")
          otplable.grid(row=50,column=0,columnspan=5)

          otpentry = Entry(root)
          otpentry.grid(row=51,column=0,columnspan=5)

          otpbutton = Button(root, text="Submit", command=checkotp)
          otpbutton.grid(row=52,column=0,columnspan=5)

          #SMS system Ends

          
       else:
          r = data.index("")
          data[r]=id
          itemname=products[id]
          itemquantity=quantity[id]
          itemquantityunit=quantityunit[id]
          itemprice=price[id]

          #If item is present in name, then increase the quantity and change the price
          if itemname in name:
             pos = name.index("")
             name[pos]=itemname
             r = name.index(itemname)
             count= name.count(itemname)
             r = r+2
             
             pname = Entry(root,width=50)
             pname.grid(row=r,column=0)
             pname.insert(0,itemname)
             
             uprice = Entry(root,width=20)
             uprice.grid(row=r,column=1)
             uprice.insert(0,itemprice)
             
             pqty = Entry(root,width=20)
             pqty.grid(row=r,column=2)
             Item_qssize=int(itemquantity)* int(count)
             pqty.insert(0,str(Item_qssize)+" "+itemquantityunit)
             
             fprice = Entry(root,width=20)
             fprice.grid(row=r,column=3)
             fprice.insert(0,int(itemprice)*int(count))
             
             Total=Total+int(price[id])
             
             #Empty Field side to Grand Total
             e = Entry(root)
             e.grid(row=17,column=3,columnspan=2)
             e.insert(0,Total)

             #If item is not present in name then add the item to row
          else:
            name[r]=itemname
            r = r+2
            
            pname = Entry(root,width=50)
            pname.grid(row=r,column=0)
            pname.insert(0,itemname)
            
            uprice = Entry(root,width=20)
            uprice.grid(row=r,column=1)
            uprice.insert(0,itemprice)
            
            pqty = Entry(root,width=20)
            pqty.grid(row=r,column=2)
            pqty.insert(0,itemquantity+" "+itemquantityunit)
            
            fprice = Entry(root,width=20)
            fprice.grid(row=r,column=3)
            fprice.insert(0,itemprice)
            
            Total=Total+int(price[id])

            #Empty Field side to Grand Total
            e = Entry(root)
            e.grid(row=17,column=3,columnspan=2)
            e.insert(0,Total)
            
          #Grand Total Field
          Label(text="Grand Total",font=(None, 15)).grid(row=17,column=0, columnspan=3)

          #Digital Basket Green Heading
          action = Label(text="Last Action: Item added to basket.........",font=(None, 15), fg="green")
          action.grid(row=30,column=0, columnspan=5)
          
          #Calling the function again and again after 0.5 seconds	
    root.after(500, gui)

    #Calling the function for the first time
gui()

#Main event loop
root.mainloop()

