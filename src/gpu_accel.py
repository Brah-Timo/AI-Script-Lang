import numpy as np
import cupy as cp  # مكتبة CUDA للتسريع على GPU

class GPUAccelerator:
    def __init__(self):
        self.memory_pool = cp.cuda.MemoryPool()  # تحسين إدارة الذاكرة
        cp.cuda.set_allocator(self.memory_pool.malloc)

    def execute_matrix_mul(self, A, B):
        """ تنفيذ ضرب المصفوفات على GPU باستخدام CuPy """
        A_gpu = cp.asarray(A)
        B_gpu = cp.asarray(B)
        result_gpu = cp.dot(A_gpu, B_gpu)
        return cp.asnumpy(result_gpu)  # تحويل النتيجة إلى CPU

    def accelerate_tensor_ops(self, tensor):
        """ تطبيق عمليات رياضية متقدمة على المصفوفات باستخدام GPU """
        tensor_gpu = cp.asarray(tensor)
        return cp.asnumpy(cp.exp(tensor_gpu))  # تنفيذ دالة الأُس على GPU

    def optimize_large_data(self, data):
        """ تحسين أداء العمليات على بيانات ضخمة باستخدام CuPy """
        data_gpu = cp.asarray(data)
        return cp.asnumpy(cp.log1p(data_gpu))  # تنفيذ log(1 + x) على GPU

    def transfer_data_to_gpu(self, data):
        """ تحويل بيانات NumPy إلى CuPy لنقلها إلى GPU """
        return cp.asarray(data)

    def transfer_data_to_cpu(self, data_gpu):
        """ تحويل بيانات CuPy إلى NumPy لنقلها إلى CPU """
        return cp.asnumpy(data_gpu)

# مثال استخدام:
if __name__ == "__main__":
    gpu = GPUAccelerator()

    A = np.random.rand(4, 4)
    B = np.random.rand(4, 4)
    print("🔹 GPU Matrix Multiplication Result:\n", gpu.execute_matrix_mul(A, B))

    tensor = np.random.rand(5, 5)
    print("🔹 GPU Tensor Exponential Result:\n", gpu.accelerate_tensor_ops(tensor))

    large_data = np.random.rand(1000, 1000)
    print("🔹 Optimized Large Data Computation:\n", gpu.optimize_large_data(large_data))
