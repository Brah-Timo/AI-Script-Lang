from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

class ParallelExecutor:
    def __init__(self, max_workers=4, use_threads=True):
        """إنشاء منفذ متوازي باستخدام Threads أو Processes"""
        self.use_threads = use_threads
        self.max_workers = max_workers

    def run_parallel(self, function, data, **kwargs):
        """تشغيل الوظائف بشكل متوازي باستخدام `Threads` أو `Processes`"""
        Executor = ThreadPoolExecutor if self.use_threads else ProcessPoolExecutor

        with Executor(max_workers=self.max_workers) as executor:
            results = list(executor.map(lambda x: function(x, **kwargs), data))
        
        return results

# ✅ مثال استخدام:
if __name__ == "__main__":
    executor = ParallelExecutor(max_workers=4, use_threads=False)  # استخدم `Processes`

    def power(n, exponent=2):
        """حساب القوة مع دعم المعاملات الإضافية"""
        return n ** exponent

    data = [1, 2, 3, 4, 5]
    print("Parallel Execution Results:", executor.run_parallel(power, data, exponent=3))
