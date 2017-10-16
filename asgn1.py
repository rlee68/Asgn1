# Rachel Lee
# CSC 477
# Assignment 1

from vtk import *
import sys
import math

def checkArgs():
	if len(sys.argv) == 2:
		return sys.argv[-1]
	else:
		sys.exit("Enter a pdb file name.")

def getResolution(pdb):
	res = math.sqrt(300000.0/pdb.GetNumberOfAtoms())
	if res > 20:
		res = 20
	if res < 4:
		res = 4
	return res

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

def main():
	#Check for a pdb file name
	file = checkArgs()
	pdb = vtkPDBReader()
	pdb.SetFileName(file)
	pdb.SetHBScale(1)
	pdb.SetBScale(1)
	print(pdb.GetNumberOfAtoms())
	pdb.Update()

	res = getResolution(pdb)
	atom = drawAtoms(pdb, res)
	bond = drawBonds(pdb, res)

	#Create a camera
	camera = vtkCamera()
	camera.SetPosition(0, 0, 150)
	camera.SetFocalPoint(0, 0, 0)

	#Create a renderer, render window, and interactor
	renderer = vtkRenderer()
	renderer.SetActiveCamera(camera)
	renderWindow = vtkRenderWindow()
	renderWindow.AddRenderer(renderer)
	renderWindow.SetSize(2560, 1440)
	renderWindowInteractor = vtkRenderWindowInteractor()
	renderWindowInteractor.SetRenderWindow(renderWindow)

	#Add the actor to the scene
	renderer.AddActor(atom)
	renderer.AddActor(bond)
	renderer.SetBackground(1, 1, 1)

	#Render and interact
	renderWindow.Render()
	renderWindowInteractor.Start()

if __name__ == "__main__":
    main()