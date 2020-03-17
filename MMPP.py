import sys 
import numpy as np


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
class MeshTalBlock:
    """ Basic Data block object. """

    # pylint: disable=too-many-instance-attributes
    # Necessary

    # #####################################################
    # Constructor
    def __init__(self):
        self.e_bins = []
        self.x_bins = []
        self.y_bins = []
        self.z_bins = []
        self.bin_lims = [0.0,0.0,0.0,0.0]
        self.nx = 0
        self.ny = 0
        self.nz = 0
        self.ng = 0
        self.data_values = []
        print("MeshTalBlock created")
      
    # #####################################################  
    def __ChooseCellE(self,EValue,verbose=True):
        """ Chooses an energy-bin based on a specific value for the
        energy. """
        index = len(self.e_bins)-1
        for a in range(0,len(self.e_bins)):
            if (self.e_bins[a] > EValue):
                index = a
                break
            
            
        print("The chosen energy bin is " + 
              str(index) + " with upper limit " + 
              str(self.e_bins[index] ))
        return index
      
    # #####################################################  
    def __ChooseCellX(self,XValue):
        """ Chooses coordinate bin based on specific value. """

        index = (len(self.x_bins))-1
        for a in range(0,len(self.x_bins)):
            if (XValue <= self.x_bins[a]):
                index = a
                break
        print("The chosen X coordinate is " + str(self.x_bins[index] ))
        return index

    # #####################################################
    def __ChooseCellY(self,YValue):
        """ Chooses coordinate bin based on specific value. """

        index = (len(self.y_bins))-1
        for a in range(0,len(self.y_bins)):
            if(YValue <= self.y_bins[a]):
                index = a
                break
        print("The chosen Y coordinate is " + str(self.y_bins[index] ))
        return index
     
    # ##################################################### 
    def __ChooseCellZ(self,ZValue):
        """ Chooses coordinate bin based on specific value. """

        index = (len(self.z_bins))-1
        for a in range(0,len(self.z_bins)):
            if(ZValue <= self.z_bins[a]):
                index = a
                break
        print("The chosen Z coordinate is " + str(self.z_bins[index] ))
        return index
    
    # #####################################################
    def SizeDataValues(self):
        """ Don't use this method outside MMPP. 
        Sizes data structures. """

        self.nx = len(self.x_bins)
        self.ny = len(self.y_bins)
        self.nz = len(self.z_bins)
        self.ng = len(self.e_bins)+1
    
        self.data_values = np.zeros([self.ng,self.nx,self.ny,self.nz,5])
    
    # #####################################################
    def UnpackGivenXYE(self,x,y,e):
        """ Extracts line data by unpacking data from the data block 
        given an x-coordinate, y-coordinate and an energy value. 
        
        Arguments:
            x: [float] A coordinate. Bin will be chosen. 
            y: [float] A coordinate. Bin will be chosen.
            e: [float] An energy value. Bin will be chosen. 
            
        Returns:
            s: [float array] Coordinate centers.
            v: [float array] Values. """

        n = self.nz 
        s = np.zeros(n)
        v = np.zeros(n)
        for i in range(0,n):
            s[i] = self.data_values[e,x,y,i,2]
            v[i] = self.data_values[e,x,y,i,3]
        
        return s,v
  
    # #####################################################
    def UnpackGivenXZE(self,x,z,e):
        """ Extracts line data by unpacking data from the data block 
        given an x-coordinate, z-coordinate and an energy value. 
        
        Arguments:
            x: [float] A coordinate. Bin will be chosen. 
            z: [float] A coordinate. Bin will be chosen.
            e: [float] An energy value. Bin will be chosen. 
            
        Returns:
            s: [float array] Coordinate centers.
            v: [float array] Values. """

        n = self.ny
        s = np.zeros(n)
        v = np.zeros(n)
        for i in range(0,n):
            s[i] = self.data_values[e,x,i,z,1]
            v[i] = self.data_values[e,x,i,z,3]
        
        return s,v
  
    # #####################################################
    def UnpackGivenYZE(self,y,z,e):
        """ Extracts line data by unpacking data from the data block 
        given an y-coordinate, z-coordinate and an energy value. 
        
        Arguments:
            y: [float] A coordinate. Bin will be chosen. 
            z: [float] A coordinate. Bin will be chosen.
            e: [float] An energy value. Bin will be chosen. 
            
        Returns:
            s: [float array] Coordinate centers.
            v: [float array] Values. """

        n = self.nx
        s = np.zeros(n)
        v = np.zeros(n)
        for i in range(0,n):
            s[i] = self.data_values[e,i,y,z,0]
            v[i] = self.data_values[e,i,y,z,3]
        
        return s,v
  
    # #####################################################
    def UnpackGivenXE_bins(self,x,e):
        """ Extracts YZ-2D plane data by unpacking data from the 
        data block given an x-bin and an energy bin. 
        
        Arguments:
            x: [int] X-bin number.
            e: [int] Energy bin number.
            
        Returns:
            s: [float array] Coordinate centers along y. Logically 2D.
            t: [float array] Coordinate centers along z. Logically 2D.
            v: [float array] Values. Logically 2D.
            u: [float array] Uncertainty.  Logically 2D.
            
        The returned values are logically 2D (row based). """

        n0 = self.ny
        n1 = self.nz

        if (n0 <= 1) or (n1 <= 1):
            print("ERROR: UnpackGivenXE found data that is not 2D. " + \
                  "This normally indicates only 1 bin along a " + \
                  "direction.")
            exit()
    
        s = np.zeros([n0,n1])
        t = np.zeros([n0,n1])
        v = np.zeros([n0,n1])
        z = np.zeros([n0,n1])
        for i in range(0,n0):
            for j in range(0,n1):
                s[i,j] = self.data_values[e,x,i,j,1]
                t[i,j] = self.data_values[e,x,i,j,2]
                v[i,j] = self.data_values[e,x,i,j,3]
                z[i,j] = self.data_values[e,x,i,j,4]
        
        return s,t,v,z

    # #####################################################    
    def UnpackGivenYE_bins(self,y,e):
        """ Extracts XZ-2D plane data by unpacking data from the 
        data block given an y-bin and an energy bin. 
        
        Arguments:
            y: [int] Y-bin number.
            e: [int] Energy bin number.
            
        Returns:
            s: [float array] Coordinate centers along x. Logically 2D.
            t: [float array] Coordinate centers along z. Logically 2D.
            v: [float array] Values. Logically 2D.
            u: [float array] Uncertainty.  Logically 2D.
            
        The returned values are logically 2D (row based). """

        n0 = self.nx
        n1 = self.nz

        if (n0 <= 1) or (n1 <= 1):
            print("ERROR: UnpackGivenXE found data that is not 2D. " + \
                  "This normally indicates only 1 bin along a " + \
                  "direction.")
            exit()

        s = np.zeros([n0,n1])
        t = np.zeros([n0,n1])
        v = np.zeros([n0,n1])
        z = np.zeros([n0,n1])
        for i in range(0,n0):
            for j in range(0,n1):
                s[i,j] = self.data_values[e,i,y,j,0]
                t[i,j] = self.data_values[e,i,y,j,2]
                v[i,j] = self.data_values[e,i,y,j,3]
                z[i,j] = self.data_values[e,i,y,j,4]
    
        return s,t,v,z
    
    # #####################################################
    def UnpackGivenZE_bins(self,zbin,e):
        """ Extracts XY-2D plane data by unpacking data from the 
        data block given an z-bin and an energy bin. 
        
        Arguments:
            z: [int] Z-bin number.
            e: [int] Energy bin number.
            
        Returns:
            s: [float array] Coordinate centers along x. Logically 2D.
            t: [float array] Coordinate centers along y. Logically 2D.
            v: [float array] Values. Logically 2D.
            u: [float array] Uncertainty.  Logically 2D.
            
        The returned values are logically 2D (row based). """

        n0 = self.nx
        n1 = self.ny

        if (n0 <= 1) or (n1 <= 1):
            print("ERROR: UnpackGivenXE found data that is not 2D. " + \
                  "This normally indicates only 1 bin along a " + \
                  "direction.")
            exit()
        
        s = np.zeros([n0,n1])
        t = np.zeros([n0,n1])
        v = np.zeros([n0,n1])
        z = np.zeros([n0,n1])
        for i in range(0,n0):
            for j in range(0,n1):
                s[i,j] = self.data_values[e,i,j,zbin,0]
                t[i,j] = self.data_values[e,i,j,zbin,1]
                v[i,j] = self.data_values[e,i,j,zbin,3]
                z[i,j] = self.data_values[e,i,j,zbin,4]
        return s,t,v,z
    
    # #####################################################
    def UnpackGivenXE(self,xval,e):
        """ Extracts YZ-2D plane data by unpacking data from the 
        data block given an x-coordinate and an energy value. 
        
        Arguments:
            x: [float] A coordinate. Bin will be chosen. 
            e: [float] An energy value. Bin will be chosen. 
            
        Returns:
            s: [float array] Coordinate centers along y. Logically 2D.
            t: [float array] Coordinate centers along z. Logically 2D.
            v: [float array] Values. Logically 2D.
            u: [float array] Uncertainty.  Logically 2D.
            
        The returned values are logically 2D (row based). """

        x = self.__ChooseCellX(float(xval))
        
        s,t,v,u = self.UnpackGivenXE_bins(x,e)
        
        return s,t,v,u
  
    # #####################################################
    def UnpackGivenYE(self,yval,e):
        """ Extracts XZ-2D plane data by unpacking data from the 
        data block given an y-coordinate and an energy value. 
        
        Arguments:
            y: [float] A coordinate. Bin will be chosen. 
            e: [float] An energy value. Bin will be chosen. 
            
        Returns:
            s: [float array] Coordinate centers along x. Logically 2D.
            t: [float array] Coordinate centers along z. Logically 2D.
            v: [float array] Values. Logically 2D.
            u: [float array] Uncertainty.  Logically 2D.
            
        The returned values are logically 2D (row based). """
        
        y = self.__ChooseCellY(float(yval))
        s,t,v,u = self.UnpackGivenYE_bins(y,e)
        
        return s,t,v,u
  
    # #####################################################
    def UnpackGivenZE(self,zval,e):
        """ Extracts XY-2D plane data by unpacking data from the 
        data block given an z-coordinate and an energy value. 
        
        Arguments:
            z: [float] A coordinate. Bin will be chosen. 
            e: [float] An energy value. Bin will be chosen. 
            
        Returns:
            s: [float array] Coordinate centers along x. Logically 2D.
            t: [float array] Coordinate centers along y. Logically 2D.
            v: [float array] Values. Logically 2D.
            u: [float array] Uncertainty.  Logically 2D.
            
        The returned values are logically 2D (row based). """
        
        z = self.__ChooseCellZ(float(zval))
        s,t,v,u = self.UnpackGivenZE_bins(z,e)
        
        return s,t,v,u

      
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def ReadMeshtalfile(meshtal_filename):
    print('***** Reading file "' + meshtal_filename + '"')
    mfile = open(meshtal_filename,"r")
    lines = mfile.readlines()
    num_lines = len(lines)
    print("Number of lines = "+str(num_lines))
  
    ############################################ Data structures
    blocks = []
  
    ############################################ Read energy groups
    ell = -1
    stop_flag = False
    cur_block = []
    while not stop_flag:
        ell += 1
        line = lines[ell]
    
        words = line.split()
    
        ############################## Detect new block
        if len(words) >= 3:
            if (words[0]=="Mesh") and \
               (words[1]=="Tally") and \
               (words[2]=="Number"):
                cur_block = MeshTalBlock()
                blocks.append(cur_block)
    
        ############################## Detect x bins
        if len(words) >= 3:
            if (words[0]=="X") and \
               (words[1]=="direction:"):
                num_bounds = len(words)-3
                for b in range(0,num_bounds):
                    cur_block.x_bins.append(float(words[b+3]))
                cur_block.bin_lims[0] = float(words[3])
                print("X bins extracted:", len(cur_block.x_bins))
    
        ############################## Detect y bins
        if len(words) >= 3:
            if (words[0]=="Y") and \
               (words[1]=="direction:"):
                num_bounds = len(words)-3
                for b in range(0,num_bounds):
                    cur_block.y_bins.append(float(words[b+3]))
                cur_block.bin_lims[1] = float(words[3])
                print("Y bins extracted:", len(cur_block.y_bins))
    
        ############################## Detect z bins
        if len(words) >= 3:
            if (words[0]=="Z") and \
               (words[1]=="direction:"):
                num_bounds = len(words)-3
                for b in range(0,num_bounds):
                    cur_block.z_bins.append(float(words[b+3]))
                cur_block.bin_lims[2] = float(words[3])
                print("Z bins extracted:", len(cur_block.z_bins))
    
        ############################## Detect energy boundaries
        if len(words) >= 3:
            if (words[0]=="Energy") and \
               (words[1]=="bin") and \
               (words[2]=="boundaries:"):
                num_bounds = len(words)-4
                for g in range(0,num_bounds):
                    cur_block.e_bins.append(float(words[g+4]))
                cur_block.bin_lims[3] = float(words[4])
                print("Energy bins extracted:", 
                      len(cur_block.e_bins),cur_block.e_bins)
                print("Sizing data black")
                cur_block.SizeDataValues()
    
        ############################## Extract data
        if len(words) >= 3:
            if (words[0]=="Energy") and \
               (words[1]=="X") and \
               (words[2]=="Y"):
                nx = cur_block.nx
                ny = cur_block.ny
                nz = cur_block.nz
                ng = cur_block.ng
                for e in range(0,ng):
                    for x in range(0,nx):
                        for y in range(0,ny):
                            for z in range(0,nz):
                                ell += 1
                                dline = lines[ell]
                                words = dline.split()
                                cur_block.data_values[e,x,y,z,0] = float(words[1])
                                cur_block.data_values[e,x,y,z,1] = float(words[2])
                                cur_block.data_values[e,x,y,z,2] = float(words[3])
                                cur_block.data_values[e,x,y,z,3] = float(words[4])
                                cur_block.data_values[e,x,y,z,4] = float(words[5])
    
    
        if (ell >= (num_lines-1)) or ell>100:
            stop_flag = True
            print("***** Quit at file end")
  
      # print(words)
  
    mfile.close()
  
    return blocks

def menu():
    print("")
    print("Please select one of the following options:")
    print("1: Slice in the YZ plane")
    print("2: Slice in the XZ plane")
    print("3: Slice in the XY plane")
    print("4: Enter a specify energy level, it's assumed to be the 0th energy-bin")
    print("9: Exit")
    return input()
    
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Main program if run as standalone
# if __name__ == '__main__':
#     num_args = len(sys.argv)
#     print("Program arguments:",sys.argv)
  
#     if num_args < 2:
#        in_meshtal_filename = input("Enter the name of the meshtal file: ")
#     else:
#        in_meshtal_filename = sys.argv[1]
#     blocks = ReadMeshtalfile(in_meshtal_filename)
  
#     e = 0
    
#     while (True):
#         temp = float(menu())
#         if temp == 1:
#             xval = input("Enter an X coord: ")
#             s,t,v,z = blocks[0].UnpackGivenXE(xval,e)
#             s,t,v2,z = blocks[0].UnpackGivenXE(xval,1)
#             plt.xlabel("Y [cm]")
#             plt.ylabel("Z [cm]")
#             #plott(s,t,v)
#             if (float(input("Do you want to see a plot of the error? 1 or 0: "))==1.0):
#                 plt.contourf(s,t,z,cmap=cm.jet)
#                 plt.title("Relative error")
#                 plt.xlabel("Y [cm]")
#                 plt.ylabel("Z [cm]")
#                 plt.show()
            
#         elif temp == 2:
#             yval = input("Enter a Y coord: ")
#             s,t,v,z = blocks[0].UnpackGivenYE(yval,e)
#             s,t,v2,z = blocks[0].UnpackGivenYE(yval,1)
#             plt.xlabel("X [cm]")
#             plt.ylabel("Z [cm]")
#             plott(s,t,v)
#             if (float(input("Do you want to see a plot of the error? 1 or 0: "))==1.0):
#                 plt.contourf(s,t,z,cmap=cm.jet)
#                 plt.title("Relative error")
#                 plt.xlabel("X [cm]")
#                 plt.ylabel("Z [cm]")
#                 plt.show()          
                
#         elif temp == 3:
#             zval = input("Enter a Z coord: ")
#             s,t,v,z = blocks[0].UnpackGivenZE(zval,e)
#             s,t,v2,z = blocks[0].UnpackGivenZE(zval,1)
#             plt.xlabel("X [cm]")
#             plt.ylabel("Y [cm]")
#             plott(s,t,v)
#             if (float(input("Do you want to see a plot of the error? 1 or 0: "))==1.0):
#                 plt.contourf(s,t,z,cmap=cm.jet)
#                 plt.title("Relative error")
#                 plt.xlabel("Y [cm]")
#                 plt.ylabel("Z [cm]")
#                 plt.show()
                
#         elif temp == 4:
#             e = blocks[0].__ChooseCellE(float(input("choose an energy level: ")))
            
#         elif temp == 9:
#             break
   