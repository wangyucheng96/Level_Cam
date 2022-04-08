import numpy as np
arr1 = np.array([[1372.520173890660, 624.5073097515924], [1372.5276306632102, 623.5346245161421],
                [1372.5186972604693, 623.4596631264588], [1372.5435266371167, 623.5173742343953],
                [1372.5155423217143, 623.5036245888779], [1372.5219754229781, 623.4721351891103],
                [1372.5562499943692, 623.4671654154973], [1372.5240325333239, 622.5097512178322],
                [1372.5241761713046, 622.5175921836022], [1372.5224297074017, 624.4917452228523]])

arr2 = np.array([[507.153079922715, 520.7963029387379], [507.16601317442513, 520.669129375012],
                [507.1632900514191, 520.6886765087074], [507.4092341574921, 520.6819804920036],
                [507.69586363186346, 520.6466156489308], [507.1900562321473, 520.5787428069491],
                [507.36391565774176, 520.7653900151056], [507.6034052006587, 520.9063693652963],
                [506.87106673774275, 520.6393883409362], [507.25985164484337, 520.6768154919765]])
# print("variance:", np.var(arr))
# print("sqrt of variance:", np.sqrt(np.var(arr)))
# print("standard deviation ", np.std(arr))
print("standard deviation ", np.std(arr1, axis=0, ddof=1))

print("standard deviation ", np.std(arr2, axis=0, ddof=1))

# print("standard deviation ", np.std(arr, axis=1))

