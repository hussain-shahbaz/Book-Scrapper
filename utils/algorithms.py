class Algorithm:
    def BubbleSort(self, arr):
        arr = arr.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    def InsertionSort(self, arr):
        arr = arr.copy()
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    def SelectionSort(self, arr):
        arr = arr.copy()
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

    def MergeSort(self, arr):
        def merge(left, right):
            res = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    res.append(left[i])
                    i += 1
                else:
                    res.append(right[j])
                    j += 1
            res.extend(left[i:])
            res.extend(right[j:])
            return res

        if len(arr) <= 1:
            return arr.copy()

        mid = len(arr) // 2
        left = self.MergeSort(arr[:mid])
        right = self.MergeSort(arr[mid:])
        return merge(left, right)

    def QuickSort(self, arr):
        arr = arr.copy()

        def partition(a, l, r):
            pivot = a[r]
            idx = l
            for j in range(l, r):
                if a[j] <= pivot:
                    a[j], a[idx] = a[idx], a[j]
                    idx += 1
            a[idx], a[r] = a[r], a[idx]
            return idx

        def quick(a, l, r):
            if l >= r:
                return
            p = partition(a, l, r)
            quick(a, l, p - 1)
            quick(a, p + 1, r)

        quick(arr, 0, len(arr) - 1)
        return arr

    def CountSort(self, arr):
        arr = arr.copy()
        if not arr:
            return arr
        minimum = min(arr)
        maximum = max(arr)
        size = maximum - minimum + 1
        freq = [0] * size

        for n in arr:
            freq[n - minimum] += 1

        for i in range(1, len(freq)):
            freq[i] += freq[i - 1]

        ans = [0] * len(arr)
        for i in range(len(arr) - 1, -1, -1):
            freq[arr[i] - minimum] -= 1
            idx = freq[arr[i] - minimum]
            ans[idx] = arr[i]
        return ans

    def RadixSort(self, arr):
        arr = arr.copy()
        if not arr:
            return arr
        def getMax(a):
            m = a[0]
            for x in a:
                if x > m:
                    m = x
            return m

        def countSortByDigit(a, exp):
            output = [0] * len(a)
            freq = [0] * 10
            for num in a:
                digit = (num // exp) % 10
                freq[digit] += 1
            for i in range(1, 10):
                freq[i] += freq[i - 1]
            for i in range(len(a) - 1, -1, -1):
                digit = (a[i] // exp) % 10
                freq[digit] -= 1
                output[freq[digit]] = a[i]
            for i in range(len(a)):
                a[i] = output[i]

        maximum = getMax(arr)
        exp = 1
        while maximum // exp > 0:
            countSortByDigit(arr, exp)
            exp *= 10
        return arr

    def BucketSort(self, arr):
        arr = arr.copy()
        n = len(arr)
        if n == 0:
            return arr
        buckets = [[] for _ in range(n)]
        for num in arr:
            idx = int(num * n)
            if idx >= n:
                idx = n - 1
            buckets[idx].append(num)

        def insertion(bucket):
            for i in range(1, len(bucket)):
                key = bucket[i]
                j = i - 1
                while j >= 0 and key < bucket[j]:
                    bucket[j + 1] = bucket[j]
                    j -= 1
                bucket[j + 1] = key
            return bucket

        for b in buckets:
            insertion(b)

        res = []
        for b in buckets:
            res.extend(b)
        return res
