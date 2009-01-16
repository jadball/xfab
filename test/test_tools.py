import unittest
import numpy as n
from xfab import tools


class test_euler2u(unittest.TestCase):
    def test1(self):  
        phi1 = 0.0
        PHI  = 0.0
        phi2 = 0.0
        Umat = tools.euler2U(phi1,PHI,phi2)
        diff = n.abs(Umat-n.eye(3)).sum()
        self.assertAlmostEquals(diff,0,9)

    def test2(self):  
        phi1 = 0.1
        PHI  = 0.0
        phi2 = -0.1
        Umat = tools.euler2U(phi1,PHI,phi2)
        diff = n.abs(Umat-n.eye(3)).sum()
        self.assertAlmostEquals(diff,0,9)

class test_rodrigues(unittest.TestCase):

    def test_rod2U2rod(self):  
        rodvec = n.array([0.23,-0.34,0.7])
        Umat = tools.rod2U(rodvec)
        rodvec2 = tools.U2rod(Umat)

        diff = n.abs(rodvec-rodvec2).sum()
        self.assertAlmostEquals(diff,0,9)

        
    def test_U2rod2U(self):  
        phi1 = 0.2
        PHI  = 0.4
        phi2 = 0.1
        Umat = tools.euler2U(phi1,PHI,phi2)
        rodvec = tools.U2rod(Umat)
        Umat2 = tools.rod2U(rodvec)

        diff = n.abs(Umat-Umat2).sum()
        self.assertAlmostEquals(diff,0,9)


    def test_ubi2rod(self):  
        phi1 = 0.13
        PHI  = 0.4
        phi2 = 0.21
        cell = [3,4,5,80,95,100]
        Umat = tools.euler2U(phi1,PHI,phi2)
        ubi = n.linalg.inv(n.dot(Umat, tools.FormB(cell)))*2*n.pi
        rodubi = tools.ubi2rod(ubi)
        rodU = tools.U2rod(Umat)
        diff = n.abs(rodubi-rodU).sum()
        self.assertAlmostEquals(diff,0,9)

class test_twotheta(unittest.TestCase):

    def test_tth(self):
        # generate random gvector
        hkl = n.array([round(n.random.rand()*10-5),round(n.random.rand()*10-5),round(n.random.rand()*10-5)])
        ucell = n.array([3.5+n.random.rand(),3.5+n.random.rand(),3.5+n.random.rand(),89.5+n.random.rand(),89.5+n.random.rand(),89.5+n.random.rand()])
        B = tools.FormB(ucell)
        U = tools.euler2U(n.random.rand()*2.*n.pi,n.random.rand()*2.*n.pi,n.random.rand()*n.pi)
        wavelength = 0.95 + n.random.rand()*0.1
        gvec = n.dot(U,n.dot(B,hkl))
        tth = tools.tth(ucell, hkl, wavelength)
        tth2 = tools.tth2(gvec,wavelength)
        diff = n.abs(tth-tth2)
        self.assertAlmostEquals(diff,0,9)
        
class test_quarternions(unittest.TestCase):

    def test_quart2Omega(self):
        omega = n.random.rand()*360.
        Omega = tools.OMEGA(omega*n.pi/180.)
        Omega_quart = tools.quart2Omega(omega,0,0)
        diff = n.abs(Omega-Omega_quart).sum()
        self.assertAlmostEquals(diff,0,9)
        
    def test_find_omega(self):
        # generate random gvector
        hkl = n.array([round(n.random.rand()*10-5),round(n.random.rand()*10-5),round(n.random.rand()*10-5)])
        ucell = n.array([3.5+n.random.rand(),3.5+n.random.rand(),3.5+n.random.rand(),89.5+n.random.rand(),89.5+n.random.rand(),89.5+n.random.rand()])
        B = tools.FormB(ucell)
        U = tools.euler2U(n.random.rand()*2.*n.pi,n.random.rand()*2.*n.pi,n.random.rand()*n.pi)
        wavelength = 0.95 + n.random.rand()*0.1
        gvec = n.dot(U,n.dot(B,hkl))
        tth = tools.tth(ucell, hkl, wavelength)        
        # calculate corresponding eta and Omega using tools.find_omega_quart
        (omega1, eta1) = tools.find_omega_quart(gvec*wavelength/(4.*n.pi),tth,0,0)
        Om1 = []
        for i in range(len(omega1)):
            Om1.append(tools.quart2Omega(omega1[i]*180./n.pi,0,0))  
        # calculate corresponding eta and Omega using tools.find_omega
        omega2 = tools.find_omega(gvec,tth)
        Om2 = []
        for i in range(len(omega2)):
            Om2.append(tools.OMEGA(omega2[i]))
        # assert  
        for i in range(len(eta1)):          
            diff = n.abs(Om1[i]-Om2[i]).sum()
            self.assertAlmostEquals(diff,0,9)        
            
    def test_find_omega_wedge(self):
        # generate random gvector
        hkl = n.array([round(n.random.rand()*10-5),round(n.random.rand()*10-5),round(n.random.rand()*10-5)])
        ucell = n.array([3.5+n.random.rand(),3.5+n.random.rand(),3.5+n.random.rand(),89.5+n.random.rand(),89.5+n.random.rand(),89.5+n.random.rand()])
        B = tools.FormB(ucell)
        U = tools.euler2U(n.random.rand()*2.*n.pi,n.random.rand()*2.*n.pi,n.random.rand()*n.pi)
        wavelength = 0.95 + n.random.rand()*0.1
        gvec = n.dot(U,n.dot(B,hkl))
        tth = tools.tth(ucell, hkl, wavelength)
        wedge = n.random.rand()-.5
        # calculate corresponding eta and Omega using tools.find_omega_quart
        (omega1, eta1) = tools.find_omega_quart(gvec*wavelength/(4.*n.pi),tth,0,wedge)
        Om1 = []
        for i in range(len(omega1)):
            Om1.append(tools.quart2Omega(omega1[i]*180./n.pi,0,wedge))  
        # calculate corresponding eta and Omega using tools.find_omega_wedge
        Phi_y = n.array([[ n.cos(wedge), 0, n.sin(wedge)],
                         [0         , 1, 0        ],
                         [-n.sin(wedge), 0, n.cos(wedge)]])
        gvec = n.dot(n.transpose(Phi_y),gvec)
        (omega2, eta2) = tools.find_omega_wedge(gvec,tth,-wedge)
        Om2 = []
        for i in range(len(omega2)):
            Om2.append(n.dot(Phi_y,n.dot(tools.OMEGA(omega2[i]),n.transpose(Phi_y))))
        #assert  
        for i in range(len(eta1)):          
            diff = n.abs(eta1[i]-eta2[i])
            self.assertAlmostEquals(diff,0,9)
            diff = n.abs(Om1[i]-Om2[i]).sum()
            self.assertAlmostEquals(diff,0,9)        

class test_ABepsilon(unittest.TestCase):

    def test_ucell2A2ucell(self):
        ucell = n.array([3.5+n.random.rand(),3.5+n.random.rand(),3.5+n.random.rand(),89.5+n.random.rand(),89.5+n.random.rand(),89.5+n.random.rand()])
        A = tools.FormA(ucell)
        ucell2 = tools.A2ucell(A)
        diff = n.abs(ucell-ucell2).sum()
        self.assertAlmostEquals(diff,0,9)        
        
        
    def test_ucell2B2ucell(self):
        ucell = n.array([3.5+n.random.rand(),3.5+n.random.rand(),3.5+n.random.rand(),89.5+n.random.rand(),89.5+n.random.rand(),89.5+n.random.rand()])
        B = tools.FormB(ucell)
        ucell2 = tools.B2ucell(B)
        diff = n.abs(ucell-ucell2).sum()
        self.assertAlmostEquals(diff,0,9)  

    def test_epsilon2B2epsilon(self):
        ucell = n.array([3.5+n.random.rand(),3.5+n.random.rand(),3.5+n.random.rand(),89.5+n.random.rand(),89.5+n.random.rand(),89.5+n.random.rand()])
        eps = (n.random.rand(6)-.5)/1000.
        B = tools.epsilon2B(eps,ucell)
        eps2 = tools.B2epsilon(B,ucell)
        
if __name__ == '__main__':
    unittest.main()
