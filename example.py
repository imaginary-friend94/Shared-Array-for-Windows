from multiprocessing import Pool
import winsharedarray as sa
import numpy as np

def mutex_test(num):
	arr = np.zeros((1,1))
	mutx = sa.open_mutex("sem_cntr_ex")
	cntr = sa.attach_mem_sh("/shm_mem_npy_counter")
	for ix in range(num):
		sa.capture_mutex(mutx)
		cntr[0][0] += 1
		sa.release_mutex(mutx)

if __name__ == '__main__':
	print(dir(sa))

	## TEST 1
	print("TEST 1")

	arr = np.zeros((5,5))

	print(sa.check_mem_sh("/shm_mem_npy_test_1f"))
	sa.create_mem_sh("/shm_mem_npy_test_1f", arr)

	try:
		array_attached = sa.attach_mem_sh("/shm_mem_npy_test_12f")
	except RuntimeError:
		array_attached = sa.attach_mem_sh("/shm_mem_npy_test_1f")	

	array_attached[:3,:1] = 1
	print(array_attached)
	print(sa.delete_mem_sh("/shm_mem_npy_test_1f"))
	print(sa.check_mem_sh("/shm_mem_npy_test_1f"))

	## TEST 2
	print("TEST 2")

	arr = np.zeros((1081, 1920, 24))

	sa.create_mem_sh("/shm_mem_npy_test_2", arr)

	try:
		array_attached = sa.attach_mem_sh("/shm_mem_npy_test_12")
	except RuntimeError:
		array_attached = sa.attach_mem_sh("/shm_mem_npy_test_2")	

	array_attached[:30,:300] = 88.
	print(arr.mean())
	print(array_attached[:,:,:1].mean())
	sa.delete_mem_sh("/shm_mem_npy_test_2")
	## TEST 3
	print("TEST 3")

	arr = np.zeros((4,4)).astype(np.float64)
	sa.create_mem_sh("/shm_mem_npy_test_3", arr)
	array_attached = sa.attach_mem_sh("/shm_mem_npy_test_3")
	# do something
	array_attached = sa.attach_mem_sh("/shm_mem_npy_test_3")
	#import time
	#time.sleep(10)
	#print(sa.delete_mem_sh("/shm_mem_npy_test_3"))

	array_attached = sa.attach_mem_sh("/shm_mem_npy_test_3")	

	array_attached[:3,:1] = 1
	print(array_attached)

	print(
		sa.check_mem_sh("/shm_mem_npy_test_3"),
		sa.check_mem_sh("/shm_mem_npy_test_55")
	)
	sa.delete_mem_sh("/shm_mem_npy_test_3")
	sa.create_mem_sh("shm_mem_npy_test_55", arr)
	print(
		sa.check_mem_sh("/shm_mem_npy_test_3"),
		sa.check_mem_sh("/shm_mem_npy_test_55")
	)
	sa.delete_mem_sh("/shm_mem_npy_test_55")
	## TEST 4
	print("TEST 4")

	mutx = sa.create_mutex("sem_cntr_ex")
	sa.release_mutex(mutx)

	arr = np.zeros((1,1))
	sa.create_mem_sh("/shm_mem_npy_counter", arr)

	p = Pool(5)
	p.map(mutex_test, [10000, 20000, 30000])

	cntr = sa.attach_mem_sh("/shm_mem_npy_counter")
	print(cntr[0][0]) # == 10000+20000+30000=60000
	sa.delete_mem_sh("/shm_mem_npy_counter")
	print("GetLastError() = ", sa.get_last_error())

