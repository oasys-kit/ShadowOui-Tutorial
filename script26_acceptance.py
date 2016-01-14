#create file myaperture.dat needed for source optimization
file_name = "acceptance.dat"
f = open(file_name,'w')
f.write(" 3090.000      -0.005    0.005  -0.005  0.005")
f.close()
print("File written to disk: %s"%(file_name))