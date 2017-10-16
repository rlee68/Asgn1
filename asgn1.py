# Rachel Lee
# CSC 477
# Assignment 1

from vtk import *
import sys
import math

#Check if there is a specified pdb file
def checkArgs():
	if len(sys.argv) == 2:
		return sys.argv[-1]
	else:
		sys.exit("Enter a pdb file name.")


#Gets the resolution for the atoms and bonds
def getResolution(pdb):
	res = math.sqrt(300000.0/pdb.GetNumberOfAtoms())
	if res > 20:
		res = 20
	if res < 4:
		res = 4
	return res


#Renders the atoms of the molecule
def drawAtoms(pdb, res):
	#Represent the atoms as spheres
	sphere = vtkSphereSource()
	sphere.SetCenter(0, 0, 0)
	sphere.SetRadius(1)
	sphere.SetThetaResolution(int(res))
	sphere.SetPhiResolution(int(res))

	#Create atoms of the molecule
	glyph = vtkGlyph3D()
	glyph.SetInputConnection(pdb.GetOutputPort())
	glyph.SetOrient(1)
	glyph.SetColorMode(1)
	glyph.SetScaleMode(3)
	glyph.SetScaleFactor(0.25)
	glyph.SetSourceConnection(sphere.GetOutputPort())

	#Create atom mapper and actor
	atomMapper = vtkPolyDataMapper()
	atomMapper.SetInputConnection(glyph.GetOutputPort())
	atom = vtkActor()
	atom.SetMapper(atomMapper)
	return atom


#Renders the bonds of the molecule
def drawBonds(pdb, res):
	#Represent the bonds as tube
	tube = vtkTubeFilter()
	tube.SetInputConnection(pdb.GetOutputPort())
	tube.SetNumberOfSides(int(res))
	tube.SetRadius(0.1)
	tube.SetVaryRadius(0)
	tube.SetRadiusFactor(10)

	#Create bond mapper and actor
	bondMapper = vtkPolyDataMapper()
	bondMapper.SetInputConnection(tube.GetOutputPort())
	bond = vtkLODActor()
	bond.SetMapper(bondMapper)
	return bond


#Creates left render (molecule image)
def leftViewport(renderWindow):
	leftR = vtkRenderer()
	renderWindow.AddRenderer(leftR)
	leftR.SetViewport(0, 0, 0.5, 1)
	leftR.SetBackground(1, 1, 1)
	leftR.ResetCamera()
	return leftR


#Creates right render (amino acid composition)
def rightViewport(pdb, renderWindow):
	view = vtkContextView()
	rightR = view.GetRenderer()
	renderWindow.AddRenderer(rightR)
	rightR.SetViewport(0.5, 0, 1, 1)
	rightR.SetBackground(0.5, 0.5, 0.5)
	rightR.ResetCamera()

	chart = vtkChartXY()
	view.GetScene().AddItem(chart)

	table = vtkTable()


#Executes the molecule viewer 
def main():
	#Check for a pdb file name
	file = checkArgs()
	pdb = vtkPDBReader()
	pdb.SetFileName(file)
	#pdb.SetHBScale(1)
	#pdb.SetBScale(1)
	pdb.Update()

	res = getResolution(pdb)
	atom = drawAtoms(pdb, res)
	bond = drawBonds(pdb, res)

	#Create main render window and interactor
	renderWindow = vtkRenderWindow()
	renderWindow.SetSize(2560, 1440)
	renderWindowInteractor = vtkRenderWindowInteractor()
	trackball = vtkInteractorStyleTrackballCamera()
	renderWindowInteractor.SetInteractorStyle(trackball)
	renderWindowInteractor.SetRenderWindow(renderWindow)

	#Create left and right renders
	left = leftViewport(renderWindow)
	left.AddActor(bond)
	right = rightViewport(pdb, renderWindow)

	renderWindow.SetMultiSamples(0)
	renderWindow.Render()
	renderWindow.SetWindowName('Molecule Viewer: %s' % file)
	renderWindowInteractor.Start()


if __name__ == "__main__":
    main()