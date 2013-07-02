'''
This scripts copy cuts depending on the size of a single-cut from the Cuts directory.

To run this script you have to have "Cuts" directory in the main directory, which is filled with scultpure cuts writen in *.jpg format. Files should have a names from 1.jpg to any amount (for example 10000.jpg, 5000.jpg etc.).

'''

__author__ = 'itor13@gmail.com'
__version__ = '3.92'

import os, sys, shutil, wx, time

FN_APPEND = '.jpg'

amount_of_copied_cuts = 0
amount_of_cuts = 0
size_of_sculpture = 0
user_cut_thickness = 0

class Cuts_copy(wx.Frame):

    def __init__(self,parent,id):
        global items

        if not os.path.exists('Cuts'):
            message=wx.MessageDialog(None,'Can\'t find "Cuts" directiory. Please, copy directory with cuts into the main directory and rename it as "Cuts"!','Error',wx.ICON_HAND)
            message.ShowModal()
            wx.Frame.__init__(self,parent,id,'Cuts Coppier',size=(600,200))
            self.Destroy()

        else:
            items = os.listdir('Cuts')
            amount_of_cuts = len(items)
            wx.Frame.__init__(self,parent,id,'Cuts Coppier',size=(600,200))
            self.Centre()
            self.panel=wx.Panel(self)

            self.progress_bar = wx.Gauge(self.panel, -1, style=wx.GA_HORIZONTAL) 
            self.progress_bar.SetPosition((330, 95))
            self.progress_bar.SetSize((200, 20))
            self.progress_bar.Show()

            self.size_of_sulpture_text_up=wx.StaticText(self.panel, -1, "Size of a sculpture [mm]", (10,10),(250,-1),wx.ALIGN_CENTER)
            self.size_of_sulpture_text_up.SetForegroundColour('white')
            self.size_of_sulpture_text_up.SetBackgroundColour('blue')

            self.user_cut_thickness_text_up=wx.StaticText(self.panel, -1, "Size of a cut [mm]", (10,60),(250,-1),wx.ALIGN_CENTER)
            self.user_cut_thickness_text_up.SetForegroundColour('white')
            self.user_cut_thickness_text_up.SetBackgroundColour('blue')

            self.user_cut_thickness_text=wx.StaticText(self.panel, -1, "", (10,110),)
            self.user_cut_thickness_text.SetForegroundColour('white')
            self.user_cut_thickness_text.SetBackgroundColour('dark green')

            self.amount_of_cuts_text=wx.StaticText(self.panel, -1, "Amount of all cuts from database: " + str(amount_of_cuts), (10,110),)
            self.amount_of_cuts_text.SetForegroundColour('white')
            self.amount_of_cuts_text.SetBackgroundColour('dark green')

            self.amount_of_copied_cuts_text=wx.StaticText(self.panel, -1, "Amount of cuts which was coppied: " + str(amount_of_copied_cuts), (10,140),)
            self.amount_of_copied_cuts_text.SetForegroundColour('white')
            self.amount_of_copied_cuts_text.SetBackgroundColour('dark green')

            self.status_text=wx.StaticText(self.panel, -1, "How are you?", (380,120),size=(100, -1), style=wx.TE_CENTRE)

            self.button=wx.Button(self.panel,label="Copy property cuts",pos=(330,30),size=(200,60))

            self.Bind(wx.EVT_BUTTON,self.Cuts_coppier)
            self.box=wx.TextCtrl(self.panel, pos=(10,30),size=(250,-1),style=wx.TE_CENTRE)
            self.box2=wx.TextCtrl(self.panel, pos=(10,80),size=(250,-1),style=wx.TE_CENTRE)

    def Cuts_coppier(self,event):
        global items
        global cut_thickness
        global size_of_sculpture, user_cut_thickness

        self.working_status()
        self.button.Disable()
        self.progress_bar.SetValue(0)
        wx.Yield()
        try:
            size_of_sculpture = float(self.box.GetValue())
            user_cut_thickness = float(self.box2.GetValue())
        except:
            self.message_show('You provide wrong data!')
            self.Blad_status()
            self.amount_of_copied_cuts_text.SetLabel("Amount of cuts which was coppied: " + str(0))
            return
        if not os.path.exists('Cuts'):
            self.message_show('Can\'t find "Cuts" directiory. Please, copy directory with cuts into the main directory and rename it as "Cuts"!')
            self.Blad_status()
            self.amount_of_copied_cuts_text.SetLabel("Amount of cuts which was coppied: " + str(0))
            return
        elif size_of_sculpture <= 0 or user_cut_thickness <= 0:
            self.message_show('You have to provide numbers greater than zero.')
            self.Blad_status()
            self.amount_of_copied_cuts_text.SetLabel("Amount of cuts which was coppied: " + str(0))
            return
        elif size_of_sculpture < user_cut_thickness:
            self.Cuts_result_dir()
            shutil.copy("Cuts/"+str(int(round((len(items)/2),0)))+".jpg", "Cuts_result/"+str(1)+".jpg")
            self.amount_of_copied_cuts_text.SetLabel("Amount of cuts which was coppied: " + str(1))
            self.progress_bar.SetValue(100)
            wx.Yield()
            self.OK_status()
            
        else:
            amount_of_cuts = len(items)
            test_count = 1
            total_cuts_count = 1
            cuts_count = 1
            cuts_size_count = 0
            filename_write = 1
            cut_number = 0 # this is the number of the cut which should be coppied into Cuts_result directory
            items = os.listdir('Cuts')
            number_of_a_cuts = len(items)
            if int(number_of_a_cuts) != 0:
                self.Cuts_result_dir()
                cut_thickness = size_of_sculpture / number_of_a_cuts # Cut thickness for the entered size of scultpure

                if round(cut_thickness,2) > user_cut_thickness:
                    self.Bigger_Cuts()
                    return

                else:

                    while total_cuts_count != amount_of_cuts + 1:
                        cuts_size_count += cut_thickness 
                        if round(cuts_size_count,2) >= user_cut_thickness:
                            if total_cuts_count == 1:
                                cut_number = 1
                                total_cuts_count += 1
                                self.progress(total_cuts_count,amount_of_cuts)
                            else:
                                cut_number = total_cuts_count - float(cuts_count / 2)
                                total_cuts_count += 1
                                self.progress(total_cuts_count,amount_of_cuts)

                            filename_read = str("%d.jpg") % cut_number
                            shutil.copy("Cuts/"+filename_read, "Cuts_result/"+str(filename_write)+".jpg")
                            filename_write += 1
                            cuts_size_count -= user_cut_thickness
                            cuts_count = 1
                        else:
                            total_cuts_count += 1
                            cuts_count += 1
                            self.progress(total_cuts_count,amount_of_cuts)
                amount_of_copied_cuts = len(os.listdir('Cuts_result'))
                self.amounts()
                self.OK_status()

            else:
                amount_of_copied_cuts = 0
                self.message_show('"Cuts" directory  is empty!!!')
                self.amounts()
                self.Blad_status()

    def Bigger_Cuts(self):
        '''
        Copy cuts if cut thickness is smaller than user cut thickness
        '''
        cut_number = 1
        filename_write = 1
        total_cuts_count = 1
        cuts_size_count = 0
        amount_of_cuts = len(items)
        while total_cuts_count != amount_of_cuts + 1:
            cuts_size_count += user_cut_thickness
            if total_cuts_count == amount_of_cuts:
                while round(cuts_size_count,2) < cut_thickness:
                    cut_number = total_cuts_count
                    try:
                        filename_read = str("%d.jpg") % cut_number
                        shutil.copy("Cuts/"+filename_read, "Cuts_result/"+str(filename_write)+".jpg")
                    except:
                        message_file= str("Z: Cuts/%s\nDo: Cuts_result/%s.jpg") % (filename_read, str(filename_write))
                        self.Blad_status()
                        self.message_show('Can\'t copy file\n'+message_file)
                        return
                    filename_write += 1
                    cuts_size_count += user_cut_thickness

                total_cuts_count += 1
                self.progress(total_cuts_count,amount_of_cuts)
                
            else:
                if not round(cuts_size_count,2) < cut_thickness:
                    cut_number = total_cuts_count + 1
                    try:
                        filename_read = str("%d.jpg") % cut_number
                        shutil.copy("Cuts/"+filename_read, "Cuts_result/"+str(filename_write)+".jpg")
                    except:
                        message_file= str("Z: Cuts/%s\nDo: Cuts_result/%s.jpg") % (filename_read, str(filename_write))
                        self.Blad_status()
                        self.message_show('Can\'t copy file\n'+message_file)
                        return
                    filename_write += 1
                    cuts_size_count = cuts_size_count - cut_thickness
                    total_cuts_count += 1
                    self.progress(total_cuts_count,amount_of_cuts)

                else:
                    cut_number = total_cuts_count      
                    try:
                        filename_read = str("%d.jpg") % cut_number
                        shutil.copy("Cuts/"+filename_read, "Cuts_result/"+str(filename_write)+".jpg")
                    except:
                        message_file= str("Z: Cuts/%s\nDo: Cuts_result/%s.jpg") % (filename_read, str(filename_write))
                        self.Blad_status()
                        self.message_show('Can\'t copy file\n'+message_file)
                        return
                    filename_write += 1
        self.OK_status()

    def Blad_status(self):
        '''
        Change status to: Error!
        '''
        self.status_text=wx.StaticText(self.panel, -1, "Error!", (380,120),size=(100, -1), style=wx.TE_CENTRE)
        self.status_text.SetForegroundColour('white')
        self.status_text.SetBackgroundColour('red')

    def OK_status(self):
        '''
        Change status to: Everything is OK!
        '''
        self.status_text=wx.StaticText(self.panel, -1, "Everything is OK!", (380,120),size=(100, -1), style=wx.TE_CENTRE)
        self.status_text.SetForegroundColour('white')
        self.status_text.SetBackgroundColour('dark green')
        self.amounts()
        self.button.Enable()
        
    def working_status(self):
        '''
        Change status to: Working...
        '''
        self.status_text=wx.StaticText(self.panel, -1, "Working...!", (380,120),size=(100, -1), style=wx.TE_CENTRE)
        self.status_text.SetForegroundColour('black')
        self.status_text.SetBackgroundColour('none')

    def message_show(self, message):
        '''
        Show provided message
        '''
        self.amounts()
        message_warning=wx.MessageDialog(None,message,'Error!',wx.ICON_HAND)
        message_warning.ShowModal()
        self.button.Enable()
        
    def amounts(self):
        '''
        Counts cuts in both directories
        '''
        amount_of_cuts=len(items)
        try:
            amount_of_copied_cuts = len(os.listdir('Cuts_result'))
        except:
            amount_of_copied_cuts = 0
        self.amount_of_cuts_text.SetLabel("Amount of all cuts from database: " + str(amount_of_cuts))
        self.amount_of_copied_cuts_text.SetLabel("Amount of cuts which was coppied: " + str(amount_of_copied_cuts))

    def progress(self,total_cuts_count, amount_of_cuts):
        '''
        Updates progress bar
        '''
        progress_value = (total_cuts_count*100)/amount_of_cuts
        if self.progress_bar.Value != progress_value:
            self.progress_bar.SetValue(progress_value)
        wx.Yield()
        
    def Cuts_result_dir(self):
        '''
        Makes Cuts_results dir
        '''
        if os.path.exists('Cuts_result'):
            shutil.rmtree('Cuts_result')
            time.sleep(1)
            os.mkdir('Cuts_result')
        else:
            os.mkdir('Cuts_result')
            
if __name__=='__main__':
    app=wx.PySimpleApp()
    frame=Cuts_copy(parent=None,id=-1)
    frame.Show()
    app.MainLoop()
