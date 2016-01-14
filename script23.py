import Shadow

out_object = in_object.duplicate()

# pickup the beam at the source
beam = out_object._beam
# retrace it 40 m
beam.retrace(4000)

#pick up the beam after the Laue crystal
beam_after_laue = Shadow.Beam()
beam_after_laue.load("star.01")
# extract the columns that contain the electric fields
columns_with_intensity = beam_after_laue.rays[:,[6,7,8,15,16,17]]
# copy the electric fields from beam after Laue crystal to beam before Laue crystal
beam.rays[:,[6,7,8,15,16,17]] = columns_with_intensity

# prepare output
#out_object = in_object
out_object._beam = beam