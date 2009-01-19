import tntbx.eigensystem

from scitbx.array_family import flex
from libtbx.test_utils import approx_equal
from itertools import count

try:
  import platform
except ImportError:
  release = ""
else:
  release = platform.release()
if (   release.endswith("_FC4")
    or release.endswith("_FC4smp")):
  Numeric = None # LinearAlgebra.generalized_inverse is broken
else:
  try:
    import Numeric
  except ImportError:
    Numeric = None
  else:
    import LinearAlgebra

def exercise_eigensystem():
  m = [0.13589302585705959, -0.041652833629281995, 0.0,
       -0.02777294381303139, 0.0, -0.028246956907939123,
       -0.037913518508910102, -0.028246956907939123, 0.028246956907939127,
       0.066160475416849232, 0.0, -1.998692119493731e-18, 0.0,
       1.9342749002960583e-17, 2.1341441122454314e-17, -0.041652833629281995,
       0.16651402880692701, -0.041652833629282252, -0.054064923492613354,
       -0.041657741914063608, -0.027943612435735281, 0.058527480224229975,
       -0.027943612435735132, -0.034820867346713427, -0.030583867788494697,
       0.062764479782448576, 1.2238306785281e-33, 0.0, 2.0081205093967302e-33,
       8.4334666705394195e-34, 0.0, -0.041652833629282252,
       0.13589302585705959, 0.0, -0.041574928784987308, -0.028246956907939064,
       0.0, -0.028246956907939064, 0.063090910812553094,
       0.028246956907939068, -0.034843953904614026, -1.9986921194937106e-18,
       -8.9229029691439759e-18, 1.0316952905846454e-17, 3.3927420561961863e-18,
       -0.02777294381303139, -0.05406492349261334, 0.0, 1.0754189352289423,
       0.0, 0.055233150062734049, -0.030424256077943676, 0.02480889398479039,
       -0.024808893984790394, -0.024808893984790425, 0.0,
       -6.8972719971392908e-18, -1.7405118013554239e-17,
       6.1312902919038241e-18, -4.3765557245111121e-18, 0.0,
       -0.041657741914063601, -0.041574928784987308, 0.0, 1.0754189352289425,
       0.02824584556921347, 0.0, 0.056206884746120872, -0.028245845569213546,
       -0.02824584556921347, -0.027961039176907447, 5.9506047506615062e-18,
       0.0, -1.4122576510436466e-18, -7.3628624017051534e-18,
       -0.028246956907939123, -0.027943612435735277, -0.028246956907939064,
       0.055233150062734056, 0.028245845569213474, 0.058637637326162888,
       -0.021712364921140592, 0.038218912676148069, -0.039777184406252442,
       -0.036925272405022302, 0.0015582717301043682, 4.0451470549537404e-18,
       0.0, -1.3724767734658202e-17, -1.7769914789611943e-17,
       -0.037913518508910102, 0.058527480224229982, 0.0, -0.030424256077943652,
       0.0, -0.021712364921140592, 0.28175206518101342, 0.0039066487534216467,
       -0.0039066487534216484, -0.26003970025987289, 0.0,
       7.5625035918149771e-18, 1.2380916665439571e-17, -1.0148697613996034e-16,
       -9.6668563066335756e-17, -0.028246956907939123, -0.027943612435735128,
       -0.028246956907939064, 0.02480889398479039, 0.056206884746120879,
       0.038218912676148069, 0.0039066487534216484, 0.058637637326162798,
       -0.031992570455625299, -0.042125561429569719, -0.026645066870537512,
       4.0451470549537242e-18, 9.6341055014789307e-18, -2.0511818948105707e-17,
       -1.4922860501580496e-17, 0.028246956907939127, -0.034820867346713427,
       0.063090910812553094, -0.024808893984790394, -0.028245845569213508,
       -0.039777184406252442, -0.0039066487534216501, -0.031992570455625306,
       0.2922682186182603, 0.043683833159674099, -0.26027564816263499,
       -5.2586006938540899e-18, 0.0, 9.7867664544895616e-18,
       1.5045367148343648e-17, 0.066160475416849232, -0.030583867788494701,
       0.028246956907939068, -0.024808893984790466, -0.028245845569213474,
       -0.036925272405022302, -0.26003970025987289, -0.042125561429569719,
       0.043683833159674092, 0.29696497266489519, -0.0015582717301043699,
       -7.5250966340669269e-19, 2.6213138712286628e-17,
       -1.5094268920622606e-17, 1.1871379455070714e-17, 0.0,
       0.062764479782448576, -0.034843953904614026, 0.0, -0.027961039176907457,
       0.0015582717301043665, 0.0, -0.026645066870537509, -0.26027564816263499,
       -0.0015582717301043699, 0.28692071503317257, -3.8759778199373453e-18,
       3.9691789817943108e-17, -8.14982209920807e-18, 3.5417945538672385e-17,
       -1.998692119493731e-18, 1.6308338425568088e-33, -1.9986921194937102e-18,
       -6.8972719971392892e-18, 5.950604750661507e-18, 4.0451470549537412e-18,
       7.5625035918149756e-18, 4.0451470549537242e-18, -5.2586006938540899e-18,
       -7.5250966340669346e-19, -3.8759778199373446e-18, 0.054471159454508082,
       0.0064409353489570716, 0.0035601061597435495, -0.044470117945807464,
       0.0, 0.0, -8.9229029691439759e-18, -1.7405118013554239e-17, 0.0, 0.0,
       1.2380916665439569e-17, 9.6341055014789307e-18, 0.0,
       2.6213138712286628e-17, 3.9691789817943114e-17, 0.0064409353489570777,
       0.47194161564298681, -0.17456675614101194, 0.29093392415301783,
       1.9342749002960583e-17, 1.4951347746978839e-33, 1.0316952905846454e-17,
       6.1312902919038033e-18, -1.4122576510436468e-18,
       -1.3724767734658202e-17, -1.0148697613996034e-16,
       -2.0511818948105704e-17, 9.7867664544895616e-18,
       -1.5094268920622603e-17, -8.1498220992080684e-18,
       0.0035601061597435478, -0.17456675614101194, 0.61470061296798617,
       0.4365737506672307, 2.1341441122454314e-17, 1.5911491532730484e-34,
       3.392742056196186e-18, -4.3765557245111453e-18, -7.3628624017051534e-18,
       -1.7769914789611943e-17, -9.6668563066335731e-17,
       -1.4922860501580496e-17, 1.5045367148343648e-17, 1.1871379455070717e-17,
       3.5417945538672392e-17, -0.044470117945807464, 0.29093392415301783,
       0.4365737506672307, 0.77197779276605605]
  #
  m = flex.double(m)
  m.resize(flex.grid(15,15))
  s = tntbx.eigensystem.real(m)
  e_values = s.values()
  #
  if (Numeric is not None):
    n = Numeric.asarray(m)
    n.shape = (15,15)
    n_values = LinearAlgebra.eigenvalues(n)
    assert len(e_values) == len(n_values)
    #
    print '               Eigenvalues'
    print '      %-16s %-16s' % ('TNT','Numpy')
    for i,e,n in zip(count(1), e_values, n_values):
      if (isinstance(e, complex)): e = e.real
      if (isinstance(n, complex)): n = n.real
      print "  %2d %16.12f %16.12f" % (i, e, n)
  #
  sorted_values = e_values.select(
    flex.sort_permutation(data=e_values, reverse=True))
  assert approx_equal(sorted_values, [
    1.1594490522786849, 1.0940938851317932, 1.0788186474215089,
    0.68233800454109983, 0.62042869735706307, 0.53297576878337871,
    0.18708677344352156, 0.16675360561093594, 0.12774949816038345,
    0.071304124011754358, 0.02865105770313877, 0.027761263516876356,
    1.5830173657858035e-17, 2.6934929627275647e-18,
    -5.5511151231257827e-17])

def run():
  exercise_eigensystem()
  print "OK"

if (__name__ == "__main__"):
  run()
