## these are backend preinstalled tkinter library for the use of design and presentation for project without using frontend
from tkinter import Tk,Label,Frame,Entry,Button,messagebox,simpledialog,filedialog
from tkinter.ttk import Combobox
import time
from PIL import Image,ImageTk
import autotable_creation
import random
import sqlite3
import gmail
import re
from tkintertable import TableCanvas,TableModel

win=Tk()
win.title('My Project')
win.state('zoomed')
win.resizable(width=False,height=False)
win.configure(bg='powder blue')

# it is use for header footer of home page and show the name of project,logo of rupees and current date time of system in this project

header_title=Label(win,text="Banking Automation",font=('arial',50,'bold','underline'),bg='powder blue')
header_title.pack()

current_date=time.strftime('%d-%m-%Y')

header_date=Label(win,text=f'Today:{current_date}',font=('arial',14,'bold'),bg='powder blue',fg='blue')
header_date.pack(pady=10)

footer_title=Label(win,text="By:Ankit Yadav\nEmail:ankit.yadav476711@gmail.com\nMob:7783093597\nProject Guide:Mr.Aditya Kumar",font=('arial',11,'bold','underline'),bg='powder blue')
footer_title.pack(side='bottom')

img=Image.open('C:/Users/Admin/Desktop/project/logo.jpg').resize((205,136))
bitmap_img=ImageTk.PhotoImage(img,master=win)

logo_label=Label(win,imag=bitmap_img)
logo_label.place(relx=0,rely=0)


## this is use for frame home page not for new window

def main_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.68)
    global cap
    cap=''
    def generate_captcha():
        global cap
        d=str(random.randint(0,9))
        cap=cap+d
        ch=chr(random.randint(65,91))
        cap=cap+ch
        
        d=str(random.randint(0,9))
        cap=cap+d
        ch=chr(random.randint(65,90))
        cap=cap+ch
        return cap
      
    def reset():
        acn_entry.delete(0,"end")
        pass_entry.delete(0,"end")
        acn_entry.focus()

        
    
    ## this login click is use for use account,password and user role
    
    def login_click():
        global uacn
        uacn=acn_entry.get()
        upass=pass_entry.get()
        urole=role_cb.get()
        
        
        if len(uacn)==0 or len(upass)==0:
            messagebox.showerror("Login","ACN or Pass can't be empty")
            return
        
        
        if captcha_entry.get()!=cap:
            messagebox.showerror("Login","Invalid Captcha")
            return
        
        uacn=int(uacn)
        
        
        if uacn==0 and upass=='admin' and urole=='Admin':
            frm.destroy()
            welcome_admin_screen()
        
        elif urole=='User':
            
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select * from users where users_acno=? and users_pass=?',(uacn,upass))
            tup=cur_obj.fetchone()
            if tup==None:
                messagebox.showerror('login','Invalid ACN/PASS')
            else:
                global uname
                uname=tup[2]
                frm.destroy()
                welcome_user_screen()
        else:
            messagebox.showerror('login','Invalid Role')
        
        
    
    # these label and box is use for type the account number and password to login the bank page
    
    acn_label=Label(frm,font=('arial',20,'bold'),bg='pink',text='Account Number')
    acn_label.place(relx=.3,rely=.1)
    
    acn_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    acn_entry.place(relx=.5,rely=.1)
    acn_entry.focus()
    
    pass_label=Label(frm,font=('arial',20,'bold'),bg='pink',text='Password')
    pass_label.place(relx=.3,rely=.2)
    
    pass_entry=Entry(frm,font=('arial',20,'bold'),bd=5,show='*')
    pass_entry.place(relx=.5,rely=.2)
    
    role_label=Label(frm,font=('arial',20,'bold'),bg='pink',text='Role')
    role_label.place(relx=.3,rely=.3)
    
    # this combobox is use for play user and admin role in a box by clicking the arrow key 
    
    role_cb=Combobox(frm,width=22,font=('arial',18,'bold'),values=['User','Admin'])
    role_cb.current(0)
    role_cb.place(relx=.5,rely=.3)
    
    # these button are used for login ,reset and forgot password
    
    gen_captcha_label=Label(frm,width=6,font=('arial',20,'bold'),bg='white',fg='green',text=generate_captcha())
    gen_captcha_label.place(relx=.565,rely=.51)
    
    
    captcha_label=Label(frm,font=('arial',20,'bold'),bg='pink',text='Captcha')
    captcha_label.place(relx=.3,rely=.4)
    
    captcha_entry=Entry(frm,font=('arial',20,'bold'),bd=5,show='*')
    captcha_entry.place(relx=.5,rely=.4)
    
    
    login_btn=Button(frm,text='Login',font=('arial',18,'bold'),bg='powder blue',bd=5,command=login_click)
    login_btn.place(relx=.52,rely=.59)
    
    
    reset_btn=Button(frm,command=reset,text='Reset',font=('arial',18,'bold'),bg='powder blue',bd=5)
    reset_btn.place(relx=.62,rely=.59)
    
    
    forgot_btn=Button(frm,command=forgot_password_screen,text='Forgot Password',font=('arial',18,'bold'),bg='powder blue',bd=5)
    forgot_btn.place(relx=.52,rely=.73)
    
# this is use for after login the user or admin dispaly the next page and show text as welcome admin_screen  
def welcome_admin_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.71)
    
    # this logout function is use for logout from welcome page to home page
    
    def logout_click():
        resp=messagebox.askyesno("logout","Do you want to logout,kindly confirm ?")
        if resp:
            frm.destroy()
            main_screen()
        
    # this create function is use to create a user in login page
    
    def create_click():
        # this ifrm is use for inner frame
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.6)
        
        def reset_cl():
            name_entry.delete(0,"end")
            mob_entry.delete(0,"end")
            email_entry.delete(0,"end")
            aadhar_entry.delete(0,"end")
            name_entry.focus()

    
        def open_acn():
            uname=name_entry.get()
            umob=(mob_entry.get())
            uemail=email_entry.get()
            uaadhar=aadhar_entry.get()
            ubal=0
            upass=str(random.randint(100000,999999))
            
            if len(uname)==0:
                messagebox.showinfo('create','Empty name fields is not allowed')
                return
            
            if len(umob)==0:
                messagebox.showinfo('create','Empty mobile fields is not allowed')
                return
            
            if len(uemail)==0:
                messagebox.showinfo('create','Empty email fields is not allowed')
                return
            
            if len(uaadhar)==0:
                messagebox.showinfo('create','Empty aadhar fields is not allowed')
                return
            
            if not re.fullmatch('[a-zA-Z ]+',uname):
                messagebox.showerror('create','kindly enter valid name')
                return
            
            
            if not re.fullmatch('[6-9][0-9]{9}',umob):
               messagebox.showerror('create','kindly enter valid mobile number')
               return
            
            if not re.fullmatch('[a-z0-9_.]+@[a-z]+[.][a-z]+',uemail):
               messagebox.showerror('create','kindly enter valid Email ID')
               return
            
            if not re.fullmatch('[0-9]{12}',uaadhar):
                messagebox.showerror('create','kindly enter valid Aadhar number')
                return
            
            
            
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('insert into users(users_pass,users_name,users_mob,users_email,users_bal,users_aadhar,users_opendate) values(?,?,?,?,?,?,?)',(upass,uname,umob,uemail,ubal,uaadhar,current_date))
            con_obj.commit()
            con_obj.close()
            
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select max(users_acno) from users')
            tup=cur_obj.fetchone()
            uacn=tup[0]
            con_obj.close()
            #print("22")
            
            
        
            try:
                gmail_con=gmail.GMail('ankit.yadav476711@gmail.com','agym acbu zsze pfls')
                umsg=f'''Hello,{uname}
                Welcome to SBI 
                Your ACN is:{uacn}
                Your password is:{upass}
                Kindly change your password when you login 
                first time
                
                Thanks
                For giving a opportunities to service you
                '''
                #print('0000')
                msg=gmail.Message(to=uemail,subject='Account opened',text=umsg)
                gmail_con.send(msg)
                messagebox.showinfo('open acn','account created successfully kindly check your email for ACN/Pass')
                #print("1111")
            except Exception as e:
                messagebox.showerror('open acn','something went wrong')
                #print(e)
                    
        title_ifrm=Label(ifrm,font=('arial',18,'bold'),bg='white',text='This is Create user screen',fg='purple')
        title_ifrm.pack()
        
        name_label=Label(ifrm,font=('arial',15,'bold'),bg='white',text='Name',fg='blue')
        name_label.place(relx=.1,rely=.21)
        
        name_entry=Entry(ifrm,font=('arial',18,'bold'),bd=5,bg='sky blue',fg='black')
        name_entry.place(relx=.1,rely=.29)
        name_entry.focus()
        
        mob_label=Label(ifrm,font=('arial',15,'bold'),bg='white',text='Mobile',fg='blue')
        mob_label.place(relx=.1,rely=.42)
        
        mob_entry=Entry(ifrm,font=('arial',18,'bold'),bd=5,bg='sky blue',fg='black')
        mob_entry.place(relx=.1,rely=.5)
        
        email_label=Label(ifrm,font=('arial',15,'bold'),bg='white',text='Email',fg='blue')
        email_label.place(relx=.6,rely=.21)
        
        email_entry=Entry(ifrm,font=('arial',18,'bold'),bd=5,bg='sky blue',fg='black')
        email_entry.place(relx=.6,rely=.29)
        
        aadhar_label=Label(ifrm,font=('arial',15,'bold'),bg='white',text='Aadhar',fg='blue')
        aadhar_label.place(relx=.6,rely=.42)
        
        aadhar_entry=Entry(ifrm,font=('arial',18,'bold'),bd=5,bg='sky blue',fg='black')
        aadhar_entry.place(relx=.6,rely=.5)
        
        open_btn=Button(ifrm,command=open_acn,width=12,text='Open account',font=('arial',18,'bold'),bg='powder blue',bd=5)
        open_btn.place(relx=.25,rely=.7)
    
        reset_btn=Button(ifrm,command=reset_cl,width=12,text='Reset',font=('arial',18,'bold'),bg='powder blue',bd=5)
        reset_btn.place(relx=.55,rely=.7)
        
        
        
        
                
    def view_click():
        # this ifrm is use for inner frame
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.6)
    
        title_ifrm=Label(ifrm,font=('arial',18,'bold'),bg='white',text='This is View user screen',fg='purple')
        title_ifrm.pack()
        
        frame=Frame(ifrm)
        frame.place(relx=.1,rely=.1,relwidth=.8)
        
        data={}
        i=1
        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute("select * from users")
        
        for tup in cur_obj:
            
           data[f"{i}"]= {"Acno": tup[0],"Balance":tup[5],"Aadhar":tup[6],"Opendate":tup[7],"Email":tup[4],"Mob":tup[3]}
           i+=1
           
        con_obj.close()
           
        model=TableModel()
        model.importDict(data)
        
        table=TableCanvas(frame,model=model,editable=True)
        table.show()
        

        
    def delete_click():
        # this ifrm is use for inner frame
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.6)
    
        title_ifrm=Label(ifrm,font=('arial',18,'bold'),bg='white',text='This is Delete user screen',fg='purple')
        title_ifrm.pack()
        
        def delete_db():
            uacn=acn_entry.get()
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute("delete from users where users_acno=?",(uacn))
            cur_obj.execute("delete from txn where txn_acno=?",(uacn,))
            
            con_obj.commit()
            con_obj.close()
            messagebox.showinfo("Delete",f"User with Acn{uacn} deleted")
        def reset_a():
            acn_entry.delete(0,"end")
            acn_entry.focus()    
                
        acn_label=Label(ifrm,font=('arial',15,'bold'),bg='white',text='Account Number',fg='blue')
        acn_label.place(relx=.3,rely=.3)
        
        acn_entry=Entry(ifrm,font=('arial',18,'bold'),bd=5,fg='black',bg='sky blue')
        acn_entry.place(relx=.3,rely=.39)
        acn_entry.focus()
        
        
               
        
        delete_btn=Button(ifrm,command=delete_db,width=6,text='Delete',font=('arial',18,'bold'),bg='powder blue',bd=5)
        delete_btn.place(relx=.3,rely=.6)
    
        reset_btn=Button(ifrm,command=reset_a,width=6,text='Reset',font=('arial',18,'bold'),bg='powder blue',bd=5)
        reset_btn.place(relx=.47,rely=.6)
        
    
    wel_label=Label(frm,font=('arial',20,'bold'),bg='pink',text='Welcome Admin',fg='blue')
    wel_label.place(relx=.01,rely=.0)
        

    logout_btn=Button(frm,command=logout_click,text='logout',font=('arial',18,'bold'),bg='powder blue',bd=5)
    logout_btn.place(relx=.92,rely=0)
    
    create_btn=Button(frm,command=create_click,width=12,text='Create user',font=('arial',18,'bold'),bg='green',bd=5,fg='white')
    create_btn.place(relx=0,rely=.1)
    
    view_btn=Button(frm,command=view_click,width=12,text='view user',font=('arial',18,'bold'),bg='powder blue',bd=5)
    view_btn.place(relx=0,rely=.3)
    
    delete_btn=Button(frm,command=delete_click,width=12,text='Delete user',font=('arial',18,'bold'),bg='red',bd=5,fg='white')
    delete_btn.place(relx=0,rely=.5)
    
    
    
  # these button is used for forgot the password when the user lost his password then he forgot the password by this method
    
def forgot_password_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.71)
   
   # this back click is use for back the login page from home page
    
    def Back_click():
        frm.destroy()
        main_screen()
        
    def reset_cl():
            acn_entry.delete(0,"end")
            email_entry.delete(0,"end")
            mob_entry.delete(0,"end")
            acn_entry.focus()
        
    def get_password():
        uacn=acn_entry.get()
        umob=mob_entry.get()
        uemail=email_entry.get()
        
        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute('select users_name,users_pass from users where users_acno=? and users_email=? and users_mob=?',(uacn,uemail,umob))
        tup=cur_obj.fetchone()
        con_obj.close()
        
        if tup==None:
            messagebox.showerror('forgot password','Invalid Details')
        else:
            try:
                gmail_con=gmail.GMail('ankit.yadav476711@gmail.com','agym acbu zsze pfls')
                umsg=f'''Hello,{tup[0]}
                Welcome to SBI 
                Your password is:{tup[1]}

                Thanks
                '''
                msg=gmail.Message(to=uemail,subject='Password Recovery',text=umsg)
                gmail_con.send(msg)
                messagebox.showinfo('forgot password','kindly check your email for Pass')
            
            except:
                messagebox.showerror('forgot password','something went wrong')
                
            
        
        
    back_btn=Button(frm,command=Back_click,text='Back',font=('arial',18,'bold'),bg='powder blue',bd=5)
    back_btn.place(relx=0,rely=0)
    
    acn_label=Label(frm,font=('arial',20,'bold'),bg='pink',text='Account Number')
    acn_label.place(relx=.3,rely=.1)
    
    acn_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    acn_entry.place(relx=.5,rely=.1)
    acn_entry.focus()
    
    
    email_label=Label(frm,font=('arial',20,'bold'),bg='pink',text='Email')
    email_label.place(relx=.3,rely=.2)
    
    email_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    email_entry.place(relx=.5,rely=.2)
    
    mob_label=Label(frm,font=('arial',20,'bold'),bg='pink',text='Mobile')
    mob_label.place(relx=.3,rely=.3)
    
    mob_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    mob_entry.place(relx=.5,rely=.3)

    
    submit_btn=Button(frm,command=get_password,width=6,text='Submit',font=('arial',18,'bold'),bg='powder blue',bd=5)
    submit_btn.place(relx=.52,rely=.44)
    
    reset_btn=Button(frm,command=reset_cl,width=6,text='Reset',font=('arial',18,'bold'),bg='powder blue',bd=5)
    reset_btn.place(relx=.63,rely=.44)
    

def welcome_user_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.71)
     
    def logout_click():
        resp=messagebox.askyesnocancel("logout","Do you want to logout,kindly confirm ?")
        if resp:
            frm.destroy()
            main_screen()
        
    def check_click():
        # this ifrm is use for inner frame
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.23,rely=.15,relwidth=.65,relheight=.75)
    
        title_ifrm=Label(ifrm,font=('arial',18,'bold'),bg='white',text='This is Check Balance Screen',fg='purple')
        title_ifrm.pack()
        
        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute('select users_bal,users_opendate,users_aadhar from users where users_acno=?',(uacn,))
        tup=cur_obj.fetchone()
        con_obj.close()
        
        lbl_bal=Label(ifrm,text=f'Available Balance:\t{tup[0]}',fg='blue',font=('arial',15,'bold'),bg='white')
        lbl_bal.place(relx=.2,rely=.2)

        lbl_opendate=Label(ifrm,text=f'Account Opendate:\t{tup[1]}',fg='blue',font=('arial',15,'bold'),bg='white')
        lbl_opendate.place(relx=.2,rely=.4)
        
        lbl_aadhar=Label(ifrm,text=f'User Aadhar:\t{tup[2]}',fg='blue',font=('arial',15,'bold'),bg='white')
        lbl_aadhar.place(relx=.2,rely=.6)
        
        
        
    def update_click():
        # this ifrm is use for inner frame
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.23,rely=.15,relwidth=.65,relheight=.75)
    
        title_ifrm=Label(ifrm,font=('arial',18,'bold'),bg='white',text='This is Update Balance Screen',fg='purple')
        title_ifrm.pack()
        
        def update_details():
            uname=name_entry.get()
            umob=mob_entry.get()
            uemail=email_entry.get()
            upass=pass_entry.get()
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('update users set users_name=?,users_pass=?,users_email=?,users_mob=? where users_acno=?',(uname,upass,uemail,umob,uacn))
            con_obj.commit()
            con_obj.close()
            messagebox.showinfo('update','details updated')
           
        
        
        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute('select * from users where users_acno=?',(uacn,))
        tup=cur_obj.fetchone()
        con_obj.close()
        
        
        name_label=Label(ifrm,font=('arial',15,'bold'),bg='white',text='Name',fg='blue')
        name_label.place(relx=.1,rely=.21)
        
        name_entry=Entry(ifrm,font=('arial',18,'bold'),bd=5,bg='sky blue',fg='black')
        name_entry.place(relx=.1,rely=.29)
        name_entry.insert(0,tup[2])
        name_entry.focus()
        
        mob_label=Label(ifrm,font=('arial',15,'bold'),bg='white',text='Mobile',fg='blue')
        mob_label.place(relx=.1,rely=.42)
        
        mob_entry=Entry(ifrm,font=('arial',18,'bold'),bd=5,bg='sky blue',fg='black')
        mob_entry.place(relx=.1,rely=.5)
        mob_entry.insert(0,[3])
        
        
        email_label=Label(ifrm,font=('arial',15,'bold'),bg='white',text='Email',fg='blue')
        email_label.place(relx=.6,rely=.21)
        
        email_entry=Entry(ifrm,font=('arial',18,'bold'),bd=5,bg='sky blue',fg='black')
        email_entry.place(relx=.6,rely=.29)
        email_entry.insert(0,[4])
        
        
        pass_label=Label(ifrm,font=('arial',15,'bold'),bg='white',text='Password',fg='blue')
        pass_label.place(relx=.6,rely=.42)
        
        pass_entry=Entry(ifrm,font=('arial',18,'bold'),bd=5,bg='sky blue',fg='black')
        pass_entry.place(relx=.6,rely=.5)
        pass_entry.insert(0,[1])
        
        update_btn=Button(ifrm,command=update_details,width=12,text='Update',font=('arial',18,'bold'),bg='powder blue',bd=5)
        update_btn.place(relx=.393,rely=.7)
    
        
    def deposit_click():
        # this ifrm is use for inner frame
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.23,rely=.15,relwidth=.65,relheight=.75)
    
        title_ifrm=Label(ifrm,font=('arial',18,'bold'),bg='white',text='This is Deposit Balance Screen',fg='purple')
        title_ifrm.pack()
        
        def deposit_db():
            uamt=float(amt_entry.get())
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select users_bal from users where users_acno=?',(uacn,))
            ubal=cur_obj.fetchone()[0]
            con_obj.close()
            
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('update users set users_bal=users_bal+? where users_acno=?',(uamt,uacn))
            con_obj.commit()
            con_obj.close()
            
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(uacn,'cr(+)',time.strftime('%d-%b-%Y %r'),uamt,ubal+uamt))
            con_obj.commit()
            con_obj.close()
            
            messagebox.showinfo("deposit",f"Amount {uamt} deposited and updated bal {ubal+uamt}")
            
        
        amt_label=Label(ifrm,font=('arial',20,'bold'),bg='white',text='Amount',fg='blue')
        amt_label.place(relx=.25,rely=.3)
        
        amt_entry=Entry(ifrm,font=('arial',20,'bold'),bd=5,bg='sky blue',fg='black')
        amt_entry.place(relx=.4,rely=.3)
        
        deposit_btn=Button(ifrm,command=deposit_db,text='Deposit',font=('arial',20,'bold'),bg='powder blue',bd=5)
        deposit_btn.place(relx=.6,rely=.5)
        
    def withdraw_click():
        # this ifrm is use for inner frame
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.23,rely=.15,relwidth=.65,relheight=.75)
    
        title_ifrm=Label(ifrm,font=('arial',18,'bold'),bg='white',text='This is Withdraw Screen',fg='purple')
        title_ifrm.pack()
        
        def withdraw_db():
            uamt=float(amt_entry.get())
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select users_bal from users where users_acno=?',(uacn,))
            ubal=cur_obj.fetchone()[0]
            con_obj.close()
            
            if ubal>=uamt:
            
                con_obj=sqlite3.connect(database='bank.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute('update users set users_bal=users_bal-? where users_acno=?',(uamt,uacn))
                con_obj.commit()
                con_obj.close()
            
                con_obj=sqlite3.connect(database='bank.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(uacn,'Db(-)',time.strftime('%d-%b-%Y %r'),uamt,ubal-uamt))
                con_obj.commit()
                con_obj.close()
            
                messagebox.showinfo("withdraw",f"Amount {uamt} withdrawn and updated bal {ubal-uamt}")
            else:
                messagebox.showerror("withdraw",f"Insufficient Bal {ubal}")
        
        
        amt_label=Label(ifrm,font=('arial',20,'bold'),bg='white',text='Amount',fg='blue')
        amt_label.place(relx=.25,rely=.3)
        
        amt_entry=Entry(ifrm,font=('arial',20,'bold'),bd=5,bg='sky blue',fg='black')
        amt_entry.place(relx=.4,rely=.3)
        
        withdraw_btn=Button(ifrm,command=withdraw_db,text='Withdraw',font=('arial',20,'bold'),bg='powder blue',bd=5)
        withdraw_btn.place(relx=.575,rely=.5)
        
    def transfer_click():
        # this ifrm is use for inner frame
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.23,rely=.15,relwidth=.65,relheight=.75)
    
        title_ifrm=Label(ifrm,font=('arial',18,'bold'),bg='white',text='This is Transfer Screen',fg='purple')
        title_ifrm.pack()
        
        def transfer_db():
            uamt=float(amt_entry.get())
            toacn=int(to_entry.get())
           
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select users_bal,users_email from users where users_acno=?',(uacn,))
            tup=cur_obj.fetchone()
            ubal=tup[0]
            uemail=tup[1]           
            con_obj.close()
            
            if ubal>=uamt:
                
                con_obj=sqlite3.connect(database='bank.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute("select * from users where users_acno=?",(toacn,))
                tup=cur_obj.fetchone()
                con_obj.close()
                
                if tup==None:
                    
                     messagebox.showerror("transfer","To ACN does not exist")
                else:
                    
                    otp=random.randint(1000,9999)
                    try:
                        gmail_con=gmail.GMail('ankit.yadav476711@gmail.com','agym acbu zsze pfls')
                        umsg=f'''Hello,{uname}
                        Welcome to SBI 
                        Your OTP is:{otp}
                        Kindly verify this otp to complete your transaction
                
                        Thanks
                        For giving a opportunities to service you
                        '''
                        msg=gmail.Message(to=uemail,subject='Account opened',text=umsg)
                        gmail_con.send(msg)
                        messagebox.showinfo('txn','we have send otp to your registered email')
                        
                        uotp=simpledialog.askinteger("OTP","Enter OTP")
                        if otp==uotp:
                            con_obj=sqlite3.connect(database='bank.sqlite')
                            cur_obj=con_obj.cursor()
                            cur_obj.execute('update users set users_bal=users_bal-? where users_acno=?',(uamt,uacn))
                            cur_obj.execute('update users set users_bal=users_bal+? where users_acno=?',(uamt,toacn))
                            
                            con_obj.commit()
                            con_obj.close()
                            
                            tobal=tup[5]
                    
                            con_obj=sqlite3.connect(database='bank.sqlite')
                            cur_obj=con_obj.cursor()
                            cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(uacn,'Db(-)',time.strftime('%d-%b-%Y %r'),uamt,ubal-uamt))
                            cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(toacn,'Cr(+)',time.strftime('%d-%b-%Y %r'),uamt,ubal+uamt))
                            con_obj.commit()
                            con_obj.commit()
                            con_obj.close()
                    
                            messagebox.showinfo("transfer",f"Amount {uamt} transfered and updated bal {ubal-uamt}")
                        else:
                            messagebox.showerror('otp','Invalid OTP')
                            

                    except:
                        messagebox.showerror('txn','something went wrong')
          
            else:
                messagebox.showerror("transfer",f"Insufficient Bal {ubal}")
        
        
        
        to_label=Label(ifrm,font=('arial',20,'bold'),bg='white',text='To ACN',fg='blue')
        to_label.place(relx=.25,rely=.3)
        
        to_entry=Entry(ifrm,font=('arial',20,'bold'),bd=5,bg='sky blue',fg='black')
        to_entry.place(relx=.4,rely=.3)
        
        amt_label=Label(ifrm,font=('arial',20,'bold'),bg='white',text='Amount',fg='blue')
        amt_label.place(relx=.25,rely=.45)
        
        amt_entry=Entry(ifrm,font=('arial',20,'bold'),bd=5,bg='sky blue',fg='black')
        amt_entry.place(relx=.4,rely=.45)
        
        transfer_btn=Button(ifrm,command=transfer_db,text='Transfer',font=('arial',20,'bold'),bg='powder blue',bd=5)
        transfer_btn.place(relx=.59,rely=.6)
        
    def history_click():
        # this ifrm is use for inner frame
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.23,rely=.15,relwidth=.65,relheight=.75)
    
        title_ifrm=Label(ifrm,font=('arial',18,'bold'),bg='white',text='This is History Balance Screen',fg='purple')
        title_ifrm.pack()
        
        
        frame=Frame(ifrm)
        frame.place(relx=.1,rely=.1,relwidth=.72)
        
        data={}
        i=1
        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute("select * from txn where txn_acno=?",(uacn,))
        
        for tup in cur_obj:
            
           data[f"{i}"]= {"Txn Id": tup[0],"Txn Amt":tup[4],"Txn Date":tup[3],"Txn Type":tup[2],"updatebal":tup[5]}
           i+=1
           
        con_obj.close()
           
        model=TableModel()
        model.importDict(data)
        
        table=TableCanvas(frame,model=model,editable=True)
        table.show()
        
            
    wel_label=Label(frm,font=('arial',20,'bold'),bg='pink',text=f"Welcome {uname}",fg='blue')
    wel_label.place(relx=.0,rely=.0)
        

    logout_btn=Button(frm,command=logout_click,text='logout',font=('arial',18,'bold'),bg='sky blue',bd=5)
    logout_btn.place(relx=.92,rely=0)
    
    check_btn=Button(frm,command=check_click,width=15,text='Check Balance',font=('arial',18,'bold'),bg='teal',bd=5,fg='white')
    check_btn.place(relx=0,rely=.1)
    
    update_btn=Button(frm,command=update_click,width=15,text='Update Details',font=('arial',18,'bold'),bg='cyan',bd=5)
    update_btn.place(relx=0,rely=.25)
    
    deposit_btn=Button(frm,command=deposit_click,width=15,text='Deposit Amount',font=('arial',18,'bold'),bg='green',bd=5,fg='white')
    deposit_btn.place(relx=0,rely=.4)
    
    withdraw_btn=Button(frm,command=withdraw_click,width=15,text='Withdraw Amount',font=('arial',18,'bold'),bg='red',bd=5,fg='white')
    withdraw_btn.place(relx=0,rely=.55)
    
    transfer_btn=Button(frm,command=transfer_click,width=15,text='Transfer Amount',font=('arial',18,'bold'),bg='magenta',bd=5,fg='white')
    transfer_btn.place(relx=0,rely=.7)
    
    history_btn=Button(frm,command=history_click,width=15,text='Transaction History',font=('arial',18,'bold'),bg='indigo',bd=5,fg='white')
    history_btn.place(relx=0,rely=.85)
    


# it is use for display the screen and iterate the window

main_screen()
win.mainloop()
